#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys
import glob
import shlex
import shutil
import datetime
from subprocess import check_call, CalledProcessError

import logging

log = logging.getLogger(__name__)


class BuildCtbRunner(object):
    def __init__(self, args=None):
        '''
        Initializes an object to run CtbRunner in Galaxy.
        '''
        # Check whether the options are specified and saves them into the object
        # assert args != None
        self.args = args

    def build_ctb_gene(self):
        # cmdline_str = "build_ctb_gene goterms ${}".format(input_file)
        cmdline_str = "touch /tmp/foo.bar"
        cmdline_str = self.newSplit(cmdline_str)
        build_ctb_run = False
        try:
            check_call(cmdline_str)
            build_ctb_run = True
        except CalledProcessError:
            print("Error running the build_ctb_gene goterms", file=sys.stderr)
        if build_ctb_run:
            self.copy_output_file_to_dataset()
            print("Building a new DB, current time: %s" % str(datetime.date.today()))
            print("Noe4j Database Name: http://%s:%s@%s:%s/db/data/" % (self.args.username, self.args.password, self.args.url, self.args.port))
            print("GFF File - Input: %s" % str(self.args.input_file))

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
            if os.path.isdir(file_name):
                shutil.copytree(file_name, self.args.outputdir)
            elif os.path.isfile(file_name):
                shutil.copy(file_name, self.args.outputdir)


def main():
    parser = argparse.ArgumentParser(description="Tool used to extract data about genes using locus_tags")
    parser.add_argument('--outputfile')
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
    except (OSError, ValueError), e:
        print("Error exporting the NEO4J db environmental values", e)

    # make the output directory
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    ctb_gene_runner = BuildCtbRunner(args)
    ctb_gene_runner.build_ctb_gene()


if __name__ == "__main__": main()
