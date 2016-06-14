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


def inspect_docker(cmd_str):
    output = None
    try:
        output = check_output(cmd_str, shell=True)
    except CalledProcessError:
        print("Error running get_docker_port by build_ctb_gene", file=sys.stderr)
        return None
    return output


class BuildCtbRunner(object):
    def __init__(self, args=None):
        """
        Initializes an object to run CtbRunner in Galaxy.
        """
        # Check whether the options are specified and saves them into the object
        # assert args != None
        self.args = args
        self.outputdir = args.outputdir
        self.mount_point = None
        self.docker_instance_name = "build_ctb_gene_" + str(random.randrange(0, 1000, 2))

    def build_ctb_gene(self):
        cmdline_str = "goget goterms {}".format(self.args.input_file)
        cmdline_str = self.newSplit(cmdline_str)
        try:
            check_call(cmdline_str)
        except CalledProcessError:
            print("Error running the build_ctb_gene goterms", file=sys.stderr)
            return None
        else:
            # self.copy_output_file_to_dataset()
            print("Building a new DB, current time: %s" % str(datetime.date.today()))
            print("GFF File - Input: %s" % str(self.args.input_file))
            return True

    def newSplit(self, value):
        lex = shlex.shlex(value)
        lex.quotes = '"'
        lex.whitespace_split = True
        lex.commenters = ''
        return list(lex)

    def copy_output_file_to_dataset(self):
        """
        Retrieves the output files from the gx working directory and copy them to the Galaxy output directory
        """
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
            return None
        else:
            return True

    def docker_run(self):
        self.mount_point = "{}".format(self.outputdir)
        try:
            os.makedirs(self.mount_point)
        except os.error as e:
            print("Error creating mount point {mount_point}: {error}".format(mount_point=self.mount_point, error=e.strerror))

        cmd_str = "docker run --rm -P -v {mount_point}:/data -e NEO4J_UID={uid} -e NEO4J_GID={gid} -e NEO4J_AUTH=none --name {name} thoba/neo4j_galaxy_ie:latest".format(
            mount_point=self.mount_point,
            name=self.docker_instance_name,
            uid=os.getuid(),
            gid=os.getgid(),
        )
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
    cmd_str = "docker inspect --format='{{(index (index .NetworkSettings.Ports \"7474/tcp\") 0).HostPort}}' %s" % ctb_gene_runner.docker_instance_name

    # TODO: randomise the ports/names/mount_point and use the auto kill image
    neo4j_container_info = inspect_docker(cmd_str)
    if neo4j_container_info is None:
        exit(1)
    else:
        neo4j_port = neo4j_container_info[:-1]
    neo4j_url = 'http://localhost:{}/db/data/'.format(neo4j_port)
    try:
        os.environ["NEO4J_REST_URL"] = neo4j_url
    except (OSError, ValueError), e:
        print("Error setting the NEO4J db environmental values", e)

    # make the output directory
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    url = urlparse(neo4j_url)
    if '@' in url.netloc:
        (host, port) = url.netloc.split('@')[1].split(':')
    else:
        (host, port) = url.netloc.split(':')
    timeout = int(os.environ.get('NEO4J_WAIT_TIMEOUT', 30)) # time to wait till neo4j
    connected = False
    #print('host, port', host, port)
    while timeout > 0:
        try:
            socket.create_connection((host, port), 1)
        except socket.error:
            timeout -= 1
            time.sleep(1)
        else:
            connected = True
            break
    if not connected:
        sys.exit('timed out trying to connect to {}'.format(neo4j_url))        

    status = ctb_gene_runner.build_ctb_gene()
    if status is None:
        exit(1)


if __name__ == "__main__": main()
