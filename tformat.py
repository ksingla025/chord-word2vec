#!/usr/bin/python

import sys

f_in = open(sys.argv[1],'r').readlines()
label = sys.argv[2].strip()

#print("words"+"\tlabel")
for i in range(0,len(f_in)):
#	print(f_in[i])
	line = f_in[i].strip().split(" ")
	if len(line) == 101:
		vector = line[1:]
		vector = "\t".join(vector)
		word = line[0].strip()+"\t"+label
		print(vector)

