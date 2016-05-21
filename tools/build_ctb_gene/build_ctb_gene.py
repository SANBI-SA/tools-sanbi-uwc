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
        self.mount_point = "database/neo4j/data"

    def build_ctb_gene(self):
        #cmdline_str = "build_ctb_gene goterms {}".format(self.args.input_file)
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
            #print("Noe4j Database Name: http://%s:%s@%s:%s/db/data/" % (
            #    self.args.username, self.args.password, self.args.url, self.args.port))
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
        mount_point = str(os.getcwd) + "/neo4j/data/graph.db"
        result_file = glob.glob( mount_point + '/*')
        for file_name in result_file:
            if os.path.isfile(file_name):
                shutil.copy2(file_name, self.args.outputdir)
            elif os.path.isdir(file_name):
                # create the parent dir before copytree
                os.chdir(self.args.outputdir)
                shutil.copytree(file_name, file_name.rsplit('/', 1)[-1])

    def docker_stop(self):
        stop_cmd = 'docker stop build_ctb_gene'
        stop_cmd_str = self.newSplit(stop_cmd)
        try:
            check_call(stop_cmd_str)
        except CalledProcessError:
            print("Error running docker stop build_ctb_gene", file=sys.stderr)
        
    def docker_rm(self):
        cmd_str = 'docker rm build_ctb_gene'
        cmd = self.newSplit(cmd_str)
        check_call(cmd)

    def docker_run(self):
        rand_number = random.randrange(0, 1000, 2)
        cmd_str = "docker run -d -p 7474:7474 -v {}/neo4j/data:/data -e NEO4J_AUTH=none --name build_ctb_gene neo4j:2.3".format(os.getcwd())
        cmd = self.newSplit(cmd_str)
        check_call(cmd)

    def docker_container_check(self):
        cmd_str = 'docker ps -a -f name=build_ctb_gene | grep build_ctb_gene'
        output = False
        try:
            output = check_output(cmd_str, shell=True)
        except CalledProcessError:
            print("Error running docker container check", file=sys.stderr)
        if output:
            return True
        return False

def main():
    parser = argparse.ArgumentParser(description="Tool used to extract data about genes using locus_tags")
    #parser.add_argument('--outputfile')
    parser.add_argument('--outputdir')
    parser.add_argument('--input_file')
    #parser.add_argument('--mount_point')
    #parser.add_argument('--username')
    #parser.add_argument('--password')
    #parser.add_argument('--url')
    #parser.add_argument('--port')
    args = parser.parse_args()

    ctb_gene_runner = BuildCtbRunner(args)

    # boot up a neo4j docker container
    if ctb_gene_runner.docker_container_check():
        ctb_gene_runner.docker_stop()
        ctb_gene_runner.docker_rm()
    ctb_gene_runner.docker_run()
    
    # TODO: randomise the ports/names/mount_point and use the autokill image
    export_cmd = "export NEO4J_REST_URL=http://localhost:7474/db/data/"
    try:
        os.system(export_cmd)
    except (OSError, ValueError), e:
        print("Error exporting the NEO4J db environmental values", e)

    # make the output directory
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)
    time.sleep(60)
    ctb_gene_runner.build_ctb_gene()


if __name__ == "__main__": main()
