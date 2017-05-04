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
#import bl_release_parser
import unittest
import dailybuild
import mechanize
import urllib2
import urllib2
import base64
import sys

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
    def test_login_sp2010(self):
        pass
 
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

def test_login_sp2010():
    sdbu = StubDailyBuilder()
    curBuildName = sdbu.getCurrentTag('ICE7360_05.1719')
    print('Curbuildname: %s:' % curBuildName)
    content = sdbu.getReleaseContentXML()
   # https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956
    #open('C:\Users\labinxux\Downloads\ReleaseContent.xml', 'w').write(content)
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

if __name__ == '__main__':
    from requests_kerberos import HTTPKerberosAuth, REQUIRED
    import json
    import requests
    url = 'https://utpreloaded.rds.intel.com/CqUtpSms/RecentHandling.asmx/AddQuery'
    payload = {"QueryName":"149956"}
    headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'22',
    'Content-Type':'application/json; charset=UTF-8'}
    kerberos_auth = HTTPKerberosAuth(mutual_authentication=REQUIRED,
        sanitize_mutual_error_response=False)
    r = requests.post(url,auth=kerberos_auth, data=json.dumps(payload), headers=headers, verify=False)
   # test_login_sp2010()
    print(r.headers)
    print(r.text)
   # main()
    
   
#    br = Browser()
#    #json_content = br.open('https://oc6web.intel.com/mani/ICE7360_05.1718.06/ICE7360_05.1718.07/json')
#    json_content='''{"diff": {"modem/lte_fw": [{"hash": "b634c5bddbad1694a9dc4cb66494fa37c2b821ff", "parent": "49d83cb4abaa5866c98c985a9a621ccdb2b0cdae", "author": "Pradeep H N", "OAM": [], "date": "1493172206", "UTP": ["SMS18661387"], "isPerson": true, "marker": true, "subject": "Consider the Gap IntOffset to post to shcedule Suspend/Resume during IRAT gaps"}]
#, "modem/modem": [{"hash": "316fa63c2bef692cd282fd1a1aac3165e961a0d8", "parent": "b5e44abbafc5dc60a9801a826f39e1cae0b2ee29", "author": "amitx yadav", "OAM": [], "date": "1493188083", "UTP": ["SMS19152640"], "isPerson": true, "marker": true, "subject": "ICE SW-16.0 : TASK=l1ep_1 @ l1e_pal:l1e_crash.c:506,CPU=0,LOG=s:0x0706000078B23B41 v:0x0000000000000000 t:0x00000017 <Timer expired>()"}]}, "removed": [], "added": [], "error": null, "changed": [["modem/lte_fw", "cb969436583db76a2a7eba053029d2b3d221a386", "4abf665ad1a1aa1e184a722cf4860549d802809f"], ["modem/modem", "851e7195ea9d687941f751115915b6e982093cc7", "e94585386a8f76842ec489162bfb09059da3d7c4"]]}'''
#    load_jason(json_content)     
