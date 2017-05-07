import sys
sys.path.append('..')
from utils import util_excel
import unittest

class TestUtils(unittest.TestCase):
    def test_xlsxhelper(self):
        #sdb.initBeeWorkspace('ICE7360_1718.09')
        xlsxHelper = util_excel.XlsxHelper("../data/RELEASE_CHECKLIST_TEMPLATE.xlsx")
        xlsxHelper.write('A1', 'This is A1')
        xlsxHelper.write('A10',"This is A10")
        xlsxHelper.save('result.xlsx')

        xlsxHelper = util_excel.XlsxHelper("result.xlsx")
        
        self.assertEquals(xlsxHelper.getCell('A1').value, 'This is A1')
        self.assertEquals(xlsxHelper.getCell('A10').value, 'This is A10')
        #self.assertEquals()


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
