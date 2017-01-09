#!/usr/bin/env python
from __future__ import print_function
import argparse
from subprocess import check_call, CalledProcessError
import shlex
import sys
import logging
log = logging.getLogger( __name__ )


def novo_sort( bam_filename, output_filename ):
    cmdline_str = "novosort -c 8 -m 8G -s -f {} -o {}".format( bam_filename, output_filename )
    cmdline = newSplit(cmdline_str)
    try:
        check_call(cmdline)
    except CalledProcessError:
        print("Error running the nova-sort", file=sys.stderr)


def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)


def main():
    parser = argparse.ArgumentParser(description="Re-sorting aligned files by read position")
    parser.add_argument('output_filename')
    parser.add_argument('--bam_filename')
    args = parser.parse_args()

    novo_sort(args.bam_filename, args.output_filename)


if __name__ == "__main__":
    main()
