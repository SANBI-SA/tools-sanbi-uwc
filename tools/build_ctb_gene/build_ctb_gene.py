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
        assert args != None
        self.args = args

    def build_ctb_gene(self, output_file1, output_dir, input_file, mount_point):
        # cmdline_str = "build_ctb_gene goterms ${}".format(input_file)
        cmdline_str = "touch /tmp/foo.bar"
        build_ctb = False
        cmdline_str = self.newSplit(cmdline_str)
        try:
            check_call(cmdline_str)
            build_ctb = True
        except CalledProcessError:
            print("Error running the build_ctb_gene gotermS", file=sys.stderr)

        # Read the files at the mount point and load the html file
        if build_ctb:
            files = glob.glob(mount_point)
            output_file1 = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
                            <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                            <meta name="generator" content="Galaxy %s tool output - see http://g2.trac.bx.psu.edu/" />
                            <title></title>
                            <link rel="stylesheet" href="/static/style/base.css" type="text/css" />
                            </head>
                            <body>
                            <div class="toolFormBody">
                            <table>
                                <th>Files</th>
                            """
            for f in files:
                output_file1 += "<tr><td>" + f + "</td></tr>"
            output_file1 += """</table></div></body></html>\n"""

        self.copy_output_file_to_dataset()
        return output_file1

    def newSplit(value):
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
        with open(result_file[0], 'rb') as fsrc:
            with open(self.args.outputdir, 'wb') as fdest:
                shutil.copyfileobj(fsrc, fdest)


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
