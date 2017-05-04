#!/usr/bin/python
# -*- coding: utf-8 -*-
# proxy-negotiate
"""

@author labinxux
for daily build
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; \
WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer' : 'https://oc6web.intel.com/',
               'Accept': 'text/html, application/xhtml+xml, */*',
               'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
               'Accept-Encoding': 'gzip, deflate'
           }
           	15. Release content preparation
	• Create a Release content folder at linux build machine(
	• run query:  https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956
	Save the output as XML file at Release content folder(Remove the date. File name should be “ReleaseContent_XMM7360.xml”)(将下载的xml放到workspace下，然后建立ishare.txt 文件 ishare.txt放的是 差异 列表)
	• Create ishare.txt at same location with excel, and open it. And copy ticket from diff tool to this txt
	• Module unload perl && module load perl
	• Run:  setenv PERL5LIB /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/perllib/ 
	• Run: perl /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/relnotes.pl -proj=XMM7360 -release=ICE7360_05.1718.01 -utpfile=ishare.txt -xmlfile=ReleaseContent_XMM7360.xml
	• Copy generated xml to share folder (\\samba-oc6.imu.intel.com\shared_local\musxeris016\labinxux\  to \\musdsara001.imu.intel.com\SW_builds\XMM7360\Release\MODEM_05.1718\MAIN\ICE7360_05.1718.07)  share folder (linux directory:
	/nfs/imu/disks/sw_builds/XMM7360/Release )
	• Open and checkout  https://sp2010.ger.ith.intel.com/sites/XMM7360/05_Release_Management/04_Release_Documentation/ReleaseContent_ICE7360_main_line.xls
	Paste the contents from generated xml
	16. Go through the checklist excel and complete it. (RELEASE_CHECKLIST_05.1718.07.xlsx
	17. Update share point -> build available
	Find SIT tag from PREPARE-WORKSPACE -> Logs and get the base tag
	Find TAG from PUBLISH-GIT -> logs 
	Find init cfg from WS -> /modem/mhw_rf/rf_init_config/INIT_CFG_ES200/rf_release_label.txt
	Find Harts link from http://harts.imu.intel.com/harts6/ListTestBenches.do# Click Search -> By Test, Give -XMM7360_MODEM-PIT_PUBLISHER #680 [Change PIT Id accordingly] and Select      
	         Toggle All Tests and then Display Complete Result
	 Find SPS from PUBLISH-SPS -> Logs Click the Link at the bottom of the log page and copy the SPS content of the link page.
	18. Prepare an email: subject like: Check list for PIT publisher of ICE7360_05.1713.04


"""
import json
import urllib
import re
import subprocess, os
from utils.utils import Browser
import utils.utils

def login_preint(username, password):
    """
    @param username: username for website
    @param password: password for website
    """

    loginurl = 'https://oc6web.intel.com/login?next=/'
    browser = Browser()
    browser.open(loginurl)
    tag = browser.find('input', {'name':'csrfmiddlewaretoken'})
    post_data = {'csrfmiddlewaretoken': tag.attrs['value'], 'next': ' ',
                'username': username, 'password': password }

    post_data = urllib.urlencode(post_data)
    browser.submit(loginurl, post_data)

    return check_login(browser.content), browser
    
def getUTPList(json_content):
    result =[]
    json_to_python = json.loads(json_content)
    for modem_item in json_to_python['diff']['modem/modem']:
         result.extend(modem_item['UTP'])
    for modem_item in json_to_python['diff']['modem/lte_fw']:
         result.extend(modem_item['UTP'])
    return result
    
class DailyBuilder():
    def __init__(self):
        self.pit_publisher_url = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM-PIT_PUBLISHER/'
        self.nonprsvg_pit_publisher_url = \
