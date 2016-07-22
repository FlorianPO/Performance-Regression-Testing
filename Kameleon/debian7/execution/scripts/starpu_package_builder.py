#!/usr/bin/env python

import os
import sys
import csv
from csv_header import CSVHeader

package_folder = 'starpu'
result_file = None

def build_from_csv(name):
    f_csv = open(name, 'r')
    csv_reader = csv.reader(f_csv, delimiter=',')
    header = CSVHeader(csv_reader.next())

    result_file.write('\n')
    while True:
        try:
            row = csv_reader.next()
            result_file.write("    version('%s', svn='%s', revision='%s')\n" % (row[header.name], row[header.starpu_branch], row[header.starpu_revision]))
        except StopIteration:
            break;

if __name__ == "__main__":
    csv_file = (sys.argv)[1]
    spack_path = (sys.argv)[2]

    result_file = open(spack_path + '/var/spack/repos/builtin/packages/' + package_folder + '/package.py', 'a')
    build_from_csv(csv_file)
