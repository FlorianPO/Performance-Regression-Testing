#!/usr/bin/env python

import os
import sys
from csv_reader import RevisionsReader

package_folder = 'starpu'
result_file = None

def build_from_csv(cvs_name, csv_name_abstract):
    cvsr = RevisionsReader(cvs_name) # Launch CVS reader
    cvsr_abstract = RevisionsReader(cvs_name_abstract)

    result_file.write('\n')
    while True:
        try:
            csv_reader.next()
            cvsr_abstract.next()
            name = cvsr_abstract.name() + '_' + cvsr_abstract.starpuBranch() + '_' + cvsr_abstract.starpuRevision() + '_' + cvsr_abstract.command()
            result_file.write("    version('%s', svn='%s', revision=%s)\n" % (name, cvsr.starpuBranch(), cvsr.starpuRevision()))
        except StopIteration:
            break;

if __name__ == "__main__":
    result_file = open((sys.argv)[3] + '/var/spack/repos/builtin/packages/' + package_folder + '/package.py', 'a')
    build_from_csv((sys.argv)[1], (sys.argv)[2])
    result_file.close()
