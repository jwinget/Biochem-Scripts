#! /usr/bin/env python

import sys, csv

def help():
	print '='*20
	print 'Subtracts MASCOT hits of control MS from sample.'
	print '='*20
	print 'To use:'
	print '-'*10
	print 'Export your data in CSV format from MASCOT'
	print 'Invoke the program, followed by the two file names.'
	print 'The file with your control data should be first'
	print '-'*10
	print 'e.g.: Control_subtractor control.csv sample.csv'
	print '-'*10
	print 'This will print the list to the console. If you'
	print 'would like to save the list, cat it to a new file'
	print '-'*10
	print 'e.g.: Control_subtractor c.csv s.csv > hits.txt'
	print '-'*10
	return

def subtractor():
	control_file = open(sys.argv[1])
	sample_file = open(sys.argv[2])
	
	control_reader = csv.reader(control_file)

	control_hits = []
	
	i = 0
	for row in control_reader:
		i += 1

		#Skip the first 65 lines, header info
		if i < 65:
			pass
		elif row[1] == '':
			pass
		elif row[1] in control_hits:
			pass
		else:
			control_hits.append(row[1])
	control_file.close()

	print control_hits

	sample_reader = csv.reader(sample_file)
	
	sample_hits = []

	i = 0
	for row in sample_reader:
		i += 1
		if i < 65:
			pass
		elif row[1] == '':
			pass
		elif row[1] in control_hits:
			pass
		else:
			sample_hits.append(row[1])
	sample_file.close()

	for hit in sample_hits:
		print hit
	return

if sys.argv[1] == '-h':
	help()
elif sys.argv[1] == '--help':
	help()
else:
	subtractor()
