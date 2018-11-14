# Author:  Reilly Bova '20
# Date:    11 November 2018
# Project: COS 526 A2 — Point Cloud Registration
#
# File:    utils.py
# About:   Provides utility functions for reading .pts and .xf files

import numpy as np
from .point import Point

# Loads data from the given .xf file into a 4x4 np matrix
def load_xf(file_name):
    with open(file_name) as f:
        data = f.read()
        rows = []
        for r in data.split('\n'):
            if (len(r) > 0):
                rows.append(r)

        if (len(rows) != 4):
            print("Error: Invalid number of rows detected in .xf file")
            rows = ["0 0 0 0" for i in range(4)]

        # Could do in one-liner, but this has error checking
        result = []
        for r in rows:
            c = [float(v) for v in r.split(' ')]
            if (len(c) != 4):
                print("Error: Invalid number of columns detected in {}".format(file_name))
                c = [0, 0, 0, 0]
            result.append(c)

    return np.matrix(result)

# # Loads data from the given .pts file into a list of Points
def load_pts(file_name):
    with open(file_name) as f:
        data = f.read()
        rows = data.split('\n')

        result = []
        for r in rows:
            if (len(r) == 0):
                continue
            pData = [float(v) for v in r.split(' ')]
            if (len(pData) != 6):
                print("Error: Insufficient data provided for a point in {}".format(file_name))
                pData = [0, 0, 0, 0, 0, 0]
            result.append(Point(pData[0:3], pData[3:6]))

    return result
