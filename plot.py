import matplotlib.pyplot as plt
import numpy as np

from common import *

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
  
  if 'filename' in kwargs:
  	plt.savefig(kwargs['filename'], dpi=1500)
  if kwargs.get('show', True):
  	plt.show()
  plt.close()

# Plots initial points and colors them by their class (all in the same class 
# have the same color), with points with longer paths being colored lighter.
def plot_classes(l, d, rot):
  Ps, X, Y = grid(l, d, rot)

  cls = classes(Ps, X, Y)
  cls = sorted(cls, key=lambda c : len(c[0]))

  print len(cls), 'classes'
  for i in cls:
    plot_cycle(i[0], filename=str(tuple(d))+ '_' + \
    str(tuple(next(iter(i[1])))) + '.svg', show=False)

  i = 0
  for c in cls:
    X = []
    Y = []
    for pt in c[1]:
      X.append(pt[0])
      Y.append(pt[1])
    plt.scatter(X, Y, c=str(float(i) / len(cls)), s=50)
    
    i += 1
  plt.xlim(-1, l)
  plt.ylim(-1, l)
  plt.show()

# Plots a line with x being the side length of the square grid being considered
# and y being the number of classes in the grid.
def plot_class_len_vs_grid_len(l, d, rot):
  assert l >= 2
  Xs = []
  Ys = []
  for i in range(2, l):
    Ps = grid(i, d, rot)
    cls = classes(Ps)
    Xs.append(i)
    Ys.append(len(cls))
  plt.plot(Xs, Ys)
  plt.show()
  
def plot_init_vs_cycle_len(l, d, rot):
  Ps = grid(l, d, rot)
  
  Xs = []
  Ys = []
  for P in Ps:
    x = P.x
    y = P.y
    Xs.append((x**2 + y**2)**.5)
    Ys.append(len(P))
      
  plt.scatter(Xs, Ys)
  plt.title('Intial point vs. Cycle length (l=' + str(l) +')')
  plt.xlabel('Distance from initial point to (0,0)')
  plt.ylabel('Length of cycle')
  plt.show()
