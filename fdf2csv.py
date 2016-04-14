#!/usr/bin/python
#title           :fdf2csv.py
#description     :Extract all data from FDF file to a CSV file
#author          :trockenasche
#version         :0.5.1
#usage           :python fdf2csv.py file.fdf
#=================================================

import sys
import os
import re
import csv

# check if there are a argument
arglen = len(sys.argv)
if not arglen == 2:
    print("Usage: fdf2csv.py file.fdf")
    sys.exit()

# check if the file exist
fname = sys.argv[1]
if not os.path.isfile(fname):
    print("Error: " + fname + " doesn't exist")
    sys.exit()

# open file
fdf_file = open(sys.argv[1], "r")
fdf = fdf_file.read()

# replace "empty" String to an empty value
fdf_list = re.sub("(þÿ|FEFF)", "", fdf)
# print(fdf_list)

# Where the magic happened
pattern = re.compile('\/T\(([^)]*)\)\/V[(/<]([^>)]*)')
fdf_list = re.findall(pattern, fdf_list)
# print(fdf_list)

# separate head and values
csv_head = []
csv_values = []
for i in fdf_list:
    csv_head.append(i[0])
    csv_values.append(i[1])
# alternative way >>> csv_head, csv_values = zip(*fdf_list)

# Set the output filename based on input file
csv_file = re.sub("\.fdf", ".csv", fname)

print("writing file", csv_file)

with open(csv_file, "w") as myfile:
    wr = csv.writer(myfile, delimiter=";", lineterminator='\n')
    wr.writerow(csv_head)
    wr.writerow(csv_values)


# TODO possibility to pass an alternative csv file as an argument
# TODO a possibility to get all fdf from the current folder
# TODO sorting the csv_head before
# TODO check if there already a csv file with the same header and append the values