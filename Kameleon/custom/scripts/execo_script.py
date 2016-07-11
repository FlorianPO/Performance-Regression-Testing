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
_jobID = None
_nbrNodes = None
_walltime = None

script_path = os.path.dirname(os.path.realpath(__file__))

class ExecoWorkload(Engine):
    def setup_result_dir(self):
        self.result_dir = script_path + '/' + 'results_' + time.strftime("%Y-%m-%d--%H-%M-%S")

    def checkProcess(self, process):
        if (not process.ok):
            logger.info("Error : {}".format(process.error_reason))
            logger.info("Spack stdout : {}".format(process.stdout))

    def run(self):
        # Go to the result folder before everything
        os.chdir(self.result_dir)

        # STARPU INSTALLATION
        spack_spec = 'chameleon@trunk+starpu+fxt ^starpu@svn-trunk+fxt'
        spack_command = 'spack install -v' + ' ' + spack_spec 
        
        logger.info("Starting StarPU installation...")
        spack_process = Process(spack_command).start()
        spack_process.wait()

        logger.info("StarPU installation DONE...")
        checkProcess(spack_process)
        spack_process.kill()

        # STARPU DIRECTORY
        logger.info("Searching and going to StarPU installation directory...")

        starpu_location_process = Process(spack_spec).start()
        starpu_location_process.wait()
        checkProcess(starpu_location)

        starpu_cd_process = Process('cd ' + starpu_location_process.stdout + '/lib/chameleon').start()
        starpu_cd_process.wait()
        checkProcess(starpu_cd_process)
        
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
        checkProcess(starpu_experiment_process)        
        starpu_experiment_process.kill()

if __name__ == "__main__":
    _site = (sys.argv)[1]
    _jobID = int((sys.argv)[2])
    _nbrNodes = int((sys.argv)[3])
    _walltime = (sys.argv)[4]

    execo = ExecoWorkload()
    execo.start()

