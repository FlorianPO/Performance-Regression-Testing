#!/usr/bin/env python

import sys
import os
from csv_reader import RevisionsReader

from execo import Process
from execo_engine import Engine, logger

script_path = os.path.dirname(os.path.realpath(__file__))
csv_file = None
csv_file_abstract = None

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
        cvsr = RevisionsReader(csv_file) # Launch CSV reader
        cvsr_abstract = RevisionsReader(csv_file_abstract)

        os.chdir(self.result_dir) # Go to result directory before everything

        while True:
            try:
                cvsr.next()
                cvsr_abstract.next()

                logger.info("Starting experiment %s with Chameleon@%s and StarPU@%s..." % (cvsr.name(), cvsr.chameleonRevision(), cvsr.starpuRevision()))

                chameleon_name = cvsr_abstract.name() + '_' + cvsr_abstract.chameleonBranch() + '_' + cvsr_abstract.chameleonRevision() + '_' + cvsr_abstract.command()
                starpu_name = cvsr_abstract.name() + '_' + cvsr_abstract.starpuBranch() + '_' + cvsr_abstract.starpuRevision() + '_' + cvsr_abstract.command()
                global_name = cvsr_abstract.name() \
                                + '_chameleon_' + cvsr_abstract.chameleonBranch() + '_' + cvsr_abstract.chameleonRevision()
                                + '_starpu' + cvsr_abstract.starpuBranch() + '_' + cvsr_abstract.starpuRevision()
                                + '_cmd_' + cvsr_abstract.command()
                
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

                starpu_experiment_process = Process(starpu_cd + '\n' + cvsr.command(), shell=True)
                           
                starpu_experiment_process.stdout_handlers.append(folder + '/' + 'experiment_' + global_name) # create output file for StarPU execution
                starpu_experiment_process.stdout_handlers.append(folder + '/' + 'stderr_' + global_name) # create error file for StarPU execution
                starpu_experiment_process.start()
                starpu_experiment_process.wait()

                logger.info("StarPU experiment DONE...")
                is_ok = self.checkProcess(starpu_experiment_process)        
                starpu_experiment_process.kill()

                if (not is_ok):
                    continue # stop this experiment

            except StopIteration:
                break;
            
if __name__ == "__main__":
    csv_file = (sys.argv)[1]
    csv_file_abstract = (sys.argv)[2]

    execo = ExecoWorkload()
    execo.start()

