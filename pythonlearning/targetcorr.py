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
