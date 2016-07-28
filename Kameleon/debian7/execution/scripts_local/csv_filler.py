#!/usr/bin/env python

import os
import subprocess
import sys
import string
from csv_reader import *

script_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    revisions_file = (sys.argv)[1]
    commands_file = (sys.argv)[2]
    branches_file = (sys.argv)[3]

    rev_reader = RevisionsReader(revisions_file)
    cmd_reader = CommandsReader(commands_file)
    bch_reader = BranchesReader(branches_file)

    # COMMANDS
    hash_cmd = {}
    while True:
        try:
            cmd_reader.next()
            hash_cmd[cmd_reader.commandName()] = cmd_reader.command()
        except StopIteration:
            break

    # BRANCHES
    hash_chameleon_bch = {}
    hash_starpu_bch = {}
    while True:
        try:
            bch_reader.next()
            hash_chameleon_bch[bch_reader.chameleonName()] = bch_reader.chameleon()
            hash_starpu_bch[bch_reader.starpuName()] = bch_reader.starpu()
        except StopIteration:
            break

    # BEGINNING OF WRITTING
    result_file = open(script_path + '/../scripts/revisions.csv', 'w')

    # HEADER
    result_file.write('%s,%s,%s,%s,%s,%s' % (rev_reader.name(), rev_reader.chameleonBranch(), rev_reader.chameleonRevision(), \
                                             rev_reader.starpuBranch(), rev_reader.starpuRevision(), rev_reader.command()) + '\n')

    while True:
        try:
            rev_reader.next()
            result_file.write('%s,%s,%s,%s,%s,"%s"' % (rev_reader.name(), hash_chameleon_bch[rev_reader.chameleonBranch()], rev_reader.chameleonRevision(), \
                                                     hash_starpu_bch[rev_reader.starpuBranch()], rev_reader.starpuRevision(), hash_cmd[rev_reader.command()]) + '\n')
        except StopIteration:
            break

    result_file.close()
