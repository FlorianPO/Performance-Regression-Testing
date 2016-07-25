#!/usr/bin/env python

import os
import subprocess
import sys
import csv
from csv_header import CSVHeader

if __name__ == "__main__":
    f_csv = open((sys.argv)[1], 'r')
    csv_reader = csv.reader(f_csv, delimiter=',')
    header = CSVHeader(csv_reader.next())
    
    os.chdir((sys.argv)[2]) # Go to starpu_results directory
    result_file = open('./data.csv', 'w')

    result_file.write('experiment_name' + ',' + 'GFlop/s' + '\n') # header of csv file

    while True:
        try:
            row = csv_reader.next()

            file_name = subprocess.Popen(['find', '-name', '*experiment*%s' % row[header.name]], stdout=subprocess.PIPE).communicate()[0]
            file_name = file_name.replace("\n", "") # remove end of line

            cat = subprocess.Popen(['cat', file_name], stdout=subprocess.PIPE)
            tail = subprocess.Popen(['tail', '-n', '1'], stdin=cat.stdout, stdout=subprocess.PIPE)
            grep = subprocess.Popen(['grep', '-o', '-E', '[0-9]+.[0-9]+'], stdin=tail.stdout, stdout=subprocess.PIPE)
            sed = subprocess.Popen(['sed', '4q;d'], stdin=grep.stdout, stdout=subprocess.PIPE)
            sed = sed.communicate()[0].replace("\n", "") # remove end of line

            result_file.write(row[header.name] + ',' + sed + '\n')

        except StopIteration:
            break;

    result_file.close()
