#!/usr/bin/env python

from src.visualsfm.parsing import Parser
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

		if not isfile(di+"Parser.txt"):
			continue
		else:
			good_dirs.append(di)

	logs = []

	for di in good_dirs:
		logs.append(Parser(di))

	data = {}

	for Parser in logs:
		if typ == 'images':
			Parser.parse_images_infos()
		else:
			Parser.parse_matches_infos()

		for key, value in Parser.data.items():

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