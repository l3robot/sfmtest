#!/usr/bin/env python

from src.visualsfm.parsing import Log
from src.common.plotting import plot_2d

from collections import defaultdict

import sys
from os.path import join, isdir, isfile
from os import listdir

def all_logs(dirpath, typ, x, y, logscale):

	dirs = [join(dirpath, im) for im in listdir(dirpath) if isdir(join(dirpath, im))]

	good_dirs = []

	for di in dirs:

		if di[-1] != "/":
			di = di+"/"

		if not isfile(di+"log.txt"):
			continue
		else:
			good_dirs.append(di)

	logs = []

	for di in good_dirs:
		logs.append(Log(di))

	data = {}

	for log in logs:
		log.parse_matches_infos()

		for key, value in log.data.items():

			if key == 'dataset':
				continue
			else:
				try:
					data[key] += value
				except KeyError:
					data[key] = value

	try:
		plot_2d(data[typ], x, y, logscale)
	except KeyError:
		print('crawldata : {0} is not in data'.format(typ))
		return -1

if __name__ == '__main__':

	if len(sys.argv) < 5:
		print("crawldata : You must give a directory name and plotting infos")
		exit(-1)

	if len(sys.argv) > 5:
		logscale = False #fast hack
	else:
		logscale = True

	dirpath, typ, x, y = sys.argv[1:5] 

	all_logs(dirpath, typ, x, y, logscale)