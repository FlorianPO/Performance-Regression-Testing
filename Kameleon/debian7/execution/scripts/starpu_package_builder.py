#!/usr/bin/env python

import os
import sys
from csv_reader import RevisionsReader

package_folder = 'starpu'
result_file = None

def build_from_csv(cvs_name, csv_name_abstract):
    csvr = RevisionsReader(cvs_name) # Launch CVS reader
    csvr_abstract = RevisionsReader(csv_name_abstract)

    result_file.write('\n')
    while True:
        try:
            csvr.next()
            csvr_abstract.next()
            name = csvr_abstract.name() + '_' + csvr_abstract.starpuBranch() + '_' + csvr_abstract.starpuRevision() + '_' + csvr_abstract.command()
            result_file.write("    version('%s', svn='%s', revision=%s)\n" % (name, csvr.starpuBranch(), csvr.starpuRevision()))
        except StopIteration:
            break;

if __name__ == "__main__":
    result_file = open((sys.argv)[3] + '/var/spack/repos/builtin/packages/' + package_folder + '/package.py', 'a')
    build_from_csv((sys.argv)[1], (sys.argv)[2])
    result_file.close()
