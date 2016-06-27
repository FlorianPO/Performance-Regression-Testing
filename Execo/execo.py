#!/usr/bin/env python2

# Tiré de https://github.com/oar-team/batsim-experiments/blob/master/replay_workload/oar_replay_workload.py

"""
This script is running a complete OAR cluster deployment on Grid'5000 to
experiment OAR scheduling policies in real conditions.

It use the development version of an OAR scheduler name Kamelot

It give as an results information about scheduling that was done.
"""

import os
import time
import ipdb
import traceback
import json
from shutil import copy
from execo import Process, SshProcess, Remote, format_date, Put
from execo_g5k import oarsub, oardel, OarSubmission, \
    get_oar_job_nodes, wait_oar_job_start
from execo_g5k.kadeploy import deploy, Deployment
from execo_engine import Engine, logger, ParamSweeper, sweep
from execo.report import Report

script_path = os.path.dirname(os.path.realpath(__file__))

is_a_test = False

reservation_job_id = None

alredy_configured = False


def prediction_callback(ts):
    logger.info("job start prediction = %s" % (format_date(ts),))


class oar_replay_workload(Engine):

    def init(self):
        parser = self.options_parser
        parser.add_option('--is_a_test',
                          dest='is_a_test',
                          action='store_true',
                          default=False,
                          help='prefix the result folder with "test", enter '
                          'a debug mode if fails and remove the job '
                          'afterward, unless it is a reservation')
        parser.add_option('--already_configured',
                          dest='already_configured',
                          action='store_true',
                          default=False,
                          help='if set, the OAR cluster is not re-configured')

        parser.add_option('--reservation_id',
                          help="Grid'5000 reservation job ID")

        parser.add_argument('experiment_config',
                            'The config JSON experiment description file')

    def setup_result_dir(self):
        is_a_test = self.options.is_a_test

        run_type = ""
        if is_a_test:
            run_type = "test_"
        self.result_dir = script_path + '/' + run_type + 'results_' + \
            time.strftime("%Y-%m-%d--%H-%M-%S")
        logger.info('resutlt directory: {}'.format(self.result_dir))

    def run(self):
        """Run the experiment"""
        already_configured = self.options.already_configured
        reservation_job_id = int(self.options.reservation_id) \
            if self.options.reservation_id is not None else None
        is_a_test = self.options.is_a_test

        if is_a_test:
            logger.warn('THIS IS A TEST! This run will use only a few '
                        'resources')

        # make the result folder writable for all
        os.chmod(self.result_dir, 0o777)
        # Import configuration
        with open(self.args[0]) as config_file:
            config = json.load(config_file)
        # backup configuration
        copy(self.args[0], self.result_dir)

        site = config["grid5000_site"]
        resources = config["resources"]
        nb_experiment_nodes = config["nb_experiment_nodes"]
        walltime = str(config["walltime"])
        env_name = config["kadeploy_env_name"]
        workloads = config["workloads"]
        # check if workloads exists (Suppose that the same NFS mount point
        # is present on the remote and the local environment
        for workload_file in workloads:
            with open(workload_file):
                pass
            # copy the workloads files to the results dir
            copy(workload_file, self.result_dir)

        # define the workloads parameters
        self.parameters = {
            'workload_filename': workloads
        }
        logger.info('Workloads: {}'.format(workloads))

        # define the iterator over the parameters combinations
        self.sweeper = ParamSweeper(os.path.join(self.result_dir, "sweeps"),
                                    sweep(self.parameters))

        # Due to previous (using -c result_dir) run skip some combination
        logger.info('Skipped parameters:' +
                    '{}'.format(str(self.sweeper.get_skipped())))

        logger.info('Number of parameters combinations {}'.format(
            str(len(self.sweeper.get_remaining()))))
        logger.info('combinations {}'.format(
            str(self.sweeper.get_remaining())))

        if reservation_job_id is not None:
            jobs = [(reservation_job_id, site)]
        else:
            jobs = oarsub([(OarSubmission(resources=resources,
                                          job_type='deploy',
                                          walltime=walltime), site)])
        job_id, site = jobs[0]
        if job_id:
            try:
                logger.info("waiting job start %s on %s" % (job_id, site))
                wait_oar_job_start(
                    job_id, site, prediction_callback=prediction_callback)
                logger.info("getting nodes of %s on %s" % (job_id, site))
                nodes = get_oar_job_nodes(job_id, site)
                # sort the nodes
                nodes = sorted(nodes, key=lambda node: node.address)
                # get only the necessary nodes under the switch
                if nb_experiment_nodes > len(nodes):
                    raise RuntimeError('The number of given node in the '
                                       'reservation ({}) do not match the '
                                       'requested resources '
                                       '({})'.format(len(nodes),
                                                     nb_experiment_nodes))
                nodes = nodes[:nb_experiment_nodes]
                logger.info("deploying nodes: {}".format(str(nodes)))
                deployed, undeployed = deploy(
                    Deployment(nodes, env_name=env_name),
                    check_deployed_command=already_configured)
                if undeployed:
                    logger.warn(
                        "NOT deployed nodes: {}".format(str(undeployed)))
                    raise RuntimeError('Deployement failed')

                if not already_configured:

                    # install OAR
                    install_cmd = "apt-get update; apt-get install -y "
                    node_packages = "oar-node"
                    logger.info(
                        "installing OAR nodes: {}".format(str(nodes[1:])))
                    install_oar_nodes = Remote(
                        install_cmd + node_packages,
                        nodes[1:],
                        connection_params={'user': 'root'})
                    install_oar_nodes.start()

                    server_packages = ("oar-server oar-server-pgsql oar-user "
                                       "oar-user-pgsql postgresql python3-pip "
                                       "libjson-perl postgresql-server-dev-all")
                    install_oar_sched_cmd = """
                    mkdir -p /opt/oar_sched; \
                    cd /opt/oar_sched; \
                    git clone https://github.com/oar-team/oar3.git; \
                    cd oar3; \
                    git checkout dce942bebc2; \
                    pip3 install -e .; \
                    cd /usr/lib/oar/schedulers; \
                    ln -s /usr/local/bin/kamelot; \
                    pip3 install psycopg2
                    """
                    logger.info("installing OAR server node: {}".format(str(nodes[0])))
                    install_master = SshProcess(install_cmd + server_packages +
                                                ";" + install_oar_sched_cmd, nodes[0],
                                                connection_params={'user': 'root'})
                    install_master.run()
                    install_oar_nodes.wait()

                    if not install_master.ok:
                        Report(install_master)

                    configure_oar_cmd = """
                    sed -i \
                        -e 's/^\(DB_TYPE\)=.*/\\1="Pg"/' \
                        -e 's/^\(DB_HOSTNAME\)=.*/\\1="localhost"/' \
                        -e 's/^\(DB_PORT\)=.*/\\1="5432"/' \
                        -e 's/^\(DB_BASE_PASSWD\)=.*/\\1="oar"/' \
                        -e 's/^\(DB_BASE_LOGIN\)=.*/\\1="oar"/' \
                        -e 's/^\(DB_BASE_PASSWD_RO\)=.*/\\1="oar_ro"/' \
                        -e 's/^\(DB_BASE_LOGIN_RO\)=.*/\\1="oar_ro"/' \
                        -e 's/^\(SERVER_HOSTNAME\)=.*/\\1="localhost"/' \
                        -e 's/^\(SERVER_PORT\)=.*/\\1="16666"/' \
                        -e 's/^\(LOG_LEVEL\)\=\"2\"/\\1\=\"3\"/' \
                        -e 's#^\(LOG_FILE\)\=.*#\\1="{result_dir}/oar.log"#' \
                        -e 's/^\(JOB_RESOURCE_MANAGER_PROPERTY_DB_FIELD\=\"cpuset\".*\)/#\\1/' \
                        -e 's/^#\(CPUSET_PATH\=\"\/oar\".*\)/\\1/' \
                        -e 's/^\(FINAUD_FREQUENCY\)\=.*/\\1="0"/' \
                        /etc/oar/oar.conf
                    """.format(result_dir=self.result_dir)
                    configure_oar = Remote(configure_oar_cmd, nodes,
                                           connection_params={'user': 'root'})
                    configure_oar.run()
                    logger.info("OAR is configured on all nodes")

                    # Configure server
                    create_db = "oar-database --create --db-is-local"
                    config_oar_sched = ("oarnotify --remove-queue default;"
                                        "oarnotify --add-queue default,1,kamelot")
                    start_oar = "systemctl start oar-server.service"
                    logger.info(
                        "configuring OAR database: {}".format(str(nodes[0])))
                    config_master = SshProcess(create_db + ";" + config_oar_sched + ";" + start_oar,
                                               nodes[0],
                                               connection_params={'user': 'root'})
                    config_master.run()

                    # propagate SSH keys
                    logger.info("configuring OAR SSH")
                    oar_key = "/tmp/.ssh"
                    Process('rm -rf ' + oar_key).run()
                    Process('scp -o BatchMode=yes -o PasswordAuthentication=no '
                            '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
                            '-o ConnectTimeout=20 -rp -o User=root ' +
                            nodes[0].address + ":/var/lib/oar/.ssh"
                            ' ' + oar_key).run()
                    # Get(nodes[0], "/var/lib/oar/.ssh", [oar_key], connection_params={'user': 'root'}).run()
                    Put(nodes[1:], [oar_key], "/var/lib/oar/", connection_params={'user': 'root'}).run()
                    add_resources_cmd = """
                    oarproperty -a cpu || true; \
                    oarproperty -a core || true; \
                    oarproperty -c -a host || true; \
                    oarproperty -a mem || true; \
                    """
                    for node in nodes[1:]:
                        add_resources_cmd = add_resources_cmd + "oarnodesetting -a -h {node} -p host={node} -p cpu=1 -p core=4 -p cpuset=0 -p mem=16; \\\n".format(node=node.address)

                    add_resources = SshProcess(add_resources_cmd, nodes[0],
                                               connection_params={'user': 'root'})
                    add_resources.run()

                    if add_resources.ok:
                        logger.info("oar is now configured!")
                    else:
                        raise RuntimeError("error in the OAR configuration: Abort!")

                # TODO backup de la config de OAR

                # Do the replay
                logger.info('begining the replay')
                while len(self.sweeper.get_remaining()) > 0:
                    combi = self.sweeper.get_next()
                    workload_file = os.path.basename(combi['workload_filename'])
                    oar_replay = SshProcess(script_path + "/oar_replay.py " +
                                            combi['workload_filename'] + " " +
                                            self.result_dir + "  oar_gant_" +
                                            workload_file,
                                            nodes[0])
                    oar_replay.stdout_handlers.append(self.result_dir + '/' +
                                                      workload_file + '.out')
                    logger.info("replaying workload: {}".format(combi))
                    oar_replay.run()
                    if oar_replay.ok:
                        logger.info("Replay workload OK: {}".format(combi))
                        self.sweeper.done(combi)
                    else:
                        logger.info("Replay workload NOT OK: {}".format(combi))
                        self.sweeper.cancel(combi)
                        raise RuntimeError("error in the OAR replay: Abort!")

            except:
                traceback.print_exc()
                ipdb.set_trace()

            finally:
                if is_a_test:
                    ipdb.set_trace()
                if reservation_job_id is None:
                    logger.info("delete job: {}".format(jobs))
                    oardel(jobs)

if __name__ == "__main__":
    engine = oar_replay_workload()
    engine.start()

