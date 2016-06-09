#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys
import glob
import shlex
import shutil
import datetime
import time
import random
from subprocess import check_call, check_output, CalledProcessError
import socket

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import logging

log = logging.getLogger(__name__)


class BuildCtbExplorerRunner(object):
    def __init__(self, args=None):
        """
        Initializes an object to run CtbRunner in Galaxy.
        """
        # Check whether the options are specified and saves them into the object
        self.args = args
        self.outputdir1 = args.outputdir1
        self.outputdir2 = args.outputdir2
        self.input_file1 = args.input_file1
        self.input_file2 = args.input_file2

    def build_ctb_explorer(self):
        """
        :rtype: boolean
        """
        self.copy_output_file_to_dataset(self.outputdir1, self.input_file1)
        self.copy_output_file_to_dataset(self.outputdir2, self.input_file2)
        return True

    def copy_output_file_to_dataset(self, dir, input_dir):
        """
        Retrieves the output files from the gx working directory and copy them to the Galaxy output directory
        """
        result_file = glob.glob(input_dir + '/*')
        for file_name in result_file:
            if os.path.isfile(file_name):
                shutil.copy2(file_name, dir)
            elif os.path.isdir(file_name):
                # create the parent dir before copytree
                os.chdir(dir)
                shutil.copytree(file_name, file_name.rsplit('/', 1)[-1])


def main():
    parser = argparse.ArgumentParser(description="Tool used to build a combat-tb explorer dataset")
    parser.add_argument('--outputdir1')
    parser.add_argument('--outputdir2')
    parser.add_argument('--input_file1')
    parser.add_argument('--input_file2')
    args = parser.parse_args()

    ctb_explorer_runner = BuildCtbExplorerRunner(args)

    # make the output directory (neo4j)
    if not os.path.exists(args.outputdir1):
        os.makedirs(args.outputdir1)

    # make the output directory (jbrowser)
    if not os.path.exists(args.outputdir2):
        os.makedirs(args.outputdir2)

    status = ctb_explorer_runner.build_ctb_explorer()

    if status is None:
        exit(1)

if __name__ == "__main__": main()
