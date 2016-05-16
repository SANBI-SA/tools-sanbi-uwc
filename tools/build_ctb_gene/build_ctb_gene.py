#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys
import glob

import logging
log = logging.getLogger( __name__ )

def build_ctb_gene(output_file1, output_dir, input_file, mount_point ):
    #cmdline_str = "build_ctb_gene goterms ${}".format(input_file)
    cmdline_str = "echo goterms"
    build_ctb = False
    try:
        os.system(cmdline_str)
        build_ctb = True
    except:
        log.debug("Error running the build_ctb_gene goterms", file=sys.stderr)

    # Read the files at the mount point and load the html file
    if build_ctb == True:
         files=glob.glob(mount_point)
         output_file1 = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
                <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <meta name="generator" content="Galaxy %s tool output - see http://g2.trac.bx.psu.edu/" />
                <title></title>
                <link rel="stylesheet" href="/static/style/base.css" type="text/css" />
                </head>
                <body>
                <div class="toolFormBody">
                <table>
                    <th>Files</th>
                """
         for file in files:
             output_file1 += """<tr><td>file</td></tr>"""
         output_file1 += """</table></div></body></html>\n"""


def main():
    parser = argparse.ArgumentParser(description="Generate a BAM file from the Novo Align tool")
    parser.add_argument('output_file1')
    parser.add_argument('output_dir')
    parser.add_argument('--input_file')
    parser.add_argument('--mount_point')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--url')
    parser.add_argument('--port')
    args = parser.parse_args()

    export_cmd = "export NEO4J_REST_URL=http://${args.username}:${args.password}@${args.url}:${args.port}/db/data/"
    try:
        os.system(export_cmd)
    except:
        log.debug("Error exporting the NEO4J db environmental values")

    build_ctb_gene(args.output_file1, args.output_dir, args.input_file, args.mount_point)

if __name__ == "__main__": main()
