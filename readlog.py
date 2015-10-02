#!/usr/bin/env python

import src.sfmtest as sfmtest

import sys
from os.path import join, isdir, isfile
from os import listdir
from collections import defaultdict

import numpy as np

import subprocess

from pylatex import Document, Section, Table, Package

def to_real_time(sec):

	m, s = divmod(sec, 60)
	h, m = divmod(m, 60)

	return "{0}h {1}m {2}s".format(int(h), int(m), int(s))

def apply_function(dataset, func): #not very effective

	if func == 'NbTests':
		return str(len(dataset['nb_images']))
	elif func == 'MeanNbImage':
		return str(np.mean(dataset['nb_images']))
	elif func == 'MeanNbSift':
		return str(np.mean(dataset['nb_sift']))
	elif func == 'MeanSiftTime':
		return to_real_time(np.mean(dataset['t_sift'])) 
	elif func == 'StdSiftTime':
		return to_real_time(np.std(dataset['t_sift'])) 
	elif func == 'MeanNbMatch':
		return str(np.mean(dataset['nb_match']))
	elif func == 'MeanMatchTime':
		return to_real_time(np.mean(dataset['t_match'])) 
	elif func == 'StdMatchTime':
		return to_real_time(np.std(dataset['t_match'])) 
	elif func == 'MeanBATime':
		return to_real_time(np.mean(dataset['t_ba'])) 
	elif func == 'StdBATime':
		return to_real_time(np.std(dataset['t_ba'])) 
	else:
		return None;

def gen_latex(results):

	doc = Document()

	doc.packages.append(Package('geometry', options=['tmargin=1cm',
                                                 'lmargin=2cm', 'rmargin=2cm']))

	with doc.create(Section('Results on each dataset')):
		with doc.create(Table('| l |'+ ' c '*len(results)+'|')) as table:
			table.add_hline()

			first_row = []

			for key, _ in results.items():
				first_row.append(key)
			
			table.add_row(tuple(['Datasets']+first_row))

			table.add_hline()

			columns = ('NbTests', 'MeanNbImage', 'MeanNbSift', 'MeanSiftTime', 'StdSiftTime',\
				   'MeanNbMatch', 'MeanMatchTime', 'StdMatchTime', 'MeanBATime', 'StdBATime')

			for column in columns:

				# table.add_hline()

				row = [column]

				for dataset in first_row:
					row.append(apply_function(results[dataset], column))

				table.add_row(tuple(row))

			table.add_hline()

	doc.generate_pdf("results")

	subprocess.Popen(["evince results.pdf"],shell=True)


def tabular_results(dirs):

	results = defaultdict(lambda : defaultdict(list))

	for di in dirs:

		infos = sfmtest.parse_log(di)

		results[infos['dataset']]['nb_images'].append(infos['nb_images'])
		results[infos['dataset']]['nb_sift'].append(infos['nb_sift'])
		results[infos['dataset']]['t_sift'].append(infos['t_sift'])
		results[infos['dataset']]['nb_match'].append(infos['nb_match'])
		results[infos['dataset']]['t_match'].append(infos['t_match'])
		results[infos['dataset']]['t_ba'].append(infos['t_ba'])
	
	# for key, values in results.items():
	# 	print(key)
	# 	print(values)

	gen_latex(results)


def all_logs(dirpath, print_bool=1):

	dirs = [join(dirpath, im) for im in listdir(dirpath) if isdir(join(dirpath, im))]

	good_dirs = []

	for di in dirs:

		if di[-1] != "/":
			di = di+"/"

		if not isfile(di+"log.txt"):
			continue
		else:
			good_dirs.append(di)

		if print_bool:
			print(sfmtest.read_log(di)) # note1 : not effective, read 2 times
			print()

	if not print_bool:
		tabular_results(good_dirs) # note 1
 
if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("You must give a directory name")
		exit(-1)

	if len(sys.argv) > 2:
		option = sys.argv[2]
	else:
		option = "--one"

	dirpath = sys.argv[1]	

	if option == "--all":
		all_logs(dirpath)
	elif option == "--all-no-print":
		all_logs(dirpath, 0)
	else:
		if dirpath[-1] != "/":
			dirpath = dirpath+"/"
		head = "FOR {0}".format(dirpath)
		thelen = len(head) 
		print(head)
		print("-"*thelen)
		sfmtest.read_log(dirpath)
		print()
