import pandas as pd
import utils
import os

__author__ = 'LBX'


def get_data():
    data = utils.getData('https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data',
                         datadir=os.path.abspath('./data'))
    rocksVMines = pd.read_csv(data, header=None, prefix='v')
    return rocksVMines
