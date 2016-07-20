#!/usr/bin/env python

import sys
import os
import time
import csv
# import ipdb
import traceback
from shutil import copy
from execo import Process, SshProcess, Remote, format_date, Put
from execo_g5k import oarsub, oardel, OarSubmission, get_oar_job_nodes, wait_oar_job_start
from execo_engine import Engine, logger, ParamSweeper, sweep
from execo.report import Report

script_path = os.path.dirname(os.path.realpath(__file__))
csv_file = None

class ExecoWorkload(Engine):
    def setup_result_dir(self):
        self.result_dir = script_path + '/results_execo'

    def checkProcess(self, process):
        if (not process.ok):
            logger.info("Error : {}".format(process.error_reason))
            logger.info("Spack stdout : {}".format(process.stdout))

    def run(self):
        f_csv = open(csv_file, 'r')
        csv_reader = csv.reader(f_csv, delimiter=',')

        # Go to the result folder before everything
        os.chdir(self.result_dir)
    
        for row in csv_reader:
            logger.info("Starting experiment %s with Chameleon@%s and StarPU@%s..." % (row[0], row[2], row[4]))

            # STARPU INSTALLATION
            spack_spec = 'chameleon@' + row[0] + '+starpu+fxt ^starpu@' + row[0] + '+fxt'

            logger.info("Starting StarPU installation...")
            spack_process = Process('spack install -v' + ' ' + spack_spec)

            spack_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU_installation_' + row[0]) # create output file for StarPU installation
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
                       
            starpu_experiment_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU_experiment_' + row[0]) # create output file for StarPU execution
            starpu_experiment_process.start()
            starpu_experiment_process.wait()

            logger.info("StarPU experiment DONE...")
            self.checkProcess(starpu_experiment_process)        
            starpu_experiment_process.kill()

if __name__ == "__main__":
    csv_file = (sys.argv)[1]

    execo = ExecoWorkload()
    execo.start()

