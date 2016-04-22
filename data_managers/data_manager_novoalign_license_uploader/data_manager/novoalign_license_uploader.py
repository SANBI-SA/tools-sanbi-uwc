#!/usr/bin/env 
# Zipho Masholoigu (SANBI-UWC)

import os
import argparse

import logging
log = logging.getLogger( __name__ )

LICENSE_TARGET_DIRECTORY = "novoalign"

#Parse Command Line
parser = argparse.ArgumentParser(description="Upload the nonoalign license to the tool-data path")
parser.add_argument('--license_filename')
parser.add_argument('--license_dir')

args = parser.parse_args()
filename = args.license_filename

#create the license target directory
target_dir = args.license_dir + "/" + LICENSE_TARGET_DIRECTORY
license_file = target_dir+"/"+"license.lic"
if not os.path.isfile(license_file):
    os.mkdir( target_dir )
    #move/copy license file to the tool-data path
    os.rename( filename, target_dir+"/"+"license.lic")
else:
    log.debug("License for novoalign seems to exists already")
