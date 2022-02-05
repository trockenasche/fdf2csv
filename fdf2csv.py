#!/usr/bin/python3
"""
#title           :fdf2csv.py
#description     :Extract all data from FDF file to a CSV file
#author          :trockenasche
#version         :0.5.1
#usage           :python fdf2csv.py file.fdf

#contributor     :wexi
#testing         :Acrobat Reader FDF's only
"""

import bisect
import csv
import os
import re
import sys
from codecs import BOM_UTF16_LE, BOM_UTF16_BE


# check if there are a argument
arglen = len(sys.argv)
if not arglen == 2:
    print("Usage: fdf2csv.py file[.fdf]")
    sys.exit()

# check if the file exist
fname = os.path.expanduser(sys.argv[1])
if fname.endswith('.'):
    fname += 'fdf'
elif not fname.endswith('.fdf'):
    fname += '.fdf'
if not os.path.isfile(fname):
    print("Error: " + fname + " doesn't exist")
    sys.exit()

# open file
with open(fname, 'rb') as f:
    fdf = f.read()

if not fdf.startswith(b'%FDF-1.2\r%'):
    print("Error: Missing FDF signature")
    sys.exit()

# Where the magic happened
pattern = re.compile(rb'<</T\(([^\)]*)\)(/V\(([^\)]*)\))?>>')
fdf_list = re.findall(pattern, fdf)

# separate head and values
csv_head = []
csv_values = []
for i in fdf_list:
    bom = i[0][:2]
    if bom in (BOM_UTF16_LE, BOM_UTF16_BE):  # ignores Submit
        key = i[0].decode('utf-16')
        loc = bisect.bisect(csv_head, key)
        csv_head.insert(loc, key)
        bom = i[2][:2]
        if bom in (BOM_UTF16_LE, BOM_UTF16_BE):
            value = i[2].decode('utf-16')
        else:
            value = i[2].decode('utf-8')
        csv_values.insert(loc, value)

# Set the output filename based on input file
csv_file = re.sub(r'\.fdf$', '.csv', fname)

mode = 'at' if os.path.isfile(csv_file) else 'wt'
print('Adding to' if mode == 'at' else 'Creating', os.path.basename(csv_file))

with open(csv_file, mode) as f:
    wr = csv.writer(f)
    if mode == 'wt':
        wr.writerow(csv_head)
    wr.writerow(csv_values)
