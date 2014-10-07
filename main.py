#!/usr/bin/python
import numpy as np

from mpl_toolkits.mplot3d import axes3d

from plot import *
from common import *
from debug import *

def grid(l, d, rot):
  res = []
  X = []
  Y = []
  for x in range(0, l):
    X.append([])
    Y.append([])
    res.append([])
    for y in range(0, l):
      P, count, found = find_cycle((x,y), d, rot)
      #print x, y, count, found
      X[-1].append(x)
      Y[-1].append(y)
      if found:
#        plot_cycle(P, filename=str(d)+ '_' + str([x,y]) + '.svg', show=False)
        res[-1].append(P)
      else:
        res[-1].append(None)
  
  return res, X, Y
  
d = [1, 0]
rot = [[0,-1],[1,0]]

Ps, X, Y = grid(20, d, rot)

cls = classes(Ps, X, Y)
cls = sorted(cls, key=lambda c : len(c[0]))

print len(cls), 'classes'
for i in cls:
  plot_cycle(i[0], filename=str(tuple(d))+ '_' + \
  str(tuple(next(iter(i[1])))) + '.svg', show=False)

i = 0
for c in cls:
  print c[1]
  print i
  X = []
  Y = []
  for pt in c[1]:
    X.append(pt[0])
    Y.append(pt[1])
  plt.scatter(X, Y, c=str(float(i) / len(cls)), s=50)
  
  i += 1
plt.show()
#check_equal()
