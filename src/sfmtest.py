#!/usr/bin/env python

import random
import sys
import os
import time

from subprocess import call
from shutil import copy, move

# Infos #####################

sfm_command = ["VisualSFM", "sfm"]
test_dir = "/dev/shm/"
good_ext = (".jpg", ".JPG")
log_path = "/home/local/shared/sfm/bin/log" 

#############################

# Return true if the string represent a file and an image
def file_and_image(dirpath, images):

	path = os.path.join(dirpath, images)

	if not os.path.isfile(path):
		return False

	_, ext = os.path.splitext(path)

	if not ext in good_ext:
		return False

	return True

# Choose a random number of images to use
def choose_image(dirpath, number):

	test_time = time.asctime(time.localtime())
	test_time = test_time.lower().replace(" ", "_")
	print(test_time)

	if dirpath[-1] == '/':
		dirname = dirpath[0:-1]
	else:
		dirname = dirpath

	if os.path.basename(dirname) == "images":
		dirname = dirpath[0:dirpath.find("/images")]

	dirname = os.path.basename(dirname)

	print("-- Beginning tests on {0} images of {1} --".format(number, dirname))

	images = [os.path.join(dirpath, im) for im in os.listdir(dirpath) if file_and_image(dirpath, im)]

	try:
		idx = random.sample(range(0,len(images)), int(number))
	except ValueError:
		print("Not enough images, will take all images.")
		number = len(images)
		idx = random.sample(range(0,len(images)), int(number))

	images_kept = [im for i, im in enumerate(images) if i in idx]

	test_dir_name = test_dir+"sfmtest-"+dirname+"_"+str(number)+"img"+"-"+test_time+"/"

	if not os.path.exists(test_dir_name):
		os.makedirs(test_dir_name)
	else:
		os.makedirs(test_dir_name+"-v2")

	with open(test_dir_name+"images.txt", "w") as f:
		f.write("#"*21+"\n")
		f.write("#"+" "*4+"Images used"+" "*4+"#"+"\n")
		f.write("#"*21+"\n")
		f.write("\n".join(images_kept))

	return (test_dir_name, images_kept)

# Copy images to test in test_dir
def setup_dir(test_dir_name, images_to_test):

	print("Setup sfmtest directory")

	images_dir = test_dir_name+"images/"

	os.makedirs(images_dir)

	for image in images_to_test:
		print("Copy {0} to {1}".format(os.path.basename(image), images_dir))
		copy(image, images_dir)

# Start VisualSFM on test_dir/images
def start_sfm(test_dir_name):

	print("Starting VisualSFM ...")

	command = sfm_command + [(test_dir_name + "images"), (test_dir_name + "sfm.nvm")]
	with open(test_dir_name+"log.txt", "w") as f:
		call(command, stdout=f)

	print("End of VisualSFM processing")

# Erase images in test_dir/images
def clean_dir(test_dir_name, images_to_test):

	print("Clean sfmtest directory")

	images_dir = test_dir_name+"images/"

	for image in images_to_test:
		image = os.path.basename(image)
		print("Remove {0}".format(image))
		image = images_dir+image
		os.remove(image)

# Read the log and give informations
def read_log(test_dir_name):

	print("Reading log")

	with open(test_dir_name+"log.txt", "r") as f:
		log = f.read()

	infos = []

	pt = 0

	for i in range(3):
		idx = log.find("timing", pt)
		start = log.find('\n', idx) + 1
		end = log.find('\n', start)
		pt = end
		infos.append(log[start:end])

	print("Timing infos :")

	print("\n".join(infos))

# Move test_dir in working directory
def keep_result(test_dir_name):

	move(test_dir_name, ".")

def correct_nvm(test_dir_name, dirpath):

	nvm_path = test_dir_name+"sfm.nvm"

	if dirpath[-1] != '/':
		dirpath = dirpath + '/'

	with open(nvm_path, 'r') as f:
		nvm = f.read()

	new_nvm = nvm.replace("images/", dirpath)

	with open(nvm_path, 'w') as f:
		f.write(new_nvm)

def main():

	if len(sys.argv) < 3:
		print("You must give a directory name and a number of images.")
		exit(-1)

	dirpath = sys.argv[1]

	try:
		number = int(sys.argv[2])
	except ValueError:
		print("You must give a valid number of images.")
		exit(0)

	test_dir_name, images_to_test = choose_image(dirpath, number)
	setup_dir(test_dir_name, images_to_test)

	start_sfm(test_dir_name)

	clean_dir(test_dir_name, images_to_test)

	read_log(test_dir_name)

	keep_result(test_dir_name)

	correct_nvm(test_dir_name, dirpath)

if __name__ == '__main__':
	main()
