import numpy as np 
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

def plot_2d(data, x, y, log=True):

    try :
        xx = [d[x] for d in data if isinstance(d, dict)]
    except KeyError:
        print("plotting : There's no \"{0}\" information in data".format(x))
        return -1

    try :
        yy = [d[y] for d in data if isinstance(d, dict)]
    except KeyError:
        print("plotting : There's no \"{0}\" information in data".format(y))
        return -1

    if log:
        xx = np.log(xx)
        xlabel = 'log({0})'.format(x)
    else:
        xlabel = '{0}'.format(x)

    f = np.polyfit(xx, yy, 1)
    p = np.poly1d(f)

    plt.plot(xx, yy, 'r.')
    plt.title('Crawled on {0} results ~ y = {1:.2e}x + {2:.2e}'.format(len(data), f[0], f[1]))
    plt.xlabel(xlabel)
    plt.ylabel('{0}'.format(y))

    ma = np.max(xx)
    mi = np.min(xx)

    xnew = np.linspace(mi, ma)
    plt.plot(xnew, p(xnew), 'b-')
    plt.show()