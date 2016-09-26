#-*- coding: utf-8 -*-

import unittest
import mkstatistics

class Param:
    def __init__(self):
        self.user = 'labinxu'
        self.passwd = 'Sep@0909'
        self.input_file=''


class MkstatisticsTestCases(unittest.TestCase):
    def testGetComments(self):

        mkstatistics.INPUT_ARGS = Param()
        #mkstatistics.cmdline('-u','labinxux', '-p', 'Sep@0909'])
        #assert('ok' == mkstatistics.get_comments('OAM-37814'))

    def testCountRowFails(self):
        assert(4==mkstatistics.countRowFailuers(['Fail','Fail','Fail','Fail']))

if __name__ == '__main__':
    unittest.main()

