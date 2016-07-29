#!/usr/bin/env python

import errno
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
        csvr = RevisionsReader(csv_file) # Launch CSV reader
        csvr_abstract = RevisionsReader(csv_file_abstract)

        os.chdir(self.result_dir) # Go to result directory before everything

        while True:
            try:
                csvr.next()
                csvr_abstract.next()

                chameleon_name = csvr_abstract.name() + '_' + csvr_abstract.chameleonBranch() + '_' + csvr_abstract.chameleonRevision() + '_' + csvr_abstract.command()
                starpu_name = csvr_abstract.name() + '_' + csvr_abstract.starpuBranch() + '_' + csvr_abstract.starpuRevision() + '_' + csvr_abstract.command()
                global_name = csvr_abstract.name() \
                                + '_chameleon_' + csvr_abstract.chameleonBranch() + '_' + csvr_abstract.chameleonRevision() \
                                + '_starpu_' + csvr_abstract.starpuBranch() + '_' + csvr_abstract.starpuRevision() \
                                + '_' + csvr_abstract.command()
                
                logger.info("Starting experiment %s ..." % (global_name))

                spack_spec = 'chameleon@' + chameleon_name + ' +starpu+fxt ^starpu@' + starpu_name + ' +fxt'

                # FOLDER CREATION
                folder_name = 'chameleon_' + csvr_abstract.chameleonBranch() + '_' + csvr_abstract.chameleonRevision() \
                                + '_starpu_' + csvr_abstract.starpuBranch() + '_' + csvr_abstract.starpuRevision()
                folder = self.result_dir + '/' + folder_name

                try:
                    os.mkdir(folder, 0764)
                except OSError as exc:
                    if (exc.errno != errno.EEXIST):
                        raise exc
                    pass

                # STARPU INSTALLATION
                logger.info("Starting StarPU installation...")
                spack_process = Process('spack install -v' + ' ' + spack_spec)


                if (not os.path.isfile(folder + '/' + 'compil_' + folder_name)):
                    spack_process.stdout_handlers.append(folder + '/' + 'compil_' + folder_name) # create output file for StarPU installation
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

                starpu_experiment_process = Process(starpu_cd + '\n' + csvr.command(), shell=True)
                           
                starpu_experiment_process.stdout_handlers.append(folder + '/' + 'stdout_' + global_name) # create output file for StarPU execution
                starpu_experiment_process.stderr_handlers.append(folder + '/' + 'stderr_' + global_name) # create error file for StarPU execution
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

