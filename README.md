Structure From Motion Tester
============================

This project is used to test the performance of a structure from motion algorithm pipeline.


- sfmtest.py [Implementation] [images folder] [number of images]
- readlog.py [folder] [--all|--all-no-print]
- crawldata.py [folder] [images|matches] [xaxis] [yaxis]

Example with VisualSFM
----------------------
sfmtest.py -V [images folder] [number of images]

Example with OpenMVG
----------------------
sfmtest.py -O [images folder] [number of images]

Dependencies
------------
- VisualSFM : Executable in PATH
- OpenMVG : python scripts in PATH)
- CMVS/PMVS : executable in PATH (good tutorial for installation : http://adinutzyc21.blogspot.ca/2013/02/installing-bundler-on-linux-tutorial.html)


