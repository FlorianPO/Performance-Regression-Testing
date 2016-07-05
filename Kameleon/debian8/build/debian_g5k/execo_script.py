#!/usr/bin/env python

import sys
import os
import time
# import ipdb
import traceback
from shutil import copy
from execo import Process, SshProcess, Remote, format_date, Put
from execo_g5k import oarsub, oardel, OarSubmission, get_oar_job_nodes, wait_oar_job_start
from execo_g5k.kadeploy import deploy, Deployment
from execo_engine import Engine, logger, ParamSweeper, sweep
from execo.report import Report

# defined in __main__
_site = None
_jobID = None
_nbrNodes = None
_walltime = None

script_path = os.path.dirname(os.path.realpath(__file__))

class ExecoWorkload(Engine):
    def setup_result_dir(self):
        self.result_dir = script_path + '/' + 'results_' + time.strftime("%Y-%m-%d--%H-%M-%S")

    def run(self):
        # Go to the result folder before everything
        # os.chdir(self.result_dir)

        jobs = [(_jobID, _site)]
        # Get nodes
        nodes = get_oar_job_nodes(_jobID, _site)

        try:
            # logger.info("Creating hostfiles for all combinations...")
            # for nbr_node in _nbrNodes:
            #     hostfile_filename = self.result_dir + '/' + 'hostfile-' + nbr_node
            #     with open(hostfile_filename, 'w') as hostfile:
            #         for node in nodes[:int(nbr_node)]:
            #             print>>hostfile, node.address
            spack_command = 'spack install -v chameleon@trunk+starpu+fxt ^starpu@svn-trunk+fxt'

            logger.info("Starting StarPU installation...")
            spack_process = Process(spack_command).start()

            spack_process.wait()
            logger.info("StarPU installation DONE...")
            if (not spack_process.ok):
                logger.info("Error : {}".format(spack_process.error_reason))
                logger.info("Spack stdout : {}".format(spack_process.stdout));

            spack_process.kill()

            # Pilotage

        finally:
            logger.info("Delete job: {}".format(jobs))
            oardel(jobs)

if __name__ == "__main__":
    _site = (sys.argv)[1]
    _jobID = int((sys.argv)[2])
    _nbrNodes = int((sys.argv)[3])
    _walltime = (sys.argv)[4]

    execo = ExecoWorkload()
    execo.start()

