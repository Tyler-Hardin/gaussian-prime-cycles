import numpy as np
import sys

def simple_prime(n, prime_lst):
  for i in prime_lst:
    if i >= n:
      break
    if n % i == 0:
      return False
  return True

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
  return P, count, True

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
# Ps = [[Path, Path, ...], [Path, Path, ...], ...]
# X = [[x init, x init, ...], [x init, x init, ...], ...]
# Y = [[y init, y init, ...], [y init, y init, ...], ...]
# such that P[i][j] is the path with initial point (X[i][j], Y[i][j]).
#
# Returns a list of eq. classes of the form:
# [class, ...]
# such that class = [representative path, [init set]]
# such that init set = set([(x,y), ...])
def classes(Ps, X, Y):
  Ps = tuple(tuple(p for p in P) for P in Ps)
  class_lst = []
  for i in range(len(Ps)):
    for j in range(len(Ps[i])):
      P = Ps[i][j]
      x = X[i][j]
      y = Y[i][j]
      
      # Search reps of existing classes to see if one is equiv to P
      new_cls = True
      for cls in class_lst:
        Q = cls[0]
        
        # If equal, append (x,y) to classes init point list.
        if equal(P, Q):
          print x, y, 'not new'
          cls[1].add((x,y))
          new_cls = False
          break
        
      # If not, create a new class.
      if new_cls:
        print x, y, 'new'
        class_lst.append([P, set([(x,y)])])
      
      if len(class_lst) == 0:
        class_lst.append([P, set([(x,y)])])
        
  return class_lst
































