#!/usr/bin/env python





if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("You must give a directory name")
		exit(-1)

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
