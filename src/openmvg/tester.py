from subprocess import call
import numpy as np

import os
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

        #with open(self.log_file, "w") as f:
        call(self.command)

        print("End of OpenMVG process")

    def dense(self):

        print("Making dense reconstruction")

        results = os.path.join(self.test_dir_name, "results/reconstruction_global")
        results_json = os.path.join(results, "sfm_data.json")

        command = "openMVG_main_openMVG2PMVS -i {} -o {}".format(results_json, results)
        os.system(command)

        pmvs = os.path.join(results, "PMVS/")

        command = "pmvs2 {} pmvs_options.txt".format(pmvs)
        os.system(command)

