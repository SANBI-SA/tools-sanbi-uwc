#!/usr/bin/env python

from __future__ import print_function
import argparse
from subprocess import check_call, CalledProcessError
from json import load, dump, dumps
from os import environ, mkdir, makedirs
from os.path import isdir, exists
import shlex
import sys


def get_id_name(params, dbkey, fasta_description=None):
    # TODO: ensure sequence_id is unique and does not already appear in location file
    sequence_id = params['param_dict']['sequence_id']
    if not sequence_id:
        sequence_id = dbkey

    sequence_name = params['param_dict']['sequence_name']
    if not sequence_name:
        sequence_name = fasta_description
        if not sequence_name:
            sequence_name = dbkey
    return sequence_id, sequence_name


def make_rnastar_index(output_directory, fasta_filename):
    if exists(output_directory) and not isdir(output_directory):
        print("Output directory path already exists but is not a directory: {}".format(output_directory),
              file=sys.stderr)
    elif not exists(output_directory):
        mkdir(output_directory)

    if 'GALAXY_SLOTS' in environ:
        nslots = environ['GALAXY_SLOTS']
    else:
        nslots = 1

    cmdline_str = 'STAR --runMode genomeGenerate --genomeDir {} --genomeFastaFiles {} --runThreadN {}'.format(
        output_directory,
        fasta_filename,
        nslots)
    cmdline = shlex.split(cmdline_str)
    try:
        check_call(cmdline)
    except CalledProcessError:
        print("Error building RNA STAR index", file=sys.stderr)
    return (output_directory)


def main():
    parser = argparse.ArgumentParser(description="Generate RNA STAR genome index and JSON describing this")
    parser.add_argument('output_filename')
    parser.add_argument('--fasta_filename')
    parser.add_argument('--fasta_dbkey')
    parser.add_argument('--fasta_description', default=None)
    parser.add_argument('--data_table_name', default='rnastar_index')
    args = parser.parse_args()

    filename = args.output_filename

    params = load(open(filename, 'rb'))
    output_directory = params['output_data'][0]['extra_files_path']
    makedirs(output_directory)

    make_rnastar_index(output_directory, args.fasta_filename)
    (sequence_id, sequence_name) = get_id_name(params, args.fasta_dbkey, args.fasta_description)
    data_table_entry = dict(value=sequence_id, dbkey=args.fasta_dbkey, name=sequence_name, path=output_directory)

    output_datatable_dict = dict(data_tables={args.data_table_name: [data_table_entry]})
    open(filename, 'wb').write(dumps(output_datatable_dict))

if __name__ == "__main__":
    main()
