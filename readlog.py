#!/usr/bin/env python

import src.sfmtest as sfmtest

import sys

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("You must give a directory name")
		exit(-1)

	dirpath = sys.argv[1]	

	sfmtest.read_log(dirpath)
