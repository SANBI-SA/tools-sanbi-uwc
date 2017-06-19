#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import os.path

parser = argparse.ArgumentParser(
    description="Write HTML summary from neostore datatype")
parser.add_argument('basepath')
parser.add_argument('label')

args = parser.parse_args()

output = """<html><head><title>Files for Composite Dataset ({})</title></head>
    <p/>This composite dataset is composed of
     the following files:<p/><ul>\n""".format(args.label)
db_path = args.basepath + '/neo4jdb/databases/graph.db'
for filename in os.listdir(db_path):
    if filename.startswith('.'):
        continue
    path = db_path + '/' + filename
    if os.path.isdir(path):
        continue
    output += "<li>{}</li>\n".format(filename)
output += '</ul></html>\b'
print(output)
