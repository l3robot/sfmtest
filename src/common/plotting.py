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

	plt.plot(np.log(xx), yy, 'r.')
	plt.xlabel('log({0})'.format(x))
	plt.xlabel('{0}'.format(y))
	plt.show()