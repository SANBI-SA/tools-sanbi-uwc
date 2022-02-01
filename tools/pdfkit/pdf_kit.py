#!/usr/bin/env python
from __future__ import print_function
import argparse
from subprocess import check_call, CalledProcessError
import shlex
import sys
import pdfkit
import logging

log = logging.getLogger(__name__)


def generate_pdf(input_file, output_file):
    cmdline_str = "pdfkit.from_file({}, {})".format(input_file, output_file)
    cmdline = new_split(cmdline_str)
    try:
        check_call(cmdline)
    except CalledProcessError:
        print("Error running the tsv convert to pdf", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--input_file')
    parser.add_argument('--out', default="output.pdf")


    args = parser.parse_args()
    generate_pdf(args.input_file, args.out)

if __name__ == "__main__":
    main()
