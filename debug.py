from common import *

def check_equal():
  d = [1,0]
  rot = [[0,-1],[1,0]]
  P = find_cycle([-1,0], d, rot)[0]
  Q = find_cycle([-1,1], d, rot)[0]
  assert equal(P, Q)
  
  P = find_cycle([-1,0], d, rot)[0]
  Q = find_cycle([-1,-1], d, rot)[0]
  assert not equal(P, Q)
