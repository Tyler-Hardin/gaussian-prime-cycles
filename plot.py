import matplotlib.pyplot as plt
import matplotlib.cm
import numpy as np

from common import *

# Abstracts calls to plt.{savefig,show,close)() to allow for common interface
# for supressing show and or saving in all plot commands in this module.
def plot(kwargs):
  if 'filename' in kwargs:
  	plt.savefig(kwargs['filename'], dpi=600)
  if kwargs.get('show', True):
  	plt.show()
  plt.close()
  
# Plots a single path from find_cycle(...).
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
  
  plot(kwargs.get('plot_args', {}))

# Plots initial points and colors them by their class (all in the same class 
# have the same color), with points with longer paths being colored lighter.
def plot_classes(l, d, rot):
  Ps = grid(l, d, rot)

  cls = classes(Ps)
  cls = sorted(cls, key=lambda c : len(c.path))

  print len(cls), 'classes'
  for i in cls:
    plot_cycle(i.path, plot_args={'filename':'classes/' + str(tuple(d))+ '_' + \
    str(tuple(next(iter(i.init_points)))), 'show':False})

  cm = plt.cm.get_cmap('nipy_spectral')
  i = 0.0
  X = []
  Y = []
  color_lst = []
  for c in cls:
    for pt in c.init_points:
      X.append(pt[0])
      Y.append(pt[1])
      color_lst.append(i)
    i += 1
    #plt.scatter(X, Y, c=str(float(i) / len(cls)), s=50)
  plt.scatter(X, Y, c=color_lst, s=50, cmap=cm)
    
  plt.xlim(-1, l)
  plt.ylim(-1, l)
  plt.show()

# Plots a line with x being the side length of the square grid being considered
# and y being the number of classes in the grid.
def plot_class_len_vs_grid_len(l, d, rot, **kwargs):
  assert l >= 2
  Xs = []
  Ys = []
  
  Ps = grid(l, d, rot)
  cls = classes(Ps)
  for i in range(2, l):
    Xs.append(i)
    count = 0
    # Count classes in (0,0),(i,i) grid
    for c in cls:
      if c.in_grid(i):
        count += 1
    Ys.append(count)
  plt.plot(Xs, Ys)
  #plt.title('Grid size vs. Number of classes')
  plt.xlabel('Grid size')
  plt.ylabel('Number of classes')
  plot(kwargs.get('plot_args', {}))
  
def plot_init_vs_cycle_len(l, d, rot, **kwargs):
  Ps = grid(l, d, rot)
  
  Xs = []
  Ys = []
  for P in Ps:
    x = P.x
    y = P.y
    Xs.append((x**2 + y**2)**.5)
    Ys.append(len(P))
      
  plt.scatter(Xs, Ys)
  #plt.title('Intial point vs. Cycle length (l=' + str(l) +')')
  plt.xlabel('Distance from initial point to (0,0)')
  plt.ylabel('Length of cycle')
  
  plot(kwargs.get('plot_args', {}))
