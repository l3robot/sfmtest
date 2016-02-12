#!/usr/bin/env python

import sys
import os

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

	for t, v in exif.items():
		str_v = TAGS.get(t, t)
		new_exif[str_v] = v

	return new_exif

def read_exif(image):

	with Image.open(image) as img:
		exif = get_exif(img)

	company = exif['Make']
	model = exif['Model']

	return Camera(company, model, '')

def compute_score(cam, ref, verbose=False):
	scam = cam.lower()
	sref = ref.lower()

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

		tscore = 0
		truc = []

		for c, r in zip(list(tcam), list(sref)):
			if c == ' ':
				truc.append('0')
				tscore += 0
			elif c != r:
				if verbose:
					print('{} {} {}'.format(lpad, c,r))
				tscore += 1
				truc.append('1')

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

	score = 0.0

	for i, c in enumerate(cameras):
		t_score = compute_score(img.company, c.company)
		if t_score > score:
			score = t_score
			start = i
			end = i
			# print('New Potential Data : {} -- camera : {} -- ref : {}'.format(t_score, img.create_line(), c.create_line()))
		elif t_score == score:
			# print('New Potential Data : {} -- camera : {} -- ref : {}'.format(t_score, img.create_line(), c.create_line()))
			end = i

	# print('** Found {} potential camera by company -- max score : {}**'.format(end-start+1, score))

	return cameras[start:end+1], score

def eliminate_model(img, cameras):

	score = 0.0

	for i, c in enumerate(cameras):
		t_score = compute_score(img.model, c.model)
		if t_score > score:
			score = t_score
			start = i
			end = i
			# print('New Potential Data : {} -- camera : {} -- ref : {}'.format(t_score, img.create_line(), c.create_line()))
		elif t_score == score:
			# print('New Potential Data : {} -- camera : {} -- ref : {}'.format(t_score, img.create_line(), c.create_line()))
			end = i

	# print('** Found {} potential camera by model -- max score : {}**'.format(end-start+1, score))

	return cameras[start:end+1], score

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

	new_file = []

	for image in images:
		image_camera = read_exif(image)
		kept_cameras, company_score = eliminate_company(image_camera, cameras)
		kept_cameras, model_score = eliminate_model(image_camera, kept_cameras)
		camera = kept_cameras[0]
		print('image : {} -- ref : {} -- scores {} {}'.format(image_camera.create_line(), camera.create_line(), company_score, model_score))

	testdir.clean_dir(test_dir_name, images_to_test)

	testdir.keep_result(test_dir_name)

if __name__ == '__main__':
	main()