import numpy as np 
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

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

	f = np.polyfit(xx, yy, 1)
	p = np.poly1d(f)

	plt.plot(np.log(xx), yy, 'r.')
	plt.title('Crawled on {0} images ~ y = {1:.2e}x + {2:.2e}'.format(len(data), f[0], f[1]))
	plt.xlabel('log({0})'.format(x))
	plt.ylabel('{0}'.format(y))

	ma = np.max(xx)
	mi = np.min(xx)

	xnew = np.linspace(mi, ma)
	plt.plot(np.log(xnew), p(xnew), 'b-')
	plt.show()