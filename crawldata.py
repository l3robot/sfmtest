#!/usr/bin/env python

from src.visualsfm.parsing import Log
from src.common.plotting import plot_2d

import sys
from os.path import join, isdir, isfile
from os import listdir

def all_logs(dirpath, x, y):

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

	for log in logs:
		log.parse_image_infos()

	plot_2d(logs[2].data['images'], x, y)

if __name__ == '__main__':

	if len(sys.argv) < 4:
		print("You must give a directory name and plotting infos")
		exit(-1)

	all_logs(sys.argv[1], sys.argv[2], sys.argv[3])