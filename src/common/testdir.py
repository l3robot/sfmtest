import random
import sys
import os
import time

import numpy as np

from shutil import copy, move

# Infos #####################

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
def choose_image(dirpath, number, algo):

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

	images = [os.path.join(dirpath, im) for im in os.listdir(dirpath)\
	if file_and_image(dirpath, im)]

	try:
		idx = random.sample(range(0,len(images)), int(number))
	except ValueError:
		print("Not enough images, will take all images.")
		number = len(images)
		idx = random.sample(range(0,len(images)), int(number))

	images_kept = [im for i, im in enumerate(images) if i in idx]

	test_dir_name = test_dir+"sfmtest"+algo+'-'+dirname+"_"+str(number)+"img"+"-"+test_time+"/"

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

# Erase images in test_dir/images
def clean_dir(test_dir_name, images_to_test):

	print("Clean sfmtest directory")

	images_dir = test_dir_name+"images/"

	for image in images_to_test:
		image = os.path.basename(image)
		print("Remove {0}".format(image))
		image = images_dir+image
		os.remove(image)

# Move test_dir in working directory
def keep_result(test_dir_name):

	move(test_dir_name, ".")

def correct_nvm(test_dir_name, dirpath):

	nvm_path = test_dir_name+"sfm.nvm"

	nvm_bp_path = nvm_path + ".bp"

	copy(nvm_path, nvm_bp_path)

	if dirpath[-1] != '/':
		dirpath = dirpath + '/'

	with open(nvm_path, 'r') as f:
		nvm = f.read()

	new_nvm = nvm.replace("images/", dirpath)

	with open(nvm_path, 'w') as f:
		f.write(new_nvm)