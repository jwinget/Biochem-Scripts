#!/usr/bin/env python

import sys, string

def help():
	print '='*20
	print 'Compares two lists of hits'
	print '='*20
	print 'To use:'
	print '-'*10
	print 'Generate two lists of IPI identifiers'
	print 'Files should have one identifier per line'
	print 'This can be the output of Control_subtractor'
	print 'Invoke the program, followed by the two file names.'
	print '-'*10
	print 'e.g.: ./Hit_list_compare.py list1.txt list2.txt'
	print '-'*10
	print 'This will print the comparison to the console. If you'
	print 'would like to save the comparison, cat it to a new file'
	print '-'*10
	print 'e.g.: ./Hit_list_compare.py 1.txt 2.txt > compare.txt'
	print '-'*10
	return

def compare():
	list1 = open(sys.argv[1], 'r')
	list2 = open(sys.argv[2], 'r')

	list1_name = string.rstrip(sys.argv[1], '.txt')
	list2_name = string.rstrip(sys.argv[1], '.txt')

	list1_list = []
	list2_list = []

	for line in list1:
		list1_list.append(line)
	for line in list2:
		list2_list.append(line)

	matches = []
	list1_uniques = []
	list2_uniques = []

	for item in list1_list:
		if item in list2_list:
			matches.append(item)
		else:
			list1_uniques.append(item)
	
	for item in list2_list:
		if item in list1_list:
			pass
		else:
			list2_uniques.append(item)

	print '='*20
	print 'MATCHES'
	print '='*20
	for item in matches:
		print item
	print '='*20
	print list1_name+' UNIQUES'
	print '='*20
	for item in list1_uniques:
		print item
	print '='*20
	print list2_name+' UNIQUES'
	print '='*20
	for item in list2_uniques:
		print item

if sys.argv[1] == '-h':
	help()
elif sys.argv[1] == '--help':
	help()
else:
	compare()
