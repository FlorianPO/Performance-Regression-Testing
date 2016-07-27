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
            return False
        return True

    def run(self):
        f_csv = open(csv_file, 'r')
        csv_reader = csv.reader(f_csv, delimiter=',')
        header = CSVHeader(csv_reader.next())

        os.chdir(self.result_dir) # Go to result directory before everything

        while True:
            try:
                row = csv_reader.next()
                
                logger.info("Starting experiment %s with Chameleon@%s and StarPU@%s..." % (row[header.name], row[header.chameleon_revision], row[header.starpu_revision]))

                chameleon_name = row[header.name] + '_' + row[header.chameleon_revision]
                starpu_name = row[header.name] + '_' + row[header.starpu_revision]
                global_name = row[header.name] + '_c' + row[header.chameleon_revision] + '_s' + row[header.starpu_revision] 
                
                spack_spec = 'chameleon@' + chameleon_name + ' +starpu+fxt ^starpu@' + starpu_name + ' +fxt'

                # FOLDER CREATION
                folder = self.result_dir + '/' + global_name
                os.mkdir(folder, 0764)

                # STARPU INSTALLATION
                logger.info("Starting StarPU installation...")
                spack_process = Process('spack install -v' + ' ' + spack_spec)

                spack_process.stdout_handlers.append(folder + '/' + 'install_' + global_name) # create output file for StarPU installation
                spack_process.start()
                spack_process.wait()

                logger.info("StarPU installation DONE...")
                is_ok = self.checkProcess(spack_process)
                spack_process.kill()

                if (not is_ok):
                    continue # stop this experiment

                # STARPU DIRECTORY
                logger.info("Searching and going to StarPU installation directory...")

                starpu_location_process = Process('spack location -i' + ' ' + spack_spec).start()
                starpu_location_process.wait()
                is_ok = self.checkProcess(starpu_location_process)
            
                starpu_path = starpu_location_process.stdout.replace("\n", "") # remove end_of_line
                starpu_cd = 'cd' + ' ' + starpu_path + '/lib/chameleon/'
                starpu_location_process.kill()

                if (not is_ok):
                    continue # stop this experiment
                
                # RUNNING EXPERIMENT
                logger.info("Starting StarPU experiment...")

                starpu_experiment = """export STARPU_WORKER_STATS=1
                                       export STARPU_CALIBRATE=2
                                       ./timing/time_spotrf_tile --warmup --gpus=3 --threads=9 --nb=960 --ib=96 --n_range=48000:48000:9600"""

                starpu_experiment_process = Process(starpu_cd + '\n' + starpu_experiment, shell=True)
                           
                starpu_experiment_process.stdout_handlers.append(folder + '/' + 'experiment_' + global_name) # create output file for StarPU execution
                starpu_experiment_process.start()
                starpu_experiment_process.wait()

                logger.info("StarPU experiment DONE...")
                is_ok = self.checkProcess(starpu_experiment_process)        
                starpu_experiment_process.kill()

                if (not is_ok):
                    continue # stop this experiment

            except StopIteration:
                break;

        f_csv.close();
            
if __name__ == "__main__":
    csv_file = (sys.argv)[1]

    execo = ExecoWorkload()
    execo.start()

