# Author:  Reilly Bova '20
# Date:    11 November 2018
# Project: COS 526 A2 — Point Cloud Registration
#
# File:    point.py
# About:   Implements an nD Point

from math import *

# TODO: do I need object?
# Takes an nD length array of positions and optionally of normals as input
class Point:
    # Contructor (optionally) takes position array and normal array
    def __init__(self, s=[], n=[]):
        self.s = s.copy()
        self.n = n.copy()
        self.d = len(s)

    # Return deep copy
    def copy(self):
        newS = self.s.copy()
        newN = self.n.copy()
        newP = Point(newS, newN)

        return newP

    # Returns euclidean distance between two points of the same dimension
    def distTo(self, p):
        return sqrt(self.distSqdTo(p))

    # Returns squared euclidean distance between two points of the same dimension
    def distSqdTo(self, p):
        if (type(self) != type(p)):
            print("Error: Expected a Point but recieved {}".format(type(p)))
            return 0.0

        if (p.d != self.d):
            print("Error: Cannot compute distance between Points of different"
                " dimensionality")
            return 0.0

        distSqd = 0.0
        for i in range(self.d):
            distSqd += (self.s[i] - p.s[i])**2
        return distSqd
