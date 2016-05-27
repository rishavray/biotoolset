#!/usr/bin/python

import argparse
import os
import gzip
import sys

#Defining the argparse object and its attributes
parser = argparse.ArgumentParser(description="Runs Quality check on fastq files.\n At least one of the cut off values are required to process")
requiredArgument = parser.add_argument_group('Required arguments')
requiredArgument.add_argument("-i", metavar="<input filename>", help="Input fastq file",required=True)
requiredArgument.add_argument("-o", metavar="<output filename>", help="Output fastq file",required=True)
parser.add_argument("--average_cutoff", default=0, metavar="<value>", type=int, help="Removes reads with an average Phred score below <value>")
parser.add_argument("--lower_cutoff", default=0, metavar="<value>", type=int, help="Removes reads that contain one or more bases called with a Phred score below <value>")
parser.add_argument("--format", default="Sanger", metavar="<value>", choices=['Illumina', 'Sanger'], help="Quality score format. Default is Sanger")
args = parser.parse_args()

in_format=args.format
average_cutoff=args.average_cutoff
lower_cutoff=args.lower_cutoff
infile = args.i
outfile = args.o

# Sanity checks
if args.format != "Sanger" and args.format != "Illumina":
	sys.stderr.write("Input format has to be 'Sanger' or 'Illumina'\n")
	exit()
if (average_cutoff + lower_cutoff ) == 0:
	sys.stderr.write("Define a quality cutoff. Use -h option to see help\n")
	exit()

# Checking and setting input/output paths 
out_path = os.path.split(outfile)[0]
in_path = os.path.split(infile)[0]
if not os.path.isfile(infile):
	sys.stderr.write("Not a valid input file\n")
	exit()
if not os.path.exists(out_path):
	outfile = in_path + "/" + outfile

if infile.endswith(".gz"):
	infilept = gzip.open(infile,"rb")
	outfile_pass = outfile + "_pass.gz"
	outfile_fail = outfile + "_fail.gz"
	outfile_pass_pt = gzip.open(outfile_pass,"wb")
	outfile_fail_pt = gzip.open(outfile_fail,"wb")

else:
	infilept = open(infile,"rb")
	outfile_pass_pt = open(outfile+"_pass","wb")
	outfile_fail_pt = open(outfile+"_fail","wb")

# Setting differences with formats

if in_format == 'Sanger':
	diff = 33
elif in_format == 'Illumina':
	diff = 64

# Quality checking
while True:
	line = infilept.readline().strip()
	if not line:
		break
	read = [line.strip()]
	read.append(infilept.readline().strip())
	read.append(infilept.readline().strip())
	read.append(infilept.readline().strip())
	phred = [ord(quality) - diff for quality in read[3]]
	phred_min = min(phred)
	phred_avg = sum(phred)/len(phred)
	
	if phred_min >= lower_cutoff and phred_avg > average_cutoff:
		outfile_pass_pt.write(read[0] + "\n" + read[1] + "\n" + read[2] + "\n" + read[3] + "\n")
	else:
		outfile_fail_pt.write(read[0] + "\n" + read[1] + "\n" + read[2] + "\n" + read[3] + "\n")

infilept.close()
outfile_pass_pt.close()
outfile_fail_pt.close()

