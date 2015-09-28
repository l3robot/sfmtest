#!/usr/bin/env python

import src.sfmtest as sfmtest

import sys

if __name__ == '__main__':

	if len(sys.argv) < 3:
		print("You must give a directory name and an images directory name.")
		exit(-1)

	test_dir_name = sys.argv[1]
	dirpath = sys.argv[2]

	sfmtest.correct_nvm(test_dir_name, dirpath)
