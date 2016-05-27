#!/usr/bin/env python

import sys

import src.openmvg.tester as openmvg
import src.visualsfm.tester as visualsfm

from src.common import testdir

# infos ##############

imps = ['-O', '-OpenMVG', '-V', '-VisualSFM']

def main():

    if len(sys.argv) < 4:
        print("You must give an implementation, a directory name and a number of images.")
        exit(-1)

    algo, dirpath, number = sys.argv[1:4]

    try:
        number = int(number)
    except ValueError:
        print("You must give a valid number of images.")
        exit(0)

    if algo not in imps:
        print("You must give a valid sfm implementation.")
        exit(0)

    test_dir_name, images_to_test = testdir.choose_image(dirpath, number, algo)
    testdir.setup_dir(test_dir_name, images_to_test)

    if algo == "-O" or algo == "-OpenMVG":
        tester = openmvg.Tester(test_dir_name)
    elif algo == "-V" or algo == "-VisualSFM":
        tester = visualsfm.Tester(test_dir_name)

    tester.start()
    tester.dense()

    #testdir.clean_dir(test_dir_name, images_to_test)

    testdir.keep_result(test_dir_name)

if __name__ == '__main__':
    print(sys.__version__)
    exit()
    main()
