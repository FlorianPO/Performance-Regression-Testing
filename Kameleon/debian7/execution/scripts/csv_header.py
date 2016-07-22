#!/usr/bin/env python

class CSVHeader:
    ### Define your csv header here
    experiment_name = 'experiment_name'
    chameleon_branch = 'chameleon_branch'
    chameleon_revision = 'chameleon_revision'
    starpu_branch = 'starpu_branch'
    starpu_revision = 'starpu_revision' 
    #

    def __init__(self, header_row):
        ### You can retrieve these
        self.name = None
        self.chameleon_branch = None
        self.chameleon_revision = None
        self.starpu_branch = None
        self.starpu_revision = None        
        #

        index = 0
        for token in header_row:
            if token == CSVHeader.experiment_name:
                self.name = index;
            elif token == CSVHeader.chameleon_branch:
                self.chameleon_branch = index;
            elif token == CSVHeader.chameleon_revision:
                self.chameleon_revision = index
            elif token == CSVHeader.starpu_branch:
                self.starpu_branch = index;
            elif token == CSVHeader.starpu_revision:
                self.starpu_revision = index
            index += 1
