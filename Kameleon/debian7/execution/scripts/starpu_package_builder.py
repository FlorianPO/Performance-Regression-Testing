#!/usr/bin/env python

import os
import sys
import csv

package_folder = 'starpu'

name_column = 0
branch_column = 3
revision_column = 4

result_file = None

def build_from_csv(name):
    f_csv = open(name, 'r')
    csv_reader = csv.reader(f_csv, delimiter=',')

    result_file.write('\n')
    for row in csv_reader:
        result_file.write("    version('%s', svn='%s', revision='%s')\n" % (row[name_column], row[branch_column], row[revision_column]))

if __name__ == "__main__":
    csv_file = (sys.argv)[1]
    spack_path = (sys.argv)[2]

    result_file = open(spack_path + '/var/spack/repos/builtin/packages/' + package_folder + '/package.py', 'a')
    build_from_csv(csv_file)
