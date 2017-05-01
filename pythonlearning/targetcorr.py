#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

from random import uniform
import rocksVMinesData
import matplotlib.pyplot as plot

__author__ = 'LBX'

rocksVMines = rocksVMinesData.get_data()
target = []
size = len(rocksVMines)
for i in range(size):
    # assign 0 or 1 target value based on "M" or "R" labels
    if rocksVMines.iat[i, 60] == 'M':
        target.append(1.0)
    else:
        target.append(0.0)
# row: all, column 35
dataRow = rocksVMines.iloc[0:size, 35]
plot.scatter(dataRow, target)
plot.xlabel('Attribute Value')
plot.ylabel('Target Value')
plot.show()


# To improve the visualization this version dithers the points
# a little and make s them somewhat transparent
target = []
for i in range(208):
    if rocksVMines.iat[i, 60] == 'M':
        target.append(1.0 + uniform(-0.1, 0.1))
    else:
        target.append(0.0 + uniform(-0.1, 0.1))

dataRow = rocksVMines.iloc[0:208, 35]
plot.scatter(dataRow, target, alpha=0.5, s=120)
plot.xlabel('Attribute Value')
plot.ylabel('Target Value')
plot.show()

