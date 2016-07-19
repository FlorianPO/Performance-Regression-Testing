#!/usr/bin/env python

import sys
import os
import time
# import ipdb
import traceback
from shutil import copy
from execo import Process, SshProcess, Remote, format_date, Put
from execo_g5k import oarsub, oardel, OarSubmission, get_oar_job_nodes, wait_oar_job_start
from execo_engine import Engine, logger, ParamSweeper, sweep
from execo.report import Report

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

        logger.info("Starting StarPU installation...")
        spack_process = Process('spack install -v' + ' ' + spack_spec)

        spack_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU_installation') # create output file for StarPU installation
        spack_process.start()
        spack_process.wait()

        logger.info("StarPU installation DONE...")
        self.checkProcess(spack_process)
        spack_process.kill()

        # STARPU DIRECTORY
        logger.info("Searching and going to StarPU installation directory...")

        starpu_location_process = Process('spack location -i' + ' ' + spack_spec).start()
        starpu_location_process.wait()
        self.checkProcess(starpu_location_process)
    
        starpu_path = starpu_location_process.stdout.replace("\n", "") # remove end_of_line
        starpu_cd = 'cd' + ' ' + starpu_path + '/lib/chameleon/'

        starpu_location_process.kill()
        
        # RUNNING EXPERIMENT
        logger.info("Starting StarPU experiment...")

        starpu_experiment = """export STARPU_WORKER_STATS=1
                               export STARPU_CALIBRATE=2
                               ./timing/time_spotrf_tile --warmup --gpus=3 --threads=9 --nb=960 --ib=96 --n_range=48000:48000:9600"""

        starpu_experiment_process = Process(starpu_cd + '\n' + starpu_experiment, shell=True)
                   
        starpu_experiment_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU_experiment') # create output file for StarPU execution
        starpu_experiment_process.start()
        starpu_experiment_process.wait()

        logger.info("StarPU experiment DONE...")
        self.checkProcess(starpu_experiment_process)        
        starpu_experiment_process.kill()

if __name__ == "__main__":
    execo = ExecoWorkload()
    execo.start()

