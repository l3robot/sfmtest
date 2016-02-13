#!/usr/bin/env python

import sys
import os
import math

import numpy as np

from PIL import Image
from PIL.ExifTags import TAGS

from src.common import testdir

class Camera(object):

	def __init__(self, company, model, width):
		self.company = company
		self.model = model
		self.width = width[:-1]

	def create_line(self):
		return '{};{};{}'.format(self.company, self.model, self.width)

def load_database(database):

	cameras = []

	with open(database, 'r') as f:
		for line in f:
			company, model, width = line.split(';')
			cameras.append(Camera(company, model, width))

	return cameras

def get_exif(img):

	exif = img._getexif()

	new_exif = {}

	if exif is None:
		return None

	for t, v in exif.items():
		str_v = TAGS.get(t, t)
		new_exif[str_v] = v

	return new_exif

def read_exif(image):

	with Image.open(image) as img:
		exif = get_exif(img)

	if exif is None:
		print("ERROR WHILE READING EXIF {}".format(image))
		return None
	try:
		company = exif['Make']
		model = exif['Model']
	except KeyError:
		print("ERROR WHILE READING EXIF {}".format(image))
		return None

	return Camera(company, model, '')

def compute_score(cam, ref, verbose=False):
	scam = cam.lower()
	sref = ref.lower()

	if verbose:
		print('{} {}'.format(scam, sref))

	lcam = len(scam)
	lref = len(ref)
	
	if lcam > lref:
		t = scam
		scam = sref
		sref = t
		t = lcam 
		lcam = lref
		lref = t 

	lpad = lref - lcam

	scores = []

	for i in range(lpad+1):

		tcam = ' '*i + scam + ' '*(lpad-i)

		if lpad > 0:
			tscore = math.ceil(math.log(lpad))
		else:
			tscore = 0

		truc = []

		for c, r in zip(list(tcam), list(sref)):
			if verbose:
					print('{} {} {}'.format(lpad, c,r))
			if c == ' ':
				truc.append('0')
				tscore += 0
			elif c != r:
				tscore += 1
				truc.append('1')
			else:
				truc.append('0')

		scores.append(tscore)
		if verbose:
			print('------')
			print('tcam : {}'.format(tcam))
			print('sref : {}'.format(sref))
			print(' =   : {}'.format(''.join(truc)))
			print('tscore : {}'.format(tscore))
			print('------')

	return 100.0 - (float(min(scores)) / float(lcam) * 100.0)

def eliminate_company(img, cameras):
	scores = []

	for c in cameras:
		t_score = compute_score(img.company, c.company)
		scores.append(t_score)

	kept_cameras = []

	score = np.min(scores)

	for c, s in zip(cameras, scores):
		if s == score:
			kept_cameras.append(c)

	return kept_cameras, score

def eliminate_model(img, cameras):

	scores = []

	for c in cameras:
		t_score = compute_score(img.model, c.model)
		scores.append(t_score)

	kept_cameras = []

	score = np.min(scores)

	for c, s in zip(cameras, scores):
		if s == score:
			kept_cameras.append(c)

	return kept_cameras, score

def main():

	if len(sys.argv) < 4:
		print("You must give a directory name, a number of images and database.")
		exit(-1)

	dirpath, number, database = sys.argv[1:4]

	try:
		number = int(number)
	except ValueError:
		print("You must give a valid number of images.")
		exit(0)

	test_dir_name, images_to_test = testdir.choose_image(dirpath, number, '-SWCD')
	testdir.setup_dir(test_dir_name, images_to_test)

	cameras = load_database(database)

	dirpath = test_dir_name+"images/"

	images = [os.path.join(dirpath, im) for im in os.listdir(dirpath)]

	new_database = []
	new_file = []

	models = []

	for image in images:
		image_camera = read_exif(image)

		if image_camera is None:
			continue

		if image_camera.model not in models:
			kept_cameras, company_score = eliminate_company(image_camera, cameras)
			kept_cameras, model_score = eliminate_model(image_camera, kept_cameras)
			camera = kept_cameras[0]

			image_camera.width = camera.width
			new_database.append(image_camera.create_line())

			infos = 'image : {} -- ref : {} -- scores {} {}'.format(image_camera.create_line(), camera.create_line(), company_score, model_score)
			new_file.append(infos)
			print(infos)
			models.append(image_camera.model)

	with open(test_dir_name+"result.txt", 'w') as f:
		f.write('\n'.join(new_file))

	with open(test_dir_name+"sw_database.txt", 'w') as f:
		f.write('\n'.join(new_database))

	testdir.clean_dir(test_dir_name, images_to_test)

	testdir.keep_result(test_dir_name)

if __name__ == '__main__':
	main()