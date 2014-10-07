import matplotlib.pyplot as plt
import numpy as np

def plot_cycle(P, **kwargs):
  X = []
  Y = []
  
  for p in P:
    X.append(p[0])
    Y.append(p[1])
  
  X = np.array(X)
  Y = np.array(Y)
  
  lim_offset = 1
  plt.xlim((min(X) - lim_offset, max(X) + lim_offset))
  plt.ylim((min(Y) - lim_offset, max(Y) + lim_offset))
  
  w = max(X) - min(X)
  h = max(Y) - min(Y)
  plt.quiver(X[:-1], Y[:-1], X[1:]-X[:-1], Y[1:]-Y[:-1], \
    scale_units='xy', angles='xy', scale=1, \
    width=plt.gcf().get_figwidth()*.0005, \
    headwidth=2, headlength=3)
  
  if 'filename' in kwargs:
  	plt.savefig(kwargs['filename'], dpi=1500)
  if kwargs.get('show', True):
  	plt.show()
  plt.close()
