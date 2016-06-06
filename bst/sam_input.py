from avl import GenAVLTree
from itertools import groupby
import csv
import sys


#genome = GenAVLTree()
csvin = csv.reader(sys.stdin,delimiter="\t")
'''
for row in csvin:
	genome[row[2]][int(row[3])] = row

#genome.print_genome('chr1')
print genome['chr1'][564627:564665]
'''
sam_entry = []
for row in csvin:
	sam_entry.append(row)

sam_entry.sort(key=lambda x:x[0])
#print sam_entry
len_dict = {}
for key, group in groupby(sam_entry, lambda x:x[0]):
	seq_group = list(group)
	if len(seq_group) in len_dict:
		len_dict[len(seq_group)].append(seq_group)
	else:
		len_dict[len(seq_group)] = [seq_group]

for key in len_dict:
	print str(key) + "\t" + str(len(len_dict[key]))
