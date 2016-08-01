#!/usr/bin/env python

import os
import subprocess
import sys
import string

if __name__ == "__main__":
    starpu_directory = (sys.argv)[1]
    os.chdir(starpu_directory) # Go to starpu_results directory
    
    result_file = open('./data.csv', 'w')
    result_file.write('experiment_name' + ',' + 'GFlop/s' + '\n') # header of csv file

    directories = subprocess.Popen(['find', '-type', 'd'], stdout=subprocess.PIPE).communicate()[0]       
    directories = string.split(directories, '\n')
    del directories[0] # remove .
    del directories[-1] # remove ''

    for i in range(0, len(directories)):
        os.chdir(directories[i])

        # Find file
        file_name = subprocess.Popen(['find', '-name', '*.org'], stdout=subprocess.PIPE).communicate()[0]
        file_name = file_name.replace('\n', '') # remove end of line
        
        # Get data
        cat = subprocess.Popen(['cat', file_name], stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', '-E', "XP[0-9]+_Flops:"], stdin=cat.stdout, stdout=subprocess.PIPE)
        grep2 = subprocess.Popen(['grep', '-o', '-E', "[0-9]+.[0-9]+"], stdin=grep.stdout, stdout=subprocess.PIPE).communicate()[0]
        grep2 = string.split(grep2, '\n')
        del grep2[-1]

        for j in range(0, len(grep2)):
            xp_name = (directories[i]).replace('./', '')
            result_file.write(xp_name + ',' + grep2[j] + '\n')

        os.chdir('../') # Go to starpu_results directory

    result_file.close()
