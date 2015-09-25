#!/usr/bin/env python

import src.sfmtest as sfmtest

import sys
from os.path import join, isdir
from os import listdir

def all_logs(dirpath):

	dirs = [join(dirpath, im) for im in listdir(dirpath) if isdir(join(dirpath, im))]

	for di in dirs:
		if di[-1] != "/":
			di = di+"/"
		head = "FOR {0}".format(di)
		thelen = len(head) 
		print(head)
		print("-"*thelen)
		sfmtest.read_log(di)
		print()

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
	else:
		if dirpath[-1] != "/":
			dirpath = dirpath+"/"
		head = "FOR {0}".format(dirpath)
		thelen = len(head) 
		print(head)
		print("-"*thelen)
		sfmtest.read_log(dirpath)
		print()
