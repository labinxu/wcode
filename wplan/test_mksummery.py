from utils import util_docx
from utils import Args
import mksummery
import unittest

class MkSummeryTestCases(unittest.TestCase):
    def testDocx(self):
        mksummery.INPUT_ARGS = Args()
        util_docx.write('../out/testdocx.doc')

if __name__ == '__main__':
    unittest.main()


