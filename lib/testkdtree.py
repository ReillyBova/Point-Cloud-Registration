# Author:  Reilly Bova '20
# Date:    11 November 2018
# Project: COS 526 A2 — Point Cloud Registration
#
# File:    testkdtree.py
# About:   A simple script that tests kdtree.py

from .kdtree import KdTree
from .point import Point
from random import random

# Basic functionality test
t = KdTree()
p1 = Point([1, 2, 3])
p2 = Point([5, -4, 9])
p3 = Point([100, -29, 30])
t.insert(p1)
t.insert(p2)
t.insert(p1)
t.insert(p3)
assert(t.nearest(Point([99, -28, 37])).s == p3.s)

def bruteForce_nearest(p, points):
    if (len(points) == 0):
        return None
    pbest = points[0]
    dist_best = p.distSqdTo(pbest)

    for ptest in points:
        dist_test = p.distSqdTo(ptest)
        if (dist_test < dist_best):
            dist_best = dist_test
            pbest = ptest

    return pbest

print("Passed basic test")

# Insert 1000 random nD points
for d in range(1,6):
    t = KdTree(d)
    points = []
    for i in range(5000):
        p = Point([(random()*2000.0 - 1000.0) for j in range(d)])
        points.append(p)
        t.insert(p)

    # test 1000 points
    for i in range(1000):
        p = Point([(random()*2000.0 - 1000.0) for j in range(d)])
        q = t.nearest(p)
        b = bruteForce_nearest(p, points)

        assert(p.distSqdTo(q) == p.distSqdTo(b))

print("Passed consistency test")

# Stress it
t = KdTree(5)
points = []
for i in range(1000000):
    p = Point([(random()*2000.0 - 1000.0) for j in range(d)])
    points.append(p)
    t.insert(p)

print("Starting stress test with 1 million point tree....")

# Test 5 Points
for i in range(5):
    p = Point([(random()*2000.0 - 1000.0) for j in range(d)])
    #print("Starting kdtree search....")
    q = t.nearest(p)
    #print("Starting brute search....")
    b = bruteForce_nearest(p, points)
    assert(p.distSqdTo(q) == p.distSqdTo(b))

    #print(p.s)
    #print(q.s)
    #print(b.s)
    #print()

print("Passed all tests")
