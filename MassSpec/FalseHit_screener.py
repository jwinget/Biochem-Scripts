#! /usr/bin/env python

import sys, csv
from decimal import *

def help():
	print '='*20
	print 'Screens results based on decoy data to remove false positives'
	print '='*20
	print 'To use:'
	print '-'*10
	print 'Export MASCOT results as well as the decoy data'
	print ''
	print 'Invoke the program, followed by the two file names.'
	print '-'*10
	print 'e.g.: ./FalseHit_screener.py decoy.csv sample.csv'
	print '-'*10
	return

def screen():
	decoyfile = open(sys.argv[1], 'r')
	decoyreader = csv.reader(decoyfile)

	i = 0
	decoy_rank1_pepscores = []
	for row in decoyreader:
		i += 1

		#Skip the first 65 lines, header info
		if i < 65:
			pass
		#Put the ion scores of rank 1 peptides into a list
		elif row[8] == '1':
			decoy_rank1_pepscores.append(round(Decimal(row[15])))

	# Sort the list by descending peptide score
	decoy_rank1_pepscores.sort(reverse=True)

	resultfile = open(sys.argv[2], 'r')
	resultreader = csv.reader(resultfile)

	j = 0
	result_rank1_pepscores = []
	for row in resultreader:
		j += 1

		#Skip the first 65 lines, header info
		if j < 65:
			pass
		elif row[8] == '1':
			result_rank1_pepscores.append(round(Decimal(row[15])))
	result_rank1_pepscores.sort(reverse=True)

	for decoy_ion_score in decoy_rank1_pepscores:
		result_ion_score_list = []
		decoy_ion_score_list = []
		for decoy_ion in decoy_rank1_pepscores:
			if decoy_ion >= decoy_ion_score:
				decoy_ion_score_list.append(decoy_ion)
		for result_ion_score in result_rank1_pepscores:
			if result_ion_score >= decoy_ion_score:
				result_ion_score_list.append(result_ion_score)
		false_pos_perc = 100*float(len(decoy_ion_score_list))/float(len(result_ion_score_list))
		print str(decoy_ion_score)+'	'+str(len(result_ion_score_list))+'	'+str(false_pos_perc)

	resultfile.close()
	decoyfile.close()

	return

if sys.argv[1] == '-h':
	help()
elif sys.argv[1] == '--help':
	help()
else:
	screen()
