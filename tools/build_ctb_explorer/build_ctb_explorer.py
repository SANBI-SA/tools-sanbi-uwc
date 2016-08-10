#!/usr/bin/env python
from __future__ import print_function

import argparse
import datetime
import glob
import shutil

import os

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import logging

log = logging.getLogger(__name__)


def copy_output_file_to_dataset(dir_name, input_dir, dt_type=None):
    """
    Copy the datasets file to the news dataset cbt_browser
    :param dir_name: the target output directory for the ctb_explorer dataset
    :param input_dir: the input files
    :param dt_type: the type of input dataset (neo4jdb, jbrowser - default to None)
    :return: boolean
    """
    dt_loc = input_dir.rpartition('/')[2].replace(".dat", "_files")
    if dt_type:
        if dt_type == "neo4jdb":
            src_files = glob.glob(os.path.dirname(input_dir) + '/{}/{}'.format(dt_loc, dt_type) + "/*" )
        else:
            src_files = glob.glob(os.path.dirname(input_dir) + '/{}'.format(dt_loc) + "/*" )
    else:
        return False
    for file_name in src_files:
        if os.path.isfile(file_name):
            try:
                shutil.copy2(file_name, dir_name)
            except shutil.Error as e:
                log.debug('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                log.debug('Error: %s' % e.strerror)
        elif os.path.isdir(file_name):
            # create the parent dir before copytree
            try:
                os.chdir(dir_name)
                shutil.copytree(file_name, file_name.rsplit('/', 1)[-1])
            except shutil.Error as e:
                log.debug('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                log.debug('Error: %s' % e.strerror)
    return True


class BuildCtbExplorerRunner(object):

    def __init__(self, args=None):
        """
        Initializes an object to run CtbRunner in Galaxy.
        """
        # Check whether the options are specified and saves them into the object
        self.args = args
        self.output_neo4jdb = args.output_neo4jdb
        self.output_jbrowser = args.output_jbrowser
        self.input_neo4jdb = args.input_neo4jdb
        self.input_jbrowser = args.input_jbrowser

    def build_ctb_explorer(self):
        """
        :rtype: boolean
        """
        if copy_output_file_to_dataset(self.output_neo4jdb, self.input_neo4jdb, dt_type="neo4jdb") and \
                copy_output_file_to_dataset(self.output_jbrowser, self.input_jbrowser, dt_type="jbrowser"):

            """Copy the jbrowser input data file to the outputdir @TODO: investigate altenatives"""
            try:
                shutil.copy2(self.input_jbrowser, os.path.join(self.output_jbrowser, 'index.html'))
            except shutil.Error as e:
                log.debug('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                log.debug('Error: %s' % e.strerror)
            print("CTB Report run time: %s" % str(datetime.date.today()))
            print("Neo4jDB - Input: %s" % str(self.args.input_neo4jdb))
            print("JBrowser - Input: %s" % str(self.args.input_jbrowser))
        else:
            return False
        return True


def main():
    parser = argparse.ArgumentParser(description="Tool used to build a combat-tb explorer dataset")
    parser.add_argument('--output_neo4jdb')
    parser.add_argument('--output_jbrowser')
    parser.add_argument('--input_neo4jdb')
    parser.add_argument('--input_jbrowser')
    args = parser.parse_args()

    ctb_explorer_runner = BuildCtbExplorerRunner(args)

    # make the output directory (neo4j)
    if not os.path.exists(args.output_neo4jdb):
        os.makedirs(args.output_neo4jdb)

    # make the output directory (jbrowser)
    if not os.path.exists(args.output_jbrowser):
        os.makedirs(args.output_jbrowser)

    status = ctb_explorer_runner.build_ctb_explorer()

    if status is None:
        exit(1)

if __name__ == "__main__":
    main()
