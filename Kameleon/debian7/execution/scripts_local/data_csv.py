#!/usr/bin/env python

import os
import subprocess
import sys
from csv_reader import CSVReader

if __name__ == "__main__":
    f_csv = open((sys.argv)[1], 'r')
    csv_reader = csv.reader(f_csv, delimiter=',')
    header = CSVHeader(csv_reader.next())
    
    starpu_directory = (sys.argv)[2]
    os.chdir(starpu_directory) # Go to starpu_results directory
    
    result_file = open('./data.csv', 'w')
    result_file.write('experiment_name' + ',' + 'GFlop/s' + '\n') # header of csv file

    while True:
        try:
            row = csv_reader.next()
            
            # Find directory
            directory_name = subprocess.Popen(['find', '-type', 'd', '-name', '*%s*%s*%s*' % \
                (row[header.name], row[header.chameleon_revision], row[header.starpu_revision])], stdout=subprocess.PIPE).communicate()[0]       
            directory_name = directory_name.replace("\n", "") # remove end of line

            # Go to directory
            os.chdir(directory_name)

            # Find file
            file_name = subprocess.Popen(['find', '-name', '*experiment*%s*' % row[header.name]], stdout=subprocess.PIPE).communicate()[0]
            file_name = file_name.replace("\n", "") # remove end of line
            
            # Get data
            cat = subprocess.Popen(['cat', file_name], stdout=subprocess.PIPE)
            tail = subprocess.Popen(['tail', '-n', '1'], stdin=cat.stdout, stdout=subprocess.PIPE)
            grep = subprocess.Popen(['grep', '-o', '-E', '[0-9]+.[0-9]+'], stdin=tail.stdout, stdout=subprocess.PIPE)
            sed = subprocess.Popen(['sed', '4q;d'], stdin=grep.stdout, stdout=subprocess.PIPE)
            sed = sed.communicate()[0].replace("\n", "") # remove end of line

            result_file.write(row[header.name] + ',' + sed + '\n')

            os.chdir('../') # Go to starpu_results directory

        except StopIteration:
            break;

    result_file.close()
