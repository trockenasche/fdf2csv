#!/usr/bin/python3
"""
#title           :fdf2csv.py
#description     :Extract all data from FDF file to a CSV file
#author          :trockenasche
#version         :0.5.1
#usage           :python fdf2csv.py file.fdf
"""

import csv
import os
import re
import sys
from codecs import BOM_UTF16_LE, BOM_UTF16_BE

# check if there are a argument
arglen = len(sys.argv)
if not arglen == 2:
    print("Usage: fdf2csv.py file.fdf")
    sys.exit()

# check if the file exist
fname = os.path.expanduser(sys.argv[1])
if not os.path.isfile(fname):
    print("Error: " + fname + " doesn't exist")
    sys.exit()

# open file
with open(fname, 'rb') as f:
    fdf = f.read()

# Where the magic happened
pattern = re.compile(rb'<</T\(([^\)]*)\)(/V\(([^\)]*)\))?>>')
fdf_list = re.findall(pattern, fdf)

# separate head and values
csv_head = []
csv_values = []
for i in fdf_list:
    bom = i[0][:2]
    if bom in (BOM_UTF16_LE, BOM_UTF16_BE):  # ignores Submit
        csv_head.append(i[0].decode('utf-16'))
        bom = i[2][:2]
        if bom in (BOM_UTF16_LE, BOM_UTF16_BE):
            csv_values.append(i[2].decode('utf-16'))
        else:
            csv_values.append(i[2].decode('utf-8'))

# Set the output filename based on input file
csv_file = re.sub(r'\.fdf', ".csv", fname)

print("writing file", csv_file)

with open(csv_file, 'wt') as f:
    wr = csv.writer(f)
    wr.writerow(csv_head)
    wr.writerow(csv_values)

"""
TODO possibility to pass an alternative csv file as an argument
TODO a possibility to get all fdf from the current folder
TODO sorting the csv_head before
TODO check if there already a csv file with the same header and append the
values
"""
