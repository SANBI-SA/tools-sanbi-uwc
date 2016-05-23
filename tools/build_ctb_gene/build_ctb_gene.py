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


def inspect_docker(cmd_str):
    output = None
    try:
        output = check_output(cmd_str, shell=True)
    except CalledProcessError:
        print("Error running get_docker_port by build_ctb_gene", file=sys.stderr)
    return output


class BuildCtbRunner(object):
    def __init__(self, args=None):
        '''
        Initializes an object to run CtbRunner in Galaxy.
        '''
        # Check whether the options are specified and saves them into the object
        # assert args != None
        self.args = args
        self.mount_point = None
        self.docker_instance_name = "build_ctb_gene_" + str(random.randrange(0, 1000, 2))

    def build_ctb_gene(self):
        # cmdline_str = "build_ctb_gene goterms {}".format(self.args.input_file)
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
            # print("Noe4j Database Name: http://%s:%s@%s:%s/db/data/" % (
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
        mp = self.mount_point + "/graph.db"
        result_file = glob.glob(mp + '/*')
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

    def docker_run(self):
        self.mount_point = "{}/neo4j/data".format(os.getcwd())

        cmd_str = "docker run -d -p 7474:7474 -v {}:/data -e NEO4J_AUTH=none --name {} thoba/neo4j_galaxy_ie".format(
            self.mount_point, self.docker_instance_name)
        cmd = self.newSplit(cmd_str)
        try:
            check_call(cmd)
        except CalledProcessError:
            print("Error running docker run by build_ctb_gene", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Tool used to extract data about genes using locus_tags")
    parser.add_argument('--outputdir')
    parser.add_argument('--input_file')
    args = parser.parse_args()

    ctb_gene_runner = BuildCtbRunner(args)

    # boot up a neo4j docker container
    ctb_gene_runner.docker_run()

    # get the port of the docker container
    cmd_str = "docker inspect --format='{{(index (index .NetworkSettings.Ports \"7474/tcp\") 0).HostPort}}' {}".format(
        ctb_gene_runner.docker_instance_name)

    # TODO: randomise the ports/names/mount_point and use the autokill image
    export_cmd = 'export NEO4J_REST_URL=http://localhost:7474/db/data/'
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
