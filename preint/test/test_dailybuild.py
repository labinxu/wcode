import json
import sys
sys.path.append('..')
from utils.parser import WebParser
import utils.utils
from utils.utils import Browser
#import bl_release_parser
import unittest
import dailybuild

class StubDailyBuilder(dailybuild.DailyBuilder):
    def __init__(self):
        dailybuild.DailyBuilder.__init__(self)
        pass
    
    def login(self, username, password):
        preinturl='https://sp2010.ger.ith.intel.com/sites/XMM7360/Lists/7360_Preint/Default.aspx'
        import requests
        from requests_kerberos import HTTPKerberosAuth, REQUIRED
        kerberos_auth = HTTPKerberosAuth(mutual_authentication=REQUIRED, sanitize_mutual_error_response=False)
        r = requests.get(preinturl, auth=kerberos_auth,verify=False)
        print(r.text.encode('utf-8'))

    def getCurrentTag(self, base):
        import re
        bl_releases = 'https://sp2010.ger.ith.intel.com/sites/XMM7360/Lists/BL_Releases/Default.aspx'
        self.browser.open_with_requests(bl_releases)
        '''ICE7360_05.1719.05'''
        #first find ICE7360_05.1719 build
        pa = re.compile(base+'\.[0-9]{2}')
        m = pa.search(self.browser.content)
        return m.group()

sdb = StubDailyBuilder()
class TestDailyBuilder(unittest.TestCase):
    def test_useraccount(self):

        #sdb.initBeeWorkspace('ICE7360_1718.09')
        stdout, err = sdb.runShCmd('whoami')
        self.assertEquals(stdout.read().strip() , sdb.shInteractor.username)

    def test_shell_change(self):
        cmd = "ps | grep $$ | awk '{print $4}'"
        out, err = sdb.runShCmd(cmd)
        self.assertEquals(out.read().strip(), 'tcsh')

    def test_create_beeworkspace(self):
        wdir = '/local/%s/dailybuild/%s' % (sdb.shInteractor.username, 'shelltest')
        out, err  = sdb.runShCmd('mkdir -p %s' % wdir)
        out, err  = sdb.runShCmd('cd %s/..;ls -l |grep -o shelltest' % wdir)
        self.assertEquals(out.read().strip(), 'shelltest')
    
    def test_call_shfunc(self):
        #out, err = sdb.runShCmd("bash")
        out, err = sdb.runShCmd("~/bin/dailybuild.sh ICE7360_TEST debug")
        self.assertEquals(out.read().strip(), "ICE7360_TEST")

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDailyBuilder)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

   #print('All case number')
   #print(test_result.testsRun)
   #print('Failed case number')
   #print(len(test_result.failures))
   #print('Failed case and reason')
   #print(test_result.failures)
   #for case, reason in test_result.failures:
   #    print case.id()
   #    print reason

if __name__ == '__main__':
    main()
