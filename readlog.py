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
		metric = len
		value = 'nb_images' #it's kind of a hack, might be good to change it

	elif func == 'MeanNbImage':
		metric = np.mean
		value = 'nb_images'

	elif func == 'MeanSize':
		metric = np.mean
		value = 'mean_sizes'

	elif func == 'MeanStdSize':
		metric = np.mean
		value = 'std_sizes'

	elif func == 'MeanNbCamerasKept':
		metric = np.mean
		value = 'nb_cameras_kept_prop'

	elif func == 'StdNbCamerasKept':
		metric = np.std
		value = 'nb_cameras_kept_prop'

	elif func == 'MeanNbSift':
		metric = np.mean
		value = 'mean_nb_sift'

	elif func == 'MeanStdNbSift':
		metric = np.mean
		value = 'std_nb_sift'

	elif func == 'MeanSiftTime':
		metric = lambda x: to_real_time(np.mean(x))
		value = 't_sift'

	elif func == 'StdSiftTime':
		metric = lambda x: to_real_time(np.std(x))
		value = 't_sift'

	elif func == 'MeanNbMatch':
		metric = np.mean
		value = 'nb_match'

	elif func == 'MeanMatchTime':
		metric = lambda x: to_real_time(np.mean(x))
		value = 't_match'

	elif func == 'StdMatchTime':
		metric = lambda x: to_real_time(np.std(x))
		value = 't_match'

	elif func == 'MeanBATime':
		metric = lambda x: to_real_time(np.mean(x))
		value = 't_ba'

	elif func == 'StdBATime':
		metric = lambda x: to_real_time(np.std(x))
		value = 't_ba'

	elif func == 'MeanCMVS/PMVSTime':
		metric = lambda x: to_real_time(np.mean(x))
		value = 't_cpmvs'

	elif func == 'StdCMVS/PMVSTime':
		metric = lambda x: to_real_time(np.std(x))
		value = 't_cpmvs'

	elif func == 'MeanTotalTime':
		metric = lambda x: to_real_time(np.mean(x))
		value = 't_time'

	elif func == 'StdTotalTime':
		metric = lambda x: to_real_time(np.std(x))
		value = 't_time'

	else:
		return None;

	nb_value = len(dataset[value])

	if nb_value > 0:
		str2return = str(metric(dataset[value]))
		if nb_value != len(dataset['nb_images']):
			str2return = str2return + " ({0})".format(nb_value)
	else:
		str2return = "No Results"

	return str2return

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

			columns = ('NbTests', 'MeanNbImage', 'MeanSize', 'MeanStdSize',\
				       'MeanNbCamerasKept', 'StdNbCamerasKept',\
				       'MeanNbSift', 'MeanStdNbSift', 'MeanSiftTime',\
				       'StdSiftTime','MeanNbMatch', 'MeanMatchTime',\
				       'StdMatchTime','MeanBATime', 'StdBATime',\
				       'MeanCMVS/PMVSTime', 'StdCMVS/PMVSTime',\
				       'MeanTotalTime', 'StdTotalTime')

			for column in columns:

				row = [column]

				for dataset in first_row:
					row.append(apply_function(results[dataset], column))

				table.add_row(tuple(row))

			table.add_hline()

	doc.generate_pdf("results")
	doc.generate_tex("results")

	subprocess.Popen(["evince results.pdf"],shell=True)

def tabular_results(dirs):

	results = defaultdict(lambda : defaultdict(list))

	for di in dirs:

		infos = sfmtest.parse_log(di)

		for keys, value in infos.items():

			if keys == 'dataset':
				continue
			else:
				if isinstance(value, int) or isinstance(value, float):
					results[infos['dataset']][keys].append(value)

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
			print(di)

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
		print(dirpath)
		print(sfmtest.read_log(dirpath))
		print()
