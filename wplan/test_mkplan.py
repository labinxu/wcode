# coding:utf-8

import unittest
import mkplan

class CmdLine:
    def __init__(self):
        self.jiraids="OAM-37493,OAM-37814"

class MkplanTestCases(unittest.TestCase):

    def testRe(self):
        import re
        text='xxfeagf'
        pattern = re.compile("(https://jira01.devtools.intel.com/browse/)(OAM-\d{5})")
        ret  = pattern.findall(text)
        assert(ret == [])

    def test(self):

        mkplan.INPUT_ARGS = CmdLine()
        print('test_get_jiraid')
        jiraid = mkplan.getJiraId('# =HYPERLINK("https://jira01.devtools.intel.com/browse/OAM-37493","OAM-37493")')
        assert(jiraid == "OAM-37493")
        print('jiraid = %s' % jiraid)

    def testParseJiraIds(self):
        assert(["oam-37493", 'oam-37814'] == mkplan.parseJiraIds(mkplan.INPUT_ARGS.jiraids))

    def testShouldTest(self):
        assert(False == mkplan.shouldTest("oam-37493",['']))
        assert(True == mkplan.shouldTest("oam-37493",["oam-37493", 'oam-37814']))
        assert(False == mkplan.shouldTest("oam-37494",["oam-37493", 'oam-37814']))

if __name__ == '__main__':
    unittest.main()

