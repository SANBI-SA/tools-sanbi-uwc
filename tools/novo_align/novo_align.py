#!/usr/bin/env python
from __future__ import print_function
import argparse
import shlex
import os
import sys
import logging
log = logging.getLogger( __name__ )


def novo_align(out_file, out_stats, index_filename, fwd_file, rev_file ):
    param = r'@RG\tID:RG\tSM:$i\tPL:ILLUMINA'
    cmdline_str = "novoalign -c 8 -k -d {} -f {} {} -i PE 250, 100 -o SAM '{}' 2> {} > {}".format(
        index_filename,
        fwd_file,
        rev_file,
        param,
        out_stats,
        out_file) 
    try:
        os.system(cmdline_str)
    except:
        print("Error running the nova-align", file=sys.stderr)


def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)


def main():
    parser = argparse.ArgumentParser(description="Generate a BAM file from the Novo Align tool")
    parser.add_argument('out_file')
    parser.add_argument('out_stats')    
    parser.add_argument('--index_filename')
    parser.add_argument('--forward_filename')
    parser.add_argument('--reverse_filename')
    args = parser.parse_args()

    novo_align(args.out_file, args.out_stats, args.index_filename, args.forward_filename, args.reverse_filename)


if __name__ == "__main__":
    main()
