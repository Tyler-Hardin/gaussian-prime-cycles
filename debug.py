from common import *

d = [1,0]
rot = [[0,-1],[1,0]]

def check_equal():
  P = find_cycle([-1,0], d, rot)[0]
  Q = find_cycle([-1,1], d, rot)[0]
  assert equal(P, Q)
  
  P = find_cycle([-1,0], d, rot)[0]
  Q = find_cycle([-1,-1], d, rot)[0]
  assert not equal(P, Q)

def chech_partition(l):
  Ps = grid(l, d, rot)
  cls = classes(Ps)
  
  for i in range(len(cls)):
    for j in range(len(cls)):
      if i == j:
        continue
      
      if cls[i].init_points & cls[j].init_points != set():
        print cls[i].path.x, cls[i].path.y, cls[i].init_points
        print cls[j].path.x, cls[j].path.y, cls[j].init_points
        plot_cycle(cls[i].path)
        plot_cycle(cls[j].path)

def check_class(cls):
  for i in cls.init_points:
    plot_cycle(find_cycle((i[0], i[1]), d, rot))

#Ps = grid(7, d, rot)
#for P in Ps:
#  print P.x, P.y
#cls = classes(Ps)
#check_class(cls[2])
#chech_partition(5)
