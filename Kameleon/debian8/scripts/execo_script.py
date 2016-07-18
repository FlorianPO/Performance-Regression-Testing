#!/usr/bin/env python

import sys
import os
import time
# import ipdb
import traceback
from shutil import copy
from execo import Process, SshProcess, Remote, format_date, Put
from execo_g5k import oarsub, oardel, OarSubmission, get_oar_job_nodes, wait_oar_job_start
from execo_g5k.kadeploy import deploy, Deployment
from execo_engine import Engine, logger, ParamSweeper, sweep
from execo.report import Report

# defined in __main__
_site = None
_nbrNodes = None
_walltime = None
_properties = None

script_path = os.path.dirname(os.path.realpath(__file__))

class ExecoWorkload(Engine):
    def setup_result_dir(self):
        self.result_dir = script_path + '/' + 'results_' + time.strftime("%Y-%m-%d--%H-%M-%S")

    def checkProcess(self, process):
        if (not process.ok):
            logger.info("Error : {}".format(process.error_reason))
            logger.info("Spack stdout : {}".format(process.stdout))

    def prediction_callback(ts):
        logger.info("job start prediction = %s" % (format_date(ts),))

    def run(self):
        # Go to the result folder before everything
        os.chdir(self.result_dir)

        # OARSUB
        jobs = oarsub([(OarSubmission(resources='nodes=' + _nbrNodes.__str__(), 
                                      job_type='deploy', 
                                      walltime=_walltime, 
                                      sql_properties=_properties), _site)])
        
        job_id, site = jobs[0]
        try:
            # KADEPLOY
            logger.info("Waiting job start %s on %s" % (job_id, site))
            wait_oar_job_start(job_id, site, prediction_callback=prediction_callback)
            logger.info("getting nodes of %s on %s" % (job_id, site))
            nodes = get_oar_job_nodes(job_id, site)

            deployed, undeployed = deploy(Deployment(nodes, env_name=env_name),
                                          check_deployed_command=already_configured)
            if undeployed:
                logger.warn(
                    "NOT deployed nodes : {}".format(str(undeployed)))
                raise RuntimeError('Deployement failed')

            # STARPU INSTALLATION
            spack_spec = 'chameleon@trunk+starpu+fxt ^starpu@svn-trunk+fxt'
            spack_command = 'spack install -v' + ' ' + spack_spec 

            logger.info("Starting StarPU installation...")
            spack_process = Process(spack_command).start()
            spack_process.wait()

            logger.info("StarPU installation DONE...")
            self.checkProcess(spack_process)
            spack_process.kill()

            # STARPU DIRECTORY
            logger.info("Searching and going to StarPU installation directory...")

            starpu_location_process = Process(spack_spec).start()
            starpu_location_process.wait()
            self.checkProcess(starpu_location)

            starpu_cd_process = Process('cd ' + starpu_location_process.stdout + '/lib/chameleon').start()
            starpu_cd_process.wait()
            self.checkProcess(starpu_cd_process)

            starpu_location_process.kill()
            starpu_cd_process.kill()

            # RUNNING EXPERIMENT
            logger.info("Starting StarPU experiment...")
            starpu_experiment_process = Process(""" export STARPU_WORKER_STATS=1
                                                    export STARPU_CALIBRATE=2
                                                    ./timing/time_spotrf_tile --warmup --gpus=3 --threads=9 --nb=960 --ib=96 --n_range=48000:48000:9600 """)
            starpu_experiment_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU.out') # create output file for StarPU    
            starpu_experiment_process.start()
            starpu_experiment_process.wait()

            logger.info("StarPU experiment DONE...")
            self.checkProcess(starpu_experiment_process)        
            starpu_experiment_process.kill()

        finally:
	        logger.info("Delete job : {}".format(jobs))
            oardel(jobs)

if __name__ == "__main__":
    _site = 'grenoble'                   # (sys.argv)[1]
    _nbrNodes = 1                        # (sys.argv)[2]
    _walltime = '1:00:00'                # (sys.argv)[3]
    _properties = '\"gpu=\'YES\'\"'      # (sys.argv)[4]

    execo = ExecoWorkload()
    execo.start()

