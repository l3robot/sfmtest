import numpy as np

class Log:

	def __init__(dirpath):

		self.logpath = dirpath+"log.txt"

		start = dirpath.find("sfmtest-")

		if start < 0:
			self.dataset = "unknown"
		else:
			start += len("sfmtest-")
			end = dirpath.find("_")
			self.dataset = dirpath[start:end]

		with open(logpath, "r") as f:
			self.log = f.read()

		self.data = {'dataset': self.dataset}

	def parse(startStr, endStr, pt): # It might be not necessary

		pt = self.log.find(startStr, pt)
		if pt < 0:
			return (pt, 'None')
		start = pt + len(startStr)
		end = self.log.find(endStr, start)
		pt = end
		return (pt, self.log[start:end])

	def parseLine(theStr, pt):

		pt = self.log.find(theStr, pt)
		if pt < 0:
			return (pt, 'None')
		while log[pt-1] != '\n':
			pt-=1
		return parse(log[pt], '\n', pt)

	def parse_image_infos():

		pt = 0
		images = []

		while 1:
			image = {}

			pt, line = parseLine("SIFT:")
			if pt == -1:
				print("Found {0} images".format(len(images)))
				break

			line = line(5:).split(',')

			image['id'] = int(line[0])
			image_size = line[1].split('x')
			image['size'] = int(image_size[0])*int(image_size[1])
			image['nb_sift'] = int(line[2])
			timing = line[3]
			image['t_sift'] = int(timing[:timing.find('s')])

			images.append(image)

		self.data['nb_images'] = len(images)
		self.data['images'] = images

	def parse_matches_infos():

		pt = 0
		matches = []

		while 1:
			match = {}

			pt, line = parseLine("matches, ")
			if pt == -1:
				print("Found {0} matches".format(len(matches)))
				break

			iamges, infos = line.split(':')

			images = images.split('and')
			match['id'] = [int(images[0]), int(images[1])]

			infos = infos.split(',')

			nb_matches = infos[0]
			t_matches = infos[1]

			match['nb_matches'] = int(nb_matches[:nb_matches.find(' m')])
			match['t_matches'] = int(t_matches[:t_matches.find(' s')])

			matches.append(match)

		self.data['matches'] = matches		

