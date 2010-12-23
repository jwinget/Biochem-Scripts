#! /usr/bin/python2.6 -tt

# Generates nice reports from MSQuant protein exports

import sys, re, csv
from datetime import date
from math import log
import numpy as np
import matplotlib.pyplot as plt

def Initialize():
	''' Init program and set options '''
	opts_dict = {}
	opts_dict['report_title'] = raw_input("Report title: ")
	d = date.today()
	opts_dict['generated_on'] = d.isoformat()
	opts_dict['label_type'] = raw_input("Labeling: ")
	opts_dict['log2_cutoff'] = input("Log2 cutoff: ")
	return opts_dict

def ParseMSQuant(filename):
	''' Reads in a csv file from MSQuant export and parses it for processing '''
	f = open(filename, 'rU')
	reader = csv.reader(f)
	parse_dict = {}
	header_list = []
	for row in reader:
		if row[1] == 'Mascot Hit':
			for cell in row:
				parse_dict[cell] = []
				header_list.append(cell)
		elif row[0] == 'PROTEIN':
			for i in range(len(row)):
				parse_dict[header_list[i]].append(row[i])
	# Protein info can be retrieved via list position
	return parse_dict

def ProcessMSQuant(opts_dict, parse_dict):
	''' Generate log2, normalize for mixing ratio '''
	ratios = parse_dict['2/1']
	float_ratios = []
	for val in ratios:
		float_ratios.append(float(val))
	r = np.array(float_ratios)
	r_mean = np.mean(r)
	r_dev = np.std(r)
	r_upper = r_mean + r_dev
	r_lower = r_mean - r_dev
	trim = []
	for val in float_ratios:
		if val > r_lower and val < r_upper:
			trim.append(val)
	t = np.array(trim)
	t_mean = np.mean(t)
	mixing_ratio = t_mean
	parse_dict['adjusted ratios']=[]
	for val in float_ratios:
		adj_val = (1.0/t_mean)*val
		parse_dict['adjusted ratios'].append(adj_val)

	parse_dict['log2'] = []

	adj_ratios = parse_dict['adjusted ratios']
	for ratio in adj_ratios:
		i = float(ratio)
		log2 = log(i,2)
		parse_dict['log2'].append(log2)
	y = np.array(parse_dict['log2'])
	x = np.array(range(len(y)))

	# plot the curve
	plt.axes(frame_on=False)
	plt.axhline()
	plt.axhline(y=opts_dict['log2_cutoff'], color='r')
	plt.axhline(y=opts_dict['log2_cutoff']*-1, color='r')
	plt.plot(x, y, 'ko')
	plotfile = opts_dict['report_title']+'_log2_plot_'+opts_dict['generated_on']+'.png'
	plt.savefig(plotfile, dpi=100)
	return mixing_ratio, plotfile, parse_dict

def MetaRetrieve(opts_dict, parse_dict):
	''' Grab info on enriched/deenriched proteins from Uniprot '''
	log_cutoff = opts_dict['log2_cutoff']
	enriched_dict = {}
	deenriched_dict = {}
	for i in range(len(parse_dict['log2'])):
		if parse_dict['log2'][i] < -1*log_cutoff:
			for key in parse_dict.keys():
				if key not in deenriched_dict:
					deenriched_dict[key] = [parse_dict[key][i]]
				else:
					deenriched_dict[key].append(parse_dict[key][i])
		elif parse_dict['log2'][i] > log_cutoff:	
			for key in parse_dict.keys():
				if key not in enriched_dict:
					enriched_dict[key] = [parse_dict[key][i]]
				else:
					enriched_dict[key].append(parse_dict[key][i])
	return enriched_dict, deenriched_dict

def ReportGen():
	''' Generate the LaTeX report '''
	return

# Run the program
def main():
	if len(sys.argv) < 2:
		print 'usage: ./quantjournalist.py file'
		sys.exit(1)
	
	filename = sys.argv[1]

	# Functions defined above
	init_params = Initialize()
	parse = ParseMSQuant(filename)
	mix_ratio, plotfile, parse = ProcessMSQuant(init_params, parse)
	print 'Mixing ratio: '+str(mix_ratio)
	enriched, deenriched = MetaRetrieve(init_params, parse)
	print 'Enriched Proteins:'
	print '-'*10
	for i in range(len(enriched[''])):
		id = enriched['Accession number'][i]
		log2 = enriched['log2'][i]
		desc = enriched['Description'][i]
		print ("%.2f" % log2), id, desc	
	print 'Deenriched Proteins:'
	print '-'*10
	for i in range(len(deenriched[''])):
		id = deenriched['Accession number'][i]
		log2 = deenriched['log2'][i]
		desc = deenriched['Description'][i]
		print ("%.2f" % log2), id, desc	

if __name__ == '__main__':
	main()
