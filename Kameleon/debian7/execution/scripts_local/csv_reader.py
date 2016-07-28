#!/usr/bin/env python

import csv

class RevisionsReader:
    ### Define your csv header here
    _name = 'experiment_name'
    _chameleon_branch = 'chameleon_branch'
    _chameleon_revision = 'chameleon_revision'
    _starpu_branch = 'starpu_branch'
    _starpu_revision = 'starpu_revision'
    _command = 'command'
    #

    ### NAME ###
    def name(self):
        return self.row[self.i_name]
    
    ### BRANCHES ###
    def chameleonBranch(self):
        return self.row[self.i_chameleon_branch]

    def starpuBranch(self):
        return self.row[self.i_starpu_branch]

    ### REVISIONS ###
    def chameleonRevision(self):
        return self.row[self.i_chameleon_revision]

    def starpuRevision(self):
        return self.row[self.i_starpu_revision]

    ### COMMAND ###
    def command(self):
        return self.row[self.i_command]

    # NEXT
    def next(self): # except StopIteration
        self.row = self.csv_reader.next()

    def __init__(self, csv_file):
        self.f_csv = open(csv_file, 'r')
        self.csv_reader = csv.reader(self.f_csv, delimiter=',')

        self.i_name = None
        self.i_chameleon_branch = None
        self.i_chameleon_revision = None
        self.i_starpu_branch = None
        self.i_starpu_revision = None
        self.i_command = None

        self.row = self.csv_reader.next()

        index = 0
        for token in self.row:
            if token == RevisionsReader._name:
                self.i_name = index;
            elif token == RevisionsReader._chameleon_branch:
                self.i_chameleon_branch = index;
            elif token == RevisionsReader._chameleon_revision:
                self.i_chameleon_revision = index
            elif token == RevisionsReader._starpu_branch:
                self.i_starpu_branch = index;
            elif token == RevisionsReader._starpu_revision:
                self.i_starpu_revision = index
            elif token == RevisionsReader._command:
                self.i_command = index

            index += 1

class CommandsReader:
    ### Define your csv header here
    _command_name = 'command_name'
    _command = 'command'
    #

    ### NAME ###
    def commandName(self):
        return self.row[self.i_command_name]
    
    ### COMMAND ###
    def command(self):
        return self.row[self.i_command]

    # NEXT
    def next(self): # except StopIteration
        self.row = self.csv_reader.next()

    def __init__(self, csv_file):
        self.f_csv = open(csv_file, 'r')
        self.csv_reader = csv.reader(self.f_csv, delimiter=',')

        self.i_command_name = None
        self.i_command = None

        self.row = self.csv_reader.next()

        index = 0
        for token in self.row:
            if token == CommandsReader._command_name:
                self.i_command_name = index;
            elif token == CommandsReader._command:
                self.i_command = index

            index += 1

class BranchesReader:
    ### Define your csv header here
    _chameleon_name = 'chameleon_branch_name'
    _chameleon = 'chameleon_branch'
    _starpu_name = 'starpu_branch_name'
    _starpu = 'starpu_branch'
    #

    ### NAMES ###
    def chameleonName(self):
        return self.row[self.i_chameleon_name]

    def starpuName(self):
        return self.row[self.i_starpu_name]
    
    ### BRANCHES ###
    def chameleon(self):
        return self.row[self.i_chameleon]

    def starpu(self):
        return self.row[self.i_starpu]

    # NEXT
    def next(self): # except StopIteration
        self.row = self.csv_reader.next()

    def __init__(self, csv_file):
        self.f_csv = open(csv_file, 'r')
        self.csv_reader = csv.reader(self.f_csv, delimiter=',')

        self.i_chameleon_name = None
        self.i_chameleon = None
        self.i_starpu_name = None
        self.i_starpu = None
        
        self.row = self.csv_reader.next()

        index = 0
        for token in self.row:
            if token == BranchesReader._chameleon_name:
                self.i_chameleon_name = index;
            elif token == BranchesReader._chameleon:
                self.i_chameleon = index;
            elif token == BranchesReader._starpu_name:
                self.i_starpu_name = index;
            elif token == BranchesReader._starpu:
                self.i_starpu = index

            index += 1
