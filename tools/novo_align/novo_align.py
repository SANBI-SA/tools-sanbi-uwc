#!/usr/bin/env python
from __future__ import print_function
import argparse
import shlex
import os
import logging
log = logging.getLogger( __name__ )

def novo_align(output_filename, index_filename, fwd_file, rev_file ):
    param = r'@RG\tID:RG\tSM:$i\tPL:ILLUMINA'
    cmdline_str = "novoalign -c 8 -k -d {} -f {} {} -i PE 250, 100 -o SAM '{}' | samtools view -bS - > {}".format(
        index_filename,
        fwd_file,
        rev_file,
        param,
        output_filename)
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
    parser.add_argument('output_filename')
    parser.add_argument('--index_filename')
    parser.add_argument('--forward_filename')
    parser.add_argument('--reverse_filename')
    args = parser.parse_args()
   
    # a dirty way of referencing the file
    index_file_path = args.index_filename + "/" + args.index_filename.split("/")[-1]
    novo_align(args.output_filename, index_file_path, args.forward_filename, args.reverse_filename)

if __name__ == "__main__": main()
