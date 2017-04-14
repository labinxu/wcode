#!/usr/bin/python
import commands
import urllib2
import numpy as np
import sys
import os
__author__ = 'labinxu'

data = None
file = None
datafile = 'data/sonar-data.txt'
if not os.path.exists(datafile):
    commands.getoutput('mkdir data')
    # read from uci data repository
    target_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data'

    data = urllib2.urlopen(target_url)
    file = open(datafile, 'w')
    file.write(data.read())
else:
    file = open(datafile, 'r')
    data = file

xList = []
labels = []
for line in data:
    row = line.strip().split(',')
    xList.append(row)

nrow = len(xList)
ncol = len(xList[1])

type = [0] * 3
colCounts = []
col = 3
colData = []
for row in xList:
    colData.append(float(row[col]))
# size = len(colData)
# ava = 0
# print(reduce(lambda x, y: x+y, colData)/size)

colArray = np.array(colData)
colMean = np.mean(colArray)
colsd = np.std(colArray)
sys.stdout.write("Mean = " + '\t' + str(colMean)+'\t\t' +
                 "Standard Deviation = " + '\t' + str(colsd) + "\n")

# calculate quantile and boundaries
ntiles = 4
percentBdry = []
for i in range(ntiles+1):
    percentBdry.append(np.percentile(colArray, i*(100)/ntiles))

print('Boundaries for 4 Equal Percentiles\n %s' % str(percentBdry))

# The last column contain categorical variables
col = 60
colData = []
for row in xList:
    colData.append(row[col])

# awk -F, '{print $61}' | sort | uniq
unique = set(colData)
print('Unique Label Value\n%s' % str(unique))

# count up the number or elements having each value
catDict = dict(zip(list(unique), range(len(unique))))
catCount = [0] * 2
for elt in colData:
    catCount[catDict[elt]] += 1

print('Count for each Value of categorical Label')
print(list(unique))
print(catCount)

