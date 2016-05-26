#!/usr/bin/python

import argparse
import os
import gzip
import sys

#Defining the argparse object and its attributes
parser = argparse.ArgumentParser(description="Collapses the reads by merging the same reads with counts as the fasta header")
requiredArgument = parser.add_argument_group('Required arguments')
requiredArgument.add_argument("-i", metavar="<input filename>", help="Input fastq file. - if input is stdin",required=True)
requiredArgument.add_argument("-o", metavar="<output filename>", help="Output fastq file. - if output is stdout",required=True)
requiredArgument.add_argument("--format", metavar="<format>", choices=['fastq', 'fasta'], help="Input format. Must be 'fastq' or 'fasta'")
args = parser.parse_args()

infile = args.i
outfile = args.o
in_format = args.format

if infile == "-":
	infile_pt = sys.stdin
else:
	if not os.path.isfile(infile):
		sys.stderr.write("Not a valid input file\n")
		exit()
	else:
		if infile.endswith(".gz"):
			infile_pt = gzip.open(infile,"rb")
		else:
			infilept = open(infile,"rb")

if outfile == "-":
	outfile_pt = sys.stdout
else:
	if not outfile.endswith(".gz"):
		outfile += ".gz"
	outfile_pt = gzip.open(outfile,"wb")

seq_dict = {}

for line in infile_pt:
	seq = infile_pt.readline().strip()

	if in_format == "fastq":
		
		if seq in seq_dict:
			seq_dict[seq] += 1
		else:
			seq_dict[seq] = 1
		infile_pt.readline()
		infile_pt.readline()
	else:

		if seq in seq_dict:
			seq_dict[seq] += 1
		else:
			seq_dict[seq] = 1

for key in seq_dict:
	outfile_pt.write(">" + str(seq_dict[key]) + "\n" + key + "\n")