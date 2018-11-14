# Author:  Reilly Bova '20
# Date:    11 November 2018
# Project: COS 526 A2 — Point Cloud Registration
#
# File:    box.py
# About:   Implements an nD Box; adapted from COS 226's RectHV

from math import *
from .point import Point

# An nD axis-aligned box
class Box:
    # Constructor takes two points: pMin and pMax that define nD diagonal of Box
    def __init__(self, pMin, pMax):
        if (type(pMin) != Point):
            print("Error: pMin is not of type Point")
            pMin = Point([0])
        if (type(pMax) != Point):
            print("Error: pMax is not of type Point")
            pMax = Point([0])
        if (pMin.d != pMax.d):
            print("Error: pMin and pMax are not of the same dimensionality!")
            pMin = Point([0])
            pMax = Point([0])
        if (pMin.d < 1):
            print("Error: Box dimensionality must be positive")
            pMin = Point([0])
            pMax = Point([0])

        self.sMin = pMin.s.copy()
        self.sMax = pMax.s.copy()
        self.d = pMin.d
        for i, (min, max) in enumerate(zip(pMin.s, pMax.s)):
            if (min > max):
                print("Error: Box dimensionality must be positive")
                self.sMin[i] = max
                self.sMax[i] = min

    def copy(self):
        return Box(Point(self.sMin), Point(self.sMax))

    # Update the dimth dimension of sMax with val
    def updateMax(self, val, dim):
        # Check bounds first
        if (val < self.sMin[dim]):
            print("Error: Cannot update max of Box to fall below min along same"
                " dimension")
            return
        else:
            self.sMax[dim] = val

    # Update the dimth dimension of sMin with val
    def updateMin(self, val, dim):
        # Check bounds first
        if (val > self.sMax[dim]):
            print("Error: Cannot update min of Box to fall above max along same"
                " dimension")
            return
        else:
            self.sMin[dim] = val

    # Returns range of box in specified dimension
    def range(self, dim):
        if (dim < 0 or dim >= self.d):
            print("Error: Cannot compute range of invalid dimension")
            return 0

        return self.sMax[dim] - self.sMin[dim]

    # Returns True if this box intersects with that box (includes cases where
    #   only the boundaries intersect) of the same dimensionality
    def intersects(self, that):
        if (type(that) != Box):
            print("Error: Intersection parameter is not of type Box")
            return Fals
        if (p.d != self.d):
            print("Error: Cannot compute distance between Boxes of different"
                " dimensionality")
            return False

        for min, max in zip(that.sMin, self.sMax):
            if (max < min):
                return False
        for min, max in zip(self.sMin, that.sMax):
            if (max < min):
                return False

        return True

    # Returns True if this Box contains the Point of the same dimensionality
    def contains(self, p):
        if (type(p) != Point):
            print("Error: Contains parameter is not of type Point")
            return False
        if (p.d != self.d):
            print("Error: A Box cannot contain a Point of different"
                " dimensionality")
            return False

        for pval, max in zip(p.s, self.sMax):
            if (pval > max):
                return False
        for pval, min in zip(p.s, self.sMin):
            if (pval < min):
                return False
        for min, max in zip(self.sMin, that.sMax):
            if (max < min):
                return False
        return True

    # Returns the Euclidean distance between this Box and the point
    def distTo(self, p):
        return sqrt(self.distSqdTo(p))

    # Returns the square of the Euclidean distance between this rectangle
    #   and the point.
    def distSqdTo(self, p):
        if (type(p) != Point):
            print("Error: Distance parameter is not of type Point")
            return 0.0
        if (p.d != self.d):
            print("Error: Cannot compute distance from a Point of different"
                " dimensionality")
            return 0.0

        distSqd = 0.0
        for pval, min, max in zip(p.s, self.sMin, self.sMax):
            dv = 0.0
            if (pval < min):
                dv = pval - min
            elif (pval > max):
                dv = pval - max
            distSqd += dv*dv

        return distSqd
