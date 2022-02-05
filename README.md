FDF2CSV
=========
The Forms Data Format (FDF) is based on PDF, it uses the same syntax and has essentially the same file structure, but is much simpler than PDF, since the body of an FDF document consists of only one required object. Forms Data Format is defined in the PDF specification (since PDF 1.2). The Forms Data Format can be used when submitting form data to a server, receiving the response, and incorporating into the interactive form. It can also be used to export form data to stand-alone files that can be imported back into the corresponding PDF interactive form. Beginning in PDF 1.3, FDF can be used to define a container for annotations that are separate from the PDF document they apply to.

tl;dr
-----
FDF (Forms Data Format) is a file format for representing form data and annotations that are contained in a PDF form.<br>
This tool extract all information to a csv file.

Usage
=====
fdf2csv.py filename[.fdf]

Adds row/data to the output filename.csv if it exists. It is assumed that
the FDF file labels are unique; They would become the CSV column names.
