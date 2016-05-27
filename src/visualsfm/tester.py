from subprocess import call
import numpy as np

# Infos #####################

sfm_command = ["VisualSFM", "sfm+pmvs"] 

#############################

class Tester:

    def __init__(self, test_dir_name):

        self.test_dir_name = test_dir_name
        self.log_file = test_dir_name+"log.txt"

        self.command = command = sfm_command + [(test_dir_name + "images"),\
         (test_dir_name + "sfm.nvm")]

    def start(self):

        print("Starting Tests with VisualSFM ...")

        with open(self.log_file, "w") as f:
            call(self.command, stdout=f)

        print("End of VisualSFM process")