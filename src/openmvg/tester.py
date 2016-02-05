from subprocess import call
import numpy as np

import sys

# Infos #####################

sfm_command = ["SfM_GlobalPipeline.py"] 

#############################

class Tester:

	def __init__(self, test_dir_name):

		self.test_dir_name = test_dir_name
		self.log_file = test_dir_name+"log.txt"

		self.command = command = sfm_command + [(test_dir_name + "images"),\
		 (test_dir_name + "results")]

	def start(self):

		print("Starting Tests with OpenMVG ...")

		with open(self.log_file, "w") as f:
			call(self.command, stdout=f)

		print("End of OpenMVG process")