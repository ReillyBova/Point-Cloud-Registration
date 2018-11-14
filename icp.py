# Author:  Reilly Bova '20
# Date:    13 November 2018
# Project: COS 526 A2 — Point Cloud Registration
#
# File:    icp.py
# About:   Implements the Iterative Closest Points algorithm
#          Takes 2 *.pts files as the argument and tries to align the points of
#          the first file with those in the second. Expects *.xf to exist for
#          each file as well. Output appears in ./results

import os
import numpy as np
from sys import argv
from random import shuffle
from lib.utils import *
from lib.kdtree import KdTree

# Check usage
if (len(argv) != 3):
    print("Usage Error: icp.py takes additional two arguments.\n"
            "Proper usage is \"icp.py file1.pts file2.pts\"")
    quit()

# Check if pts files exist
file1 = argv[1]
file2 = argv[2]
if (not os.path.isfile(file1)):
    print("Error: Could not find .pts file: " + file1)
    quit()
if (not os.path.isfile(file2)):
    print("Error: Could not find .pts file: " + file2)
    quit()

# Load pts
pts1 = load_pts(file1)
pts2 = load_pts(file2)

# Check if xf files exist
file1_xf = '.'.join(file1.split('.')[:-1]) + '.xf'
file2_xf = '.'.join(file2.split('.')[:-1]) + '.xf'
if (not os.path.isfile(file1_xf)):
    print("Warning: Could not find .xf file: " + file1_xf)
    print("Defaulting to 4x4 identity matrix...")
    m1 = np.matrix([[1.0,0,0,0],[0,1.0,0,0],[0,0,1.0,0],[0,0,0,1.0]])
else:
    m1 = load_xf(file1_xf)
if (not os.path.isfile(file2_xf)):
    print("Warning: Could not find .xf file: " + file2_xf)
    print("Defaulting to 4x4 identity matrix...")
    m2 = np.matrix([[1.0,0,0,0],[0,1.0,0,0],[0,0,1.0,0],[0,0,0,1.0]])
else:
    m2 = load_xf(file2_xf)

# Build a kdtree out of the points in file 2
kdtree = KdTree()
for p in pts2:
    kdtree.insert(p)

# ICP iteration (until improvement is less than 0.01%)
ratio = 0.0
m2_inverse = m2.I
pts_index = [i for i in range(len(pts1))]
while (ratio < 0.9999):
    # Randomly pick 1000 points
    shuffle(pts_index)
    # Apply M1 and the inverse of M2
    p = [pts1[i].copy().transform(m1).transform(m2_inverse) for i in pts_index[:1000]]
    q = [kdtree.nearest(point) for point in p]

    break

print([qp.n for qp in q[:10]])
