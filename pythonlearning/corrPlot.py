import matplotlib.pyplot as plot
# import pandas as pd
# from pandas import DataFrame
import rocksVMinesData

__author__ = 'LBX'

rocksVMines = rocksVMinesData.get_data()

dataRow2 = rocksVMines.iloc[1, 0:60]
dataRow3 = rocksVMines.iloc[2, 0:60]
plot.scatter(dataRow2, dataRow3)

plot.xlabel('2nd Attribute')
plot.ylabel('3nd Attribute')

plot.show()


dataRow21 = rocksVMines.iloc[20, 0:60]
plot.scatter(dataRow2, dataRow21)
plot.xlabel('2nd Attribute')
plot.ylabel('21nd Attribute')
plot.show()
