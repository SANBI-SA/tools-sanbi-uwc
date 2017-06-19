#!/usr/bin/env python

from __future__ import print_function
import argparse
import os
import shlex
import subprocess
import uuid
import sys

parser = argparse.ArgumentParser(
    description="Call vcf2neo on VCF inputs from Galaxy")

parser.add_argument('--vcf_dataset_names', nargs='+',
                    help='Names of VCF datasets')
parser.add_argument('--neo4j_db_path', help='Neo4j database directory')
parser.add_argument('--user', help='Email of Galaxy user running this tool')
parser.add_argument('--variantset_name',
                    help='Name for the VariantSet containing all the variants')
parser.add_argument('--vcf_files',
                    help='VCF format variant file', nargs='+')

args = parser.parse_args()

os.mkdir(args.variantset_name)

print("VCF names:", len(args.vcf_dataset_names), args.vcf_dataset_names, file=sys.stderr)
print("VCF files:", len(args.vcf_files), args.vcf_files, file=sys.stderr)
for i, vcf_file in enumerate(args.vcf_files):
    print("XXXX I:", i, vcf_file, file=sys.stderr)
    callset_name = args.vcf_dataset_names[i]
    os.symlink(vcf_file, os.path.join(args.variantset_name,
                                      callset_name) + '.vcf')
# Usage: vcf2neo init [OPTIONS] VCF_DIR OWNER [HISTORY_ID] [OUTPUT_DIR]
#
#   Copy reference database and load VCF to Neo4j Graph database. :param
#   vcf_dir: :param refdb_dir: :param d: :return:
#
# Options:
#   -d / -D  Run Neo4j docker container.
#   --help   Show this message and exit.

history_id = str(uuid.uuid4())
cmd_str = ('vcf2neo init -d ' +
           '{input_vcf_dir} {email} {history_id} {neo4j_db_path}'.format(
               input_vcf_dir=args.variantset_name,
               email=args.user,
               history_id=history_id,
               neo4j_db_path=args.neo4j_db_path))
cmd = shlex.split(cmd_str)
subprocess.check_call(cmd)
