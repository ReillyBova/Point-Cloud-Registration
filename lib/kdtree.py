# Author:  Reilly Bova '20
# Date:    11 November 2018
# Project: COS 526 A2 — Point Cloud Registration
#
# File:    kdtree.py
# About:   Implements an kdtree of points

from math import *
from .box import Box
from .point import Point

# Node class to maintain data structure
class Node:
    # Accepts a point, a float, and a box as it's input
    def __init__(self, p, key, bounds):
        # Key associated with node (dimension coord)
        self.key = key

        # Point associated with node
        if (type(p) == Point):
            self.p = p
        else:
            self.p = None

        # Bounds associated with node
        self.bounds = bounds
        if (type(bounds) == Box):
            self.bounds = bounds
        else:
            self.bounds = None

        # Left and right links
        self.left = None
        self.right = None

# A kdtree
class KdTree:
    # Constructor takes int k defining the number of dimensions
    def __init__(self, k=3):
        self.k = k
        self.size = 0
        self.root = None
        self.minP = [-inf for i in range(k)]
        self.maxP = [inf for i in range(k)]

    # External method for inserting points
    def insert(self, p):
        if (type(p) != Point):
            print("Error: Insert method not provided a valid point")
            return
        if (p.d != self.k):
            print("Error: Point and KdTree must have same dimensionality")
            return

        bounds = Box(Point(self.minP), Point(self.maxP))
        self.root = self.put(self.root, p, 0, bounds)

    # Internal method for inserting points
    def put(self, node, p, dim, bounds):
        # Base case
        if (node == None):
            self.size += 1
            key = p.s[dim]
            return Node(p, key, bounds)

        # Compare the point to the node and proceed accordingly
        cmp = p.s[dim] - node.key
        if (cmp < 0):
            # Go left if smaller; update upper bounds
            upperBounds = bounds.copy()
            upperBounds.updateMax(node.key, dim)
            node.left = self.put(node.left, p, (dim + 1) % self.k, upperBounds)
        else:
            # Go right otherwise; update lower bounds
            lowerBounds = bounds.copy()
            lowerBounds.updateMin(node.key, dim)
            node.right = self.put(node.right, p, (dim + 1) % self.k, lowerBounds)

        return node

    # Returns nearest neighbor in kdtree to point p; Returns None if the tree is
    #   empty
    def nearest(self, p):
        if (type(p) != Point):
            print("Error: Nearest method not provided a valid point")
            return
        if (p.d != self.k):
            print("Error: Point and KdTree must have same dimensionality")
            return
        # corner case that there are no nearest points (kd tree is empty)
        if (self.size == 0):
            return None

        # Start at the root and recursively search in both subtrees using the
        # following pruning rule: if the closest point discovered so far is
        # closer than the distance between the query point and the Box
        # corresponding to a node, there is no need to explore that node
        # (or its subtrees). That is, we should search a node only if it might
        # contain a point that is closer than the best one found so far.

        # The effectiveness of the pruning rule depends on quickly finding a
        # nearby point. To do this, the recursive method is organized so that
        # when there are two possible subtrees to go down, it first chooses the
        # subtree that is on the same side of the splitting line as the query
        # point; the closest point found while exploring the first subtree may
        # enable pruning of the second subtree.
        root = self.root
        nearest_p, dist = self.find_nearest(root, p, 0, root.p, p.distSqdTo(root.p))
        return nearest_p

    # Internal method for finding the nearest point to p
    def find_nearest(self, node, p, dim, candidate, dist):
        # Base case
        if (node == None):
            return candidate, dist

        # Check if furthest distance of the nearest candidates is less than
        # that of bounding box
        if (dist < node.bounds.distSqdTo(p)):
            return candidate, dist

        # Replace candidate if closer
        newDist = p.distSqdTo(node.p)
        if (newDist < dist):
            candidate = node.p
            dist = newDist

        # Determine whether the tree should go left first or right first
        # Rmk: goes left first iff query point is on the left
        go_left = (p.s[dim] < node.key)

        for i in range(2):
            if (go_left):
                # Travel leftwards down the tree
                candidate, dist = self.find_nearest(node.left, p, (dim + 1) % self.k, candidate, dist)
            else:
                # Travels rightwards down the tree
                candidate, dist = self.find_nearest(node.right, p, (dim + 1) % self.k, candidate, dist)

            go_left = not go_left

        return candidate, dist
