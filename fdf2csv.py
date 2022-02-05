#!/usr/bin/python3
"""
#title           :fdf2csv.py
#description     :Extract all data from FDF file to a CSV file
#author          :trockenasche
#usage           :python fdf2csv.py file.fdf

#hacker          :wexi
#testing         :Acrobat Reader FDF's only
"""

import bisect
import csv
import os
import re
import sys
from codecs import BOM_UTF16_BE


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

if not fdf.startswith(b'%FDF-1.2'):
    print("Error: Missing FDF signature")
    sys.exit()

# Where the magic happened
pattern = re.compile(rb'<</T\(([^\)]*)\)(/V\(?([^\)>]*)\)?>>)?')
fdf_list = re.findall(pattern, fdf)


def utf(bs):
    return bs.decode('utf_16') if bs.startswith(BOM_UTF16_BE) \
        else bs.decode('ascii')


csn_name = []
csv_value = []
for token in fdf_list:
    key = utf(token[0])
    if key not in ('Submit', 'Reset'):
        loc = bisect.bisect(csn_name, key)
        csn_name.insert(loc, key)
        value = utf(token[2])
        csv_value.insert(loc, value)

# Set the output filename based on input file
csv_file = re.sub(r'\.fdf$', '.csv', fname)

mode = 'at' if os.path.isfile(csv_file) else 'wt'
print('Adding to' if mode == 'at' else 'Creating', os.path.basename(csv_file))

with open(csv_file, mode) as f:
    wr = csv.writer(f)
    if mode == 'wt':
        wr.writerow(csn_name)
    wr.writerow(csv_value)
