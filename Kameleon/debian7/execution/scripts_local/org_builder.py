#!/usr/bin/env python

import os
import subprocess
import sys
import string
import time
from csv_reader import RevisionsReader

if __name__ == "__main__":
    csvr = RevisionsReader((sys.argv)[1])
    csvr_abstract = RevisionsReader((sys.argv)[2])

    # Retrieve machine name
    machine_name = subprocess.Popen(['cat', 'g5k_machine'], stdout=subprocess.PIPE).communicate()[0]
    machine_name = machine_name.replace('\n', '')    

    # Go to starpu_results directory
    starpu_directory = (sys.argv)[3]
    os.chdir(starpu_directory)
 
    while True:
        try:
            csvr.next()
            csvr_abstract.next()
            
            # Find directory
            directory_name = subprocess.Popen(['find', '-type', 'd', '-name', '*%s*%s*%s*' % \
                (csvr.name(), csvr.chameleonRevision(), csvr.starpuRevision())], stdout=subprocess.PIPE).communicate()[0]       
            directory_name = directory_name.replace("\n", "") # remove end of line

            os.chdir(directory_name) # go to experiment directory

            # Create org file
            result_file_name = directory_name + '.org'    
            result_file_name = result_file_name.replace('./', '')    
            result_file = open(result_file_name, 'w')

            # HEAD
            result_file.write('#+TITLE: Experiment results' + '\n')
            result_file.write('#+DATE: %s %s' % (time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")) + '\n')
            result_file.write('#+AUTHOR: root' + '\n')
            result_file.write('#+MACHINE: %s' % (machine_name) + '\n')
            result_file.write('#+FILE: %s' % (result_file_name) + '\n') 
            result_file.write('\n') # empty line

            # HOST INFORMATION
            result_file.write('* Host information' + '\n')
            result_file.write('[[file:../node_info.org]]' + '\n')
            
            # SOFTWARE REVISIONS
            result_file.write('* Software revisions' + '\n')
            ## CHAMELEON
            result_file.write('** Chameleon' + '\n')   
            result_file.write('#+BEGIN_EXAMPLE' + '\n')
            result_file.write('chameleon_rev: %s' % (csvr.chameleonRevision()) + '\n')
            result_file.write('chameleon_bch: %s' % (csvr.chameleonBranch()) + '\n')
            result_file.write('#+END_EXAMPLE' + '\n')
            ## STARPU
            result_file.write('** StarPU' + '\n')
            result_file.write('#+BEGIN_EXAMPLE' + '\n')
            result_file.write('starpu_rev: %s' % (csvr.starpuRevision()) + '\n')
            result_file.write('starpu_bch: %s' % (csvr.starpuBranch()) + '\n')
            result_file.write('#+END_EXAMPLE' + '\n')

            # COMPILATION
            result_file.write('* Compilation' + '\n')
            file_name = subprocess.Popen(['find', '-name', '*install*'], stdout=subprocess.PIPE).communicate()[0]
            file_name = file_name.replace("\n", "") # remove end of line
            result_file.write('[[file:%s]]' % (file_name) + '\n')

            # EXPERIMENT RESULTS
            result_file.write('* Experimental results' + '\n')
            experiments = subprocess.Popen(['find', '-name', '*experiment*'], stdout=subprocess.PIPE).communicate()[0]
            experiments = string.split(experiments, '\n')
            del experiments[-1] # erase ''
            
            for i in range(0, len(experiments)):
                result_file.write('** XP%s' % (i+1) + '\n')
                # COMMAND
                result_file.write('*** Command' + '\n')
                result_file.write('#+begin_src sh :results output :exports both' + '\n')
                result_file.write(csvr.command() + '\n')
                result_file.write('#+end_src' + '\n')

                # STANDARD OUTPUT
                result_file.write('*** Standard output' + '\n')
                result_file.write('#+BEGIN_EXAMPLE' + '\n')
                starpu_result = subprocess.Popen(['cat', experiments[i]], stdout=subprocess.PIPE).communicate()[0]
                result_file.write(starpu_result + '\n')
                result_file.write('#+END_EXAMPLE' + '\n')

                # STANDARD ERROR
                result_file.write('*** Standard error' + '\n')
                # TODO

                # RESULT
                result_file.write('*** Result' + '\n')

                cat = subprocess.Popen(['cat', experiments[i]], stdout=subprocess.PIPE)
                tail = subprocess.Popen(['tail', '-n', '1'], stdin=cat.stdout, stdout=subprocess.PIPE)            
                grep = subprocess.Popen(['grep', '-o', '-E', '[0-9]+.[0-9]+'], stdin=tail.stdout, stdout=subprocess.PIPE)
                sed = subprocess.Popen(['sed', '4q;d'], stdin=grep.stdout, stdout=subprocess.PIPE)
                sed = sed.communicate()[0].replace("\n", "") # remove end of line

                result_file.write('#+BEGIN_EXAMPLE' + '\n')
                result_file.write('XP%s_Flops: %s' % ((i+1), sed) + '\n')
                result_file.write('#+END_EXAMPLE' + '\n')

            result_file.close()
            os.chdir('../') # Go to starpu_results directory

        except StopIteration:
            break;

