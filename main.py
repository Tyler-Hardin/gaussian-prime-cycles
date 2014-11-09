#!/usr/bin/python
import numpy as np

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d

from plot import *
from common import *
from debug import *
  
d = [1, 0]
rot = [[0,-1],[1,0]]
l = 10

plot_class_len_vs_grid_len(l, d, rot)
#plot_init_vs_cycle_len(10, d, rot)
#plot_init_vs_cycle_len(20, d, rot)
#plot_init_vs_cycle_len(30, d, rot)
