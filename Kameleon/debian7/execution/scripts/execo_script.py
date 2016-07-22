#!/usr/bin/env python

import sys
import os
import csv
from csv_header import CSVHeader

from execo import Process
from execo_engine import Engine, logger

script_path = os.path.dirname(os.path.realpath(__file__))
csv_file = None

class ExecoWorkload(Engine):
    def setup_result_dir(self):
        self.result_dir = script_path + '/starpu_results'

    def checkProcess(self, process):
        if (not process.ok):
            logger.info("Error : {}".format(process.error_reason))
            logger.info("Spack stdout : {}".format(process.stdout))

    def run(self):
        f_csv = open(csv_file, 'r')
        csv_reader = csv.reader(f_csv, delimiter=',')
        header = CSVHeader(csv_reader.next())

        # Go to the result folder before everything
        os.chdir(self.result_dir)
    
        while True:
            try:
                row = csv_reader.next()
                
                logger.info("Starting experiment %s with Chameleon@%s and StarPU@%s..." % (row[header.name], row[header.chameleon_revision], row[header.starpu_revision]))

                # STARPU INSTALLATION
                spack_spec = 'chameleon@' + row[header.name] + '+starpu+fxt ^starpu@' + row[header.name] + '+fxt'

                logger.info("Starting StarPU installation...")
                spack_process = Process('spack install -v' + ' ' + spack_spec)

                spack_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU_installation_' + row[header.name]) # create output file for StarPU installation
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
                           
                starpu_experiment_process.stdout_handlers.append(self.result_dir + '/' + 'StarPU_experiment_' + row[header.name]) # create output file for StarPU execution
                starpu_experiment_process.start()
                starpu_experiment_process.wait()

                logger.info("StarPU experiment DONE...")
                self.checkProcess(starpu_experiment_process)        
                starpu_experiment_process.kill()

            except StopIteration:
                break;
            
if __name__ == "__main__":
    csv_file = (sys.argv)[1]

    execo = ExecoWorkload()
    execo.start()

