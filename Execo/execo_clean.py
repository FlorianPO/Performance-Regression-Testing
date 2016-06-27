#!/usr/bin/env python
"""
This script generate the MPI traces using the NAS bachmarks and Extrae
tracing tool. The NAS bench executatble are in this repository.
Extrae is installed on the deployed environment.
It run on the graphene cluster using all the nodes under one switch to
avoid communication contention.
It use *execo* to run the experiment on Grid'5000 with parameters sweep.
Only one MPI process is running by node to be consistent with Simgrid
simple computation modele.
"""
import os
import shutil
import ipdb
import traceback
import time
from execo import SshProcess, format_date
from execo_g5k import oarsub, oardel, OarSubmission, \
    get_oar_job_nodes, wait_oar_job_start, \
    get_cluster_site
from execo_g5k.kadeploy import deploy, Deployment
from execo_engine import Engine, ParamSweeper, sweep, slugify, logger, HashableDict

script_path = os.path.dirname(os.path.realpath(__file__))

is_a_test = False

instrument_mpi = False

def prediction_callback(ts):
    logger.info("job start prediction = %s" % (format_date(ts),))


class mpi_bench(Engine):

    def setup_result_dir(self):
        result_type = ""
        if not instrument_mpi:
            result_type = 'notrace_' + result_type
        #if is_a_test:
        #    result_type = 'test_' + result_type
        self.result_dir = script_path + '/' + result_type + 'results_' + time.strftime("%Y-%m-%d--%H-%M-%S")

    def run(self):
        """Inherited method, put here the code for running the engine"""
        if is_a_test:
            logger.warn("THIS IS TEST")
        if not instrument_mpi:
            logger.warn("NO MPI TRACING")

        # define parameter consistent with the kadeploy image
        mpi_options = '--mca btl self,sm,tcp'
        cluster = 'graphene'
        switch = 'sgraphene4'
        env_name = "debian8_workload_generation_nfs"
        npb_bin_path = script_path + '/NPB_bin'

        # define the parameters
        if is_a_test:
            nb_nodes = ['1', '2']
            size = ['B']
        else:
            nb_nodes = ['1', '2', '4', '8', '16', '32']
            size = ['B', 'C', 'D']
        self.parameters = {
            'nb_nodes': nb_nodes,
            'size': size,
            'bench': ['is', 'ft', 'lu']
        }

        # define the iterator over the parameters combinations
        self.sweeper = ParamSweeper(os.path.join(self.result_dir, "sweeps"),
                                    sweep(self.parameters))

        # Due to previous (using -c result_dir) run skip some combination
        logger.info('Skipped parameters:' + \
                    '{}'.format(str(self.sweeper.get_skipped())))

        logger.info('Number of parameters combinations {}'.format(
            str(len(self.sweeper.get_remaining()))))

        # go to the result folder before everything
        os.chdir(self.result_dir)

        site = get_cluster_site(cluster)
        if is_a_test:
            jobs = oarsub([(OarSubmission(resources="{cluster='" + cluster + "'}/nodes=2",
                                      job_type='deploy',
                                      walltime='00:35:00'), site)])
        else:
            jobs = oarsub([(OarSubmission(resources="{switch='" + switch + "'}/switch=1",
                                      job_type='deploy',
                                      walltime='04:00:00'),
                        site)])

        job_id, site = jobs[0]
        if job_id:
            try:
                logger.info("waiting job start %s on %s" % (job_id, site))
                wait_oar_job_start(job_id, site, prediction_callback = prediction_callback)
                logger.info("getting nodes of %s on %s" % (job_id, site))
                nodes = get_oar_job_nodes(job_id, site)
                logger.info("create hostfiles for all combinations")
                for node_number in nb_nodes:
                    hostfile_filename = self.result_dir + '/' + 'hostfile-' + node_number
                    with open(hostfile_filename, 'w') as hostfile:
                        for node in nodes[:int(node_number)]:
                            print>>hostfile, node.address


                logger.info("deploying nodes: {}".format(str(nodes)))
                deployed, undeployed = deploy(
                    Deployment(nodes, env_name=env_name))
                if undeployed:
                    logger.warn("NOT deployed nodes: {}".format(str(undeployed)))
                    raise RuntimeError('Deployement failed')

                # Iterate over the parameters and execute the bench
                while len(self.sweeper.get_remaining()) > 0:
                    comb = self.sweeper.get_next()
                    logger.info('Processing new combination %s' % (comb,))
                    if (comb['bench'] == 'lu' and comb['size'] == 'D'):
                        logger.info('skip this combination')
                        self.sweeper.skip(comb)
                        continue

                    if comb['nb_nodes'] == '1':
                        extrae_config = 'extrae.xml'
                    else:
                        # FIXME: Warning this is NOT providing Paraver
                        # trace so they have to be generated manualy using
                        # /opt/extrae/mpi2prv in the deployed env
                        extrae_config = 'extrae_no_merge.xml'

                    mpi_env_vars = ""
                    if instrument_mpi:
                        mpi_env_vars = '-x LD_PRELOAD=/opt/extrae/lib/libmpitrace.so ' + \
                                       '-x EXTRAE_CONFIG_FILE=' + script_path + '/' + extrae_config

                    mpi_command = '{}.{}.{}'.format(comb['bench'],
                                                    comb['size'],
                                                    comb['nb_nodes'])

                    hostfile_filename = self.result_dir + '/' + 'hostfile-' + comb['nb_nodes']
                    bench_cmd = ('time mpirun {option} -hostfile {hostfile} '
                            '{env_vars} {command}').format(option=mpi_options,
                                       hostfile=hostfile_filename,
                                       env_vars=mpi_env_vars,
                                       command=npb_bin_path + "/" + mpi_command)
                    lu_bench = SshProcess("cd " + self.result_dir +
                                               "; " + bench_cmd, nodes[0])
                    lu_bench.stdout_handlers.append(
                        self.result_dir + '/' + slugify(comb) + '.out')
                    logger.info("generate command: {}".format(bench_cmd))
                    lu_bench.run()
                    if lu_bench.ok:
                        logger.info("comb ok: %s" % (comb,))
                        self.sweeper.done(comb)
                        # save results
                        # for extension in ['pcf', 'prv', 'row']:
                        #     filename = mpi_command + '.' + extension
                        #     shutil.move(filename, self.result_dir)
                        continue
            except Exception as exception:
                traceback.print_exc()
                logger.warn("comb NOT ok: %s" % (comb,))
                self.sweeper.cancel(comb)
            finally:
                logger.info("delete job: {}".format(jobs))
                oardel(jobs)

if __name__ == "__main__":
    engine = mpi_bench()
    engine.start()
