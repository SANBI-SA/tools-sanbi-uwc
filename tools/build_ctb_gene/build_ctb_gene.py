#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys
import glob
import shlex
import shutil
from subprocess import check_call, CalledProcessError

import logging

log = logging.getLogger(__name__)


class BuildCtbRunner(object):

    def __init__(self, args=None):
        '''
        Initializes an object to run CtbRunner in Galaxy.
        '''

        # Check whether the options are specified and saves them into the object
        #assert args != None
        self.args = args

    def build_ctb_gene(self, output_file1, output_dir, input_file, mount_point):
        #cmdline_str = "build_ctb_gene goterms ${}".format(input_file)
        #cmdline_str = "build_ctb_gene goterms --help"
        cmdline_str = "touch /tmp/foo.bar"
        build_ctb = False
        cmdline_str = self.newSplit(cmdline_str)
        try:
            check_call(cmdline_str)
            #build_ctb = True
        except CalledProcessError:
            print("Error running the build_ctb_gene gotermS", file=sys.stderr)

        self.copy_output_file_to_dataset()
        self.args.output_file1 = self.args.outputdir

    def newSplit(self, value):
        lex = shlex.shlex(value)
        lex.quotes = '"'
        lex.whitespace_split = True
        lex.commenters = ''
        return list(lex)

    def copy_output_file_to_dataset(self):
        '''
        Retrieves the output files from the output directory and copies them to the Galaxy output files
        '''

        # retrieve neo4j files to the working gx directory
        result_file = glob.glob(self.args.mount_point + '/*')
        for file_name in result_file:
            shutil.copy(file_name, self.args.outputdir)

        #with open(result_file[0], 'rb') as fsrc:
            #with open(self.args.outputdir, 'wb') as fdest:
            #shutil.copy(fsrc, self.args.outputdir)


def main():
    parser = argparse.ArgumentParser(description="Tool used to extract data about genes using locus_tags")
    parser.add_argument('output_file1')
    parser.add_argument('--outputdir')
    parser.add_argument('--input_file')
    parser.add_argument('--mount_point')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--url')
    parser.add_argument('--port')
    args = parser.parse_args()

    export_cmd = "export NEO4J_REST_URL=http://${args.username}:${args.password}@${args.url}:${args.port}/db/data/"
    try:
        os.system(export_cmd)
    except:
        log.debug("Error exporting the NEO4J db environmental values")

    # make the output directory
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    ctb_gene_runner = BuildCtbRunner(args)
    ctb_gene_runner.build_ctb_gene(args.output_file1, args.outputdir, args.input_file, args.mount_point)


if __name__ == "__main__": main()

