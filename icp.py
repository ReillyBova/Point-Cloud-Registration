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
from math import *
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
    M1 = np.identity(4)
else:
    M1 = load_xf(file1_xf)

# NB need to load "output" file2.xf if avaliable or will overwrite previous work
output_file2_xf = './output/' + file2_xf.split('/')[-1]
if (not os.path.isfile(output_file2_xf)):
    if (not os.path.isfile(file2_xf)):
        print("Warning: Could not find .xf file: " + file2_xf)
        print("Defaulting to 4x4 identity matrix...")
        M2 = np.identity(4)
    else:
        M2 = load_xf(file2_xf)
else:
    print("Using the transformation {} as target".format(output_file2_xf))
    M2 = load_xf(output_file2_xf)

# Build a kdtree out of the points in file 2
print("Building KdTree from {}...".format(file2))
kdtree = KdTree()
for p in pts2:
    kdtree.insert(p)

# ICP iteration (until improvement is less than 0.01%)
print("Starting iteration...")
ratio = 0.0
M2_inverse = M2.I
pts_index = [i for i in range(len(pts1))]
count = 0
while (ratio < 0.9999):
    # Randomly pick 1000 points
    shuffle(pts_index)
    # Apply M1 and the inverse of M2
    p = [pts1[i].copy().transform(M1).transform(M2_inverse) for i in pts_index[:1000]]
    q = [kdtree.nearest(point) for point in p]

    # Compute point to plane distances
    point2plane = [abs(np.subtract(pi.s, qi.s).dot(qi.n)) for pi,qi in zip(p,q)]
    median_3x = 3.0 * np.median(point2plane)

    # Cull outliers
    point_pairs = []
    dist_sum = 0.0
    for i, pair in enumerate(zip(p,q)):
        if (point2plane[i] <= median_3x):
            point_pairs.append(pair)
            dist_sum += point2plane[i]
    if (len(point_pairs) > 0):
        old_mean = dist_sum/len(point_pairs)
    else:
        print("Error: Something went wrong when computing distance means")
        quit()

    # Construct C and d
    C = np.zeros(shape=(6,6))
    d = np.zeros(shape=(6,1))
    for (p, q) in point_pairs:
        Ai = np.matrix(np.append(np.cross(p.s, q.n),q.n))
        AiT = Ai.T
        bi = np.subtract(q.s, p.s).dot(q.n)

        C += AiT*Ai
        d += AiT*bi

    # Solve the linear system of equations and compute Micp
    x = np.linalg.solve(C,d).flatten()
    rx,ry,rz,tx,ty,tz = x
    Micp = np.matrix([[1.0, ry*rx - rz, rz*rx + ry, tx],[rz, 1.0 + rz*ry*rx, rz*ry - rx, ty], [-ry, rx, 1.0, tz], [0, 0, 0, 1.0]])

    # Compute new mean point-to-plane distance
    dist_sum = 0.0
    for (p, q) in point_pairs:
        # Apply Micp
        p = p.transform(Micp)
        dist_sum += abs(np.subtract(p.s, q.s).dot(q.n))
    new_mean = dist_sum/len(point_pairs)
    count += 1
    ratio = new_mean / old_mean

    # Update M1 iff we improved (otherwise, but NOT only then, we will terminate)
    if (ratio < 1.0):
        M1 = M2*Micp*M2_inverse*M1
    else:
        new_mean = old_mean

    print("Finished iteration #{} with improvement of {:2.4%}".format(count, 1.0 - ratio))

print("Terminated successfully with a sampled mean distance of {}".format(new_mean))

# Write results to file
output_file1_pts = './output/' + file1.split('/')[-1]
output_file1_xf = './output/' + file1_xf.split('/')[-1]
output_file2_pts = './output/' + file2.split('/')[-1]
output_file2_xf = './output/' + file2_xf.split('/')[-1]
write_pts(output_file1_pts, pts1)
write_pts(output_file2_pts, pts2)
write_xf(output_file1_xf, M1)
write_xf(output_file2_xf, M2)

# All finished
quit()
