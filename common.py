import numpy as np
import sys

class Path:
  def __init__(self, lst, x, y):
    self.points = list(lst)
    self.x = x
    self.y = y
  
  def __getitem__(self, i):
    return self.points.__getitem__(i)
  
  def __getslice__(self, i, j):
    return self.points.__getslice__(i, j)
        
  def __len__(self):
    return len(self.points)
  
  def __list__(self):
    return self.points

def simple_prime(n, prime_lst):
  for i in prime_lst:
    if i >= n:
      break
    if n % i == 0:
      return False
  return True

class Class:
  def __init__(self, path, init_point):
    self.path = path
    self.init_points = set()
    self.init_points.add(init_point)
  
  def in_grid(self, l):
    for i in self.init_points:
      if 0 <= i[0] < l and 0 <= i[1] < l:
        return True
    return False
  
  def add_point(self, point):
    self.init_points.add(point)
  
def prime(n):
  if n <= 1:
    return False
    
  if n in prime.map:
    return prime.map[n]
  
  i = 0
  t = prime.lst[-1] - prime.lst[-1] % 6
  while prime.lst[-1] < n:
    if t + i * 6 + 1 > prime.lst[-1] and \
    simple_prime(t + i * 6 + 1, prime.lst):
      prime.lst.append(t + i * 6 + 1)
    if simple_prime(t + i * 6 + 5, prime.lst):
      prime.lst.append(t + i * 6 + 5)
    i += 1
    
  prime.map[n] = simple_prime(n, prime.lst)
  return prime.map[n]
prime.lst = [2, 3, 5, 7]
prime.map = {}

# Citation: http://math.stackexchange.com/a/151781/80413
def gaussian_prime(p):
  if p[0] == 0 or p[1] == 0:
    t = abs(p[0] + p[1])
    return t % 4 == 3 and prime(t)
  else:
    return prime(p[0]**2 + p[1]**2)

# p is the initial point (x,y)
# d is a vector representing the initial direction
# rot is a 2x2 list representing the rotation matrix
# End points are intentionally left off so as to only count primes 
# encountered.
#
# P = [(x,y), ...]
def find_cycle(p, d, rot, **kwargs):
  p = np.array([p])
  
  P = []
  initial = np.array(p)
  direction = np.array(d)
  
  rot_mat = np.array(rot)
  
  # The weird loop form is due to the lack of do-while loops in Python.
  count = 0
  while True:
    if gaussian_prime(p[0]):
      P.append(p[0].copy())
      direction = np.dot(rot_mat, direction.reshape((2,1))).reshape((1,2))
    
    p += direction
    
    if np.array_equal(p, initial) and np.array_equal(direction, [d]):
      break
    elif (p[0][0]-initial[0][0])**2 + (p[0][1]-initial[0][1])**2 > 1000000:
      print '(' + str(initial[0][0]) + ',' + str(initial[0][1]) + '), (' + \
        str(p[0][0]) + ',' + str(p[0][1]) + ')'
      print 'Cycle not found... len(P)=' + str(len(P))
      return P, count, False
    count += 1
  
  P.append(P[0].copy())
  return Path(P, initial[0][1], initial[0][1]), count, True

# Takes two points and returns the list of solns to the rot/trans transform
# equations.
# 
# ========== Internal structure of a soln
# solns: [theta, tx, ty]
#   theta: 0 = 0 rad, 1 = pi/2 rad, 2 = pi rad, 3 = 3pi/2 rad
#   tx: integer
#   ty: integer
def find_solns(p, q):
  x = p[0]
  y = p[1]
  xp = q[0]
  yp = q[1]
  return [(0, xp - x, yp - y), \
    (1, xp - y, yp + x), \
    (2, xp + x, yp + y), \
    (3, xp + y, yp - x)]

def check_soln(p, q, s):
  return s in find_solns(p, q)

# Returns the list of solns that when applied to all points in P, result in
# a point in Q. (Thus showing that P * soln is a subset of Q.)
def subset_solns(P, Q, try_solns = None):
  if P is None and Q is None:
    return True
  elif P is None or Q is None:
    return False
  
  possible_solns = set() if try_solns is None else set(try_solns)
  
  for q in Q:
    possible_solns |= set(find_solns(P[0], q))
  
  count = 0
  for p in P[1:]:
    p_Q_solns = set()
    for q in Q:
      p_Q_solns |= set(find_solns(p, q))
    
    possible_solns &= p_Q_solns
    if len(possible_solns) == 0:
      break
  
  return possible_solns

# Check if P is the same shape as Q, transformed or rotated.
def equal(P, Q):
  solns = subset_solns(P, Q)
  if len(solns) == 0:
    return False
  else:
    return len(subset_solns(Q, P, solns)) > 0

# Takes a list of cycles, x initials, and y initials and returns the
# equivalence classes based on translational/rotational equivalence.
# 
# Ps = [Path, ...]
#
# Returns a list of eq. classes of the form:
# [Class, ...]
# such that class = [representative path, [init set]]
# such that init set = set([(x,y), ...])
def classes(Ps):
  class_lst = []
  for P in Ps:
    x = P.x
    y = P.y
    
    # Search reps of existing classes to see if one is equiv to P
    new_cls = True
    for cls in class_lst:
      Q = cls.path
      
      # If equal, append (x,y) to classes init point list.
      if equal(P, Q):
        cls.add_point((x,y))
        new_cls = False
        break
      
    # If not, create a new class.
    if new_cls:
      class_lst.append(Class(P, (x,y)))
    
    if len(class_lst) == 0:
      class_lst.append(Class(P, (x,y)))
        
  return class_lst

# Takes a length, initial direction vector, and rotational matrix and 
# computes the cycles for all points in the square from (0,0) to (l-1,l-1), 
# inclusively.
#
# l = length of side of square
# d = [x_dir y_dir]
# rot = rotational matrix
#
# Returns P, a list of paths, and arrays X and Y such that P[i] is the path
# with initial point (X[i], Y[i]).
def grid(l, d, rot):
  res = []
  for x in range(0, l):
    for y in range(0, l):
      P, count, found = find_cycle((x,y), d, rot)
      if found:
        res.append(P)
      else:
        res.append(None)
  return res



























