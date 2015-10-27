import numpy as np 
import matplotlib.pyplot as plt

def plot_2d(data, x, y):

	try :
		xx = [d[x] for d in data]
	except KeyError:
		print("There's no \"{0}\" information in data".format(x))
		return -1

	try :
		yy = [d[y] for d in data]
	except KeyError:
		print("There's no \"{0}\" information in data".format(y))
		return -1

	print(xx)
	print(yy)

	plt.plot(xx, yy)
	plt.show()