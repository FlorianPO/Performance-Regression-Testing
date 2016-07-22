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

    while True:
        try:
            row = csv_reader.next()

            file_name = subprocess.Popen(['find', '-name', '*experiment*%s' % row[header.name]], stdout=subprocess.PIPE).communicate()[0]
            file_name = file_name.replace("\n", "") # remove end of line

            f = open(file_name, 'r')
        
            # Get data
            # TODO

        except StopIteration:
            break;