'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/'

        self.differUrl = 'https://oc6web.intel.com/mani/%s/%s/json'
        self.browser = Browser()
        self.baseTag = None
    def setBaseTag(self, baseTag):
        self.baseTag = baseTag

    def getReleaseContentXML(self):
        queryurl='https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956'
        self.browser.post_with_requests(queryurl)
        #xmlurl = 'https://utpreloaded.rds.intel.com/CqUtpSms/Handlers/Master/DownloadFile.ashx'
        #self.browser.open_with_requests(xmlurl)
        return self.browser.content
        
    def login(self, username, password):
        """
        @param username: username for website
        @param password: password for website
        """

        loginurl = 'https://sp2010.ger.ith.intel.com'
        self.browser = Browser()
        self.browser.open(loginurl)
        tag = self.browser.find('input', {'name':'csrfmiddlewaretoken'})
        post_data = {'csrfmiddlewaretoken': tag.attrs['value'], 'next': ' ',
                    'username': username, 'password': password }

        post_data = urllib.urlencode(post_data)
        self.browser.submit(loginurl, post_data)

        return check_login(self.browser.content), self.browser
        
    def getTopBuildName(self):
        """
        get the different about PIT publisher and nonprsvg publisher
        """
        self.browser.open(self.pit_publisher_url)
        attrs = {'class':'pane desc indent-multiline'}
        pit_publisher_tag = self.browser.find('div', attrs)
        pit_tag = pit_publisher_tag.label()
        print('pit_version: %s' % pit_tag)
        
        self.browser.open(self.nonprsvg_pit_publisher_url)
        nonprsvg_pit_publisher_tag = self.browser.find('div', {'class': 'pane desc indent-multiline'})
        nonprsvg_pit_tag = nonprsvg_pit_publisher_tag.label()
        print('nonprsvg_pit_version: %s' % nonprsvg_pit_tag)
        return(pit_tag, nonprsvg_pit_tag)
        
    def getDifference(self, tag1, tag2):
        #differUrl https://oc6web.intel.com/mani/ICE7360_05.1718.06/ICE7360_05.1718.07/#table
        url = self.differUrl % (tag1, tag2)
        print('Query from %s:' % url)
        jsonContent = self.browser.open(url)
        ret = getUTPList(jsonContent)
        return ret
        
    def getCurrentBuildName(self, base):

        bl_releases = 'https://sp2010.ger.ith.intel.com/sites/XMM7360/Lists/BL_Releases/Default.aspx'
        self.browser.open_with_requests(bl_releases)
        pa = re.compile(base+'\.[0-9]{2}')
        m = pa.search(self.browser.content)
        return m.group()
        
    def runCommand(self, commandline):
        p = subprocess.Popen(commandline,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        return p
    
    def createWorkspace(self):
        os.chdir('/local/labinxux/dailybuild')
        workspace = '%s' % self.baseTag
        command = 'mkdir %s' % workspace
        p = self.runCommand(command)
        print(p.stdout)
        os.chdir(workspace)
        # init workspace
        print(os.getcwd())
        initCommand = 'bee init -p ice7360 -v %s && bee sync -j16' % self.baseTag
       # p = self.runCommand(initCommand)
        os.chdir(self.baseTag)
        
    def pushBinaray(self):
        command = 'perl /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/copy_a2s.pl %s' % self.baseTag
        p = self.runCommand(command)
        releaseDir='/nfs/imu/disks/sw_builds/XMM7360/Release/MODEM_05.1719/MAIN/%s'% self.baseTag
        command = 'chmod -R 777 %s' % releaseDir
        p = self.runCommand(command)
        
if __name__ == '__main__':
    dbu = DailyBuilder()
    tag1, tag2 = dbu.getTopBuildName()
    tag1, tag2 = utils.sortBuildName(tag1, tag2)
    base = tag2[0:-3]
    cur_tag = dbu.getCurrentBuildName(base)
    print(cur_tag, tag1, tag2)
    diff = dbu.getDifference("ICE7360_05.1719.06", tag2)
    print(diff)
   
