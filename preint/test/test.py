#!/usr/bin/python

"""
@author LBX
copyright
"""
import json
import sys
sys.path.append('..')
from utils.parser import WebParser
import utils.utils
from utils.utils import Browser
from utils import outlookhelper
#import bl_release_parser
import unittest
import dailybuild
import mechanize
import urllib2
import urllib2
import base64
import sys
import re

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
       # print(self.browser.content)

        


class TestDailyBuilder(unittest.TestCase):
    def test_shell_interactor(self):
        sdb = StubDailyBuilder()
        sdb.initBeeWorkspace('ICE7360_1718.09')
        _, stdout, _ = sdb.shInteractor.execCommand('whoami')
        print(stdout)

class TestWebBrowser(unittest.TestCase):

    def test_webbrowser(self):
        browser = Browser(debug=True, content=open('../data/loginpage','r').read())
        tag = browser.find('input',{'name':'csrfmiddlewaretoken'})
        self.assertEqual(tag.get('value'), 'BkkGrr60AQxMcKsBtgL4VQHVtT4WeueS')
#
    def test_pit_publisher(self):
        PIT_PUBLISHER_URL = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM-PIT_PUBLISHER/'
        browser = Browser(debug=True, content=open('../data/PIT.html','r').read())
        # browser.open(PIT_PUBLISHER_URL)
        tag = browser.find('div',attrs={'class':'pane desc indent-multiline'})
        self.assertEqual(tag.label().strip(),'ICE7360_05.1719.01')

    def test_nonprsvg(self):  
        NONPRSVG_PIT_PUBLISHER_URL = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/'
        browser = Browser(debug=True, content=open('../data/NONPRSVG.html','r').read())
        tag = browser.find('div',{'class':'pane desc indent-multiline'})
        #browser.open(NONPRSVG_PIT_PUBLISHER_URL)
        self.assertEqual(tag.text.strip(),'ICE7360_05.1718.07')
            
    def test_tag_difference(self):
         br = Browser()
         br.open('https://oc6web.intel.com/mani/ICE7360_05.1718.06/ICE7360_05.1718.07/#table')
         
    def test_sortTags(self):
       tag1,tag2 = utils.sortTags('ICE7360_05.1719.05', 'ICE7360_05.1719.01')
       self.assertEqual((tag1,tag2),('ICE7360_05.1719.01', 'ICE7360_05.1719.05'))
    def test_bl_release(self):
        #self.assertEqual('ICE7360_05.1719.05', bl_release_parser.bl_release_parser())
        pass
def load_jason(json_content):
    json_to_python = json.loads(json_content)
    for modem_item in json_to_python['diff']['modem/modem']:
         print(modem_item['UTP'])
    for modem_item in json_to_python['diff']['modem/lte_fw']:
         print(modem_item['UTP'])
         
def ListUTPs():
        jsonContent = open('../data/5-5json.txt','r').read()
        jsonloads = json.loads(jsonContent)
        for item ,val in jsonloads['diff'].items():
            for li in val:
                print(li["UTP"])
            
        
def test_login_sp2010():
    sdbu = StubDailyBuilder()
    curBuildName = sdbu.getCurrentTag('ICE7360_05.1719')
    print('Curbuildname: %s:' % curBuildName)
    content = sdbu.getReleaseContentXML()
   # https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956
    #open('C:\Users\labinxux\Downloads\ReleaseContent.xml', 'w').write(content)
def getpitinfo():
    content = open('../data/pitlast.html','r').read()
    pa = re.compile(r'Build #(\d{3})')
    m = pa.search(content)
    print(m.group(1))
    bnpa = re.compile(r'<div>(ICE7360_05\.\d{4}\.\d{2})</div>')
    r = bnpa.search(content)
    print(r.group(1))

def searchHarts():
    sdbu = StubDailyBuilder()
    url = sdbu.constructResultUrl('ICE7360_05.1719.05_PREINT_WED_04')
    print(url)
    
    #open('hartsresult','w').write(data)
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWebBrowser)
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
def getMD5SHA1():
    fsum = utils.getMD5SHA1('../2017-05-06 - ReleaseContent_XMM7360.xml')
    print(fsum)
if __name__ == '__main__':
    #ListUTPs()
    #searchHarts()
    outlookhelper.outlook('../data/emailtemplate.htm')
    #getpitinfo()
