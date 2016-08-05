#!/usr/bin/env python

import os
import sys
from csv_reader import RevisionsReader
from subprocess import call

package_folder = 'chameleon'
result_file = None

def build_from_csv(cvs_name, csv_name_abstract):
    csvr = RevisionsReader(cvs_name) # Launch CVS reader
    csvr_abstract = RevisionsReader(csv_name_abstract)

    result_file.write('\n')
    while True:
        try:
            csvr.next()
            csvr_abstract.next()
            name = csvr_abstract.name() + '_' + csvr_abstract.chameleonBranch() + '_' + csvr_abstract.chameleonRevision() + '_' + csvr_abstract.command()
            result_file.write("    version('%s', svn='%s', revision=%s)\n" % (name, csvr.chameleonBranch(), csvr.chameleonRevision()))
        except StopIteration:
            break;

if __name__ == "__main__":
    path = (sys.argv)[3] + '/var/spack/repos/builtin/packages/' + package_folder + '/'

    # REMOVE PARALLEL COMPILATION
    with open(path + "tmp.py", "w") as outfile:
        call(["cat", path + "package.py"], stdout=outfile)
    with open(path + "package.py", "w") as outfile:
        call(["sed", '/make("install"/c\ \ \ \ \ \ \ \ \ \ \ \ make("install", parallel=False)', path + "tmp.py"], stdout=outfile)    
    call(['rm', path + "tmp.py"])

    result_file = open(path + 'package.py', 'a')
    build_from_csv((sys.argv)[1], (sys.argv)[2])
    result_file.close()
