#!/usr/bin/python

import os
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plot

import utils

__author__ = 'LBX'

data = utils.getData('https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data',
                     datadir=os.path.abspath('./data'))
rocksVMines = pd.read_csv(data, header=None, prefix='v')
print(rocksVMines.head())
print(rocksVMines.tail())

summary = rocksVMines.describe()
print(summary)
for i in range(208):
    if rocksVMines.iat[i, 60] == 'M':
        pcolor = 'red'
    else:
        pcolor = 'blue'

    dataRow = rocksVMines.iloc[i, 0:60]
    dataRow.plot(color=pcolor)

plot.xlabel("Attribute Index")
plot.ylabel(('Attribute Value'))
plot.show()
