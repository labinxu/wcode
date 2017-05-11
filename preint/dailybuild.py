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
   === for bash
   module unload perl;module load perl
perl -I/nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/perllib/ /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/relnotes.pl -proj=XMM7360 -release=ICE7360_05.1720.01 -utpfile=ishare.txt -xmlfile=ReleaseContent_XMM7360.xml
===
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
from utils.shinteract import ShInteractor
import utils.utils
import datetime
from bs4 import BeautifulSoup
from utils import util_excel
from utils import spformhelper
import time
ErrorTag ="ERROR: %s"

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
    jsonloads = json.loads(json_content)
    for item , val in jsonloads['diff'].items():
        for li in val:
            result.extend(li["UTP"])
    result = list(set(result))
    return result

def GetBuildNumberAndBuildName(data):
    pa = re.compile(r'Build #(\d{3})')
    buildnumber = pa.search(data)
    bnpa = re.compile(r'<div>(ICE7360_05\.\d{4}\.\d{2})</div>')
    buildname = bnpa.search(data)
    return (buildnumber.group(1), buildname.group(1))
        
class DailyBuilder():
    def __init__(self):
        self.pit_publisher_url = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM-PIT_PUBLISHER/'
        self.nonprsvg_pit_publisher_url = \
'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/'
        self.bn2url = {}
        self.differUrl = 'https://oc6web.intel.com/mani/%s/%s/json'
        self.browser = Browser()
        self.baseTag = None
        self.sharepointTable = []
        self.isharefile = 'ishare.txt'
        self.shInteractor = ShInteractor(username='labinxux',
                                         hostname='musxeris016.imu.intel.com')

        self.workspaceOnServer = None

    def writeSharefile(self, data):
            with open('ishare.txt', 'w') as f:
                for line in data:
                    f.write(line+'\n')

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
        print("Get top build name...")
        lastpitbuild = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM-PIT_PUBLISHER/lastBuild/'
        print("Open %s" % lastpitbuild)
        data = self.browser.open_without_parser(lastpitbuild)
        pitBuildNumber , pitBuildName = GetBuildNumberAndBuildName(data)
        print('Pit BuildName: %s ==== Build Number is %s' % (pitBuildName, pitBuildNumber))
        self.bn2url[pitBuildName] = self.pit_publisher_url + pitBuildNumber
        
        lastnonprsvgBuild = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/lastBuild/'
        print("Open %s" % lastnonprsvgBuild)
        data = self.browser.open_without_parser(lastnonprsvgBuild)
        nonprsvgBuildNumber, nonprsvgBuildName = GetBuildNumberAndBuildName(data)
        self.bn2url[nonprsvgBuildName] = self.nonprsvg_pit_publisher_url + nonprsvgBuildNumber
        print('nonprsvgBuildName: %s  ==== nonprsvgBuildNumber %s' % (nonprsvgBuildName, nonprsvgBuildNumber))
        return(pitBuildName, nonprsvgBuildName)
        
    def getDifference(self, tag1, tag2):
        #differUrl https://oc6web.intel.com/mani/ICE7360_05.1718.06/ICE7360_05.1718.07/#table
        url = self.differUrl % (tag1, tag2)
        print('Query from %s:' % url)
        jsonContent = self.browser.open(url)
        ret = getUTPList(jsonContent)
        print("Different %s" % ret)
        return ret
        
    def getCurrentBuildName(self, base):

        bl_releases = 'https://sp2010.ger.ith.intel.com/sites/XMM7360/Lists/BL_Releases/Default.aspx'
        self.browser.open_with_requests(bl_releases)
        pa = re.compile(base+'\.[0-9]{2}')
        m = pa.search(self.browser.content)
        if not m:
            print("Current build name %s" % m.group())

        print("Current build name %s" % m.group())
        self.currentBuildname = m.group()

        # get url for bl release
        soup = BeautifulSoup(self.browser.content, "html.parser")
        tag = soup.find('a', attrs={'onfocus':'OnLink(this)'},text=self.currentBuildname[:-3])
        
        self.blrelUrl = tag.attrs['href']
        self.sharepointTable.append(('BL_URL', self.blrelUrl))
        return self.currentBuildname

    def runCommand(self, commandline):
        p = subprocess.Popen(commandline,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        return p

    def comunicateWithSH(self, cmdline):
        if cmdline.strip() == '':
            print('cmdline can not empty')
            return

        stdin, stdout, stderr = self.shInteractor.execCommand(cmdline)
        while True:
            line = stdout.readline()
            if line != '':
                print(line[0:-1])
                time.sleep(0.5)
            else:
                break
        
    def runShCmd(self, cmdline):
        if cmdline.strip() == '':
            print('cmdline can not empty')
            return
        stdin, stdout, stderr = self.shInteractor.execCommand(cmdline)
        return stdout, stderr

        
    def initBeeWorkspace(self, buildname):
        out, err = self.runShCmd('whoami')
        self.useraccount = out.read().strip()
        self.workspaceOnServer = '/local/%s/dailybuild/' % self.useraccount
        # mkdir workspace
        #out, err = self.runShCmd('mkdir -p /local/%s/dailybuild/%s' % (self.useraccount, buildname))
        self.uploadfile('ishare.txt', self.workspaceOnServer+'ishare.txt')
        # find ReleaseContent file
        today = datetime.date.today()
        relConFile = "%s - %s" % (str(today), 'ReleaseContent_XMM7360.xml')
        self.uploadfile(relConFile, self.workspaceOnServer+'ReleaseContent_XMM7360.xml')

    def checkFile(self, localfile, remotefile):
        print('Check the md5 and sha1 for file ')
        lfmd5, lfsha1 = utils.getMD5SHA1(localfile)
        print("%s : MD5: %s" % (localfile, lfmd5))
        print("%s : SHA1:%s" % (localfile, lfsha1))
        # 　# md5sum download.iso
        # sha1sum download.iso
        stdout, stderr = self.runShCmd('md5sum %s' % remotefile)
        rfmd5 = stdout.read()
        stdout, stderr = self.runShCmd('sha1sum %s' % remotefile)
        rfsha1 = stdout.read()

        rfmd5 = rfmd5.split(' ')[0].strip()
        rfsha1 = rfsha1.split(' ')[0].strip()
        print("Remote %s : MD5: %s" % (localfile, rfmd5))
        print("Remote %s : SHA1:%s" % (localfile, rfsha1))
        if lfmd5 == rfmd5 and lfsha1 == rfsha1:
            print("Same file %s" % localfile)
            return False
        else:
            return True
        
        
    def uploadfile(self, localfile, remotefile):
        if self.checkFile(localfile, remotefile):
            print("upload file %s: %s" % (localfile, remotefile))
            self.shInteractor.transFile(localfile, remotefile)

    def getInitConfigVersion(self, buildname):
        rfrllb = './modem/mhw_rf/rf_init_config/INIT_CFG_ES200/rf_release_label.txt'
        stdout, stderr = self.runShCmd('cat %s' %   self.workspaceOnServer+buildname+rfrllb)
        return stdout.read().strip()

    def getDataForBuildName(self, buildname):
        buildlink = self.bn2url[buildname]
        print("Get Data for %s" % buildname)
        print("Build link %s" % buildlink)
        buildLog = self.browser.open_without_parser(buildlink+'/console')
        #open('buildlog','w').write(buildLog)
        # ===========================================================
        #https://tcloud6-delivery.rds.intel.com/b/job/PREPARE-WORKSPACE/163631/console
        prepareWorkspace = r'https://tcloud6-delivery.rds.intel.com/b/job/PREPARE-WORKSPACE/[0-9]{6}'
        prew = re.compile(prepareWorkspace)
        print("Pattern prepareWorkspace %s" % prepareWorkspace)
        result = prew.search(buildLog)
        ppwkscsLink = ''
        if result:
            ppwkscsLink = result.group()
            print("Prepare Workspace console %s" % ppwkscsLink)
            data = self.browser.open_without_parser(ppwkscsLink+'/console')
            #baseline: ICE7360/ICE7360_2017-05-03_1903_UTC
            blpa = re.compile(r'baseline.{2}ICE7360/(ICE7360_\d{4}-\d{2}-\d{2}_\d{4}_UTC)')
            gitTag = blpa.search(data).group(1)
            print("Initial Baseline (SIT Publisher) Git Tag: %s" % gitTag)
            self.sharepointTable.append(('Initial Baseline (SIT Publisher) Git Tag', gitTag))
            print("Baseline GIT TAG: %s" % gitTag)
            self.sharepointTable.append(('Baseline GIT TAG', gitTag))
        
        # ========================================================
        self.sharepointTable.append(('PIT Link', self.bn2url[buildname]))
        self.sharepointTable.append(('Build name', buildname))
        self.sharepointTable.append(('Build GIT TAG', buildname))
        sharefolder = r"\\musdsara001.imu.intel.com\sw_builds\XMM7360\Release\MODEM_%s\MAIN" % buildname[8:-3]
        self.sharepointTable.append(('XMM7360 Build Location', sharefolder + '\\' + buildname))
        artifactorylocation = 'https://mu-artifactory-builds.imu.intel.com:8443/artifactory/simple/modem-sit-xmm7360-imc-mu/pit/' 
        self.sharepointTable.append(('XMM7360 Artifactory Location', artifactorylocation + buildname))
        self.sharepointTable.append(('PRIO_1 Tickets', 'Proi red covered in xls'))
        
        #get hartlink
        #https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/148 
        keys = self.bn2url[buildname].split('/')[-2:]
        searshkeys = '%s_%s' % (keys[0], keys[1])
        print("[+] search keys %s" % searshkeys)
        self.sharepointTable.append(('HartsLink', self.constructResultUrl(searshkeys)))
        #===================================================
        revNANDLink = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_UBS-FULL-MODEM-BUILD_XMM7360-REV-2.1-NAND/lastBuild/console'
 
        data = self.browser.open_without_parser(revNANDLink)
        sstpa = re.compile('build_number=([a-zA-Z0-9]{35}__ICE\d{4}_\d{2}.\d{4}.\d{2})')
        sstBuildNumber = sstpa.search(data)
        sst = ""
        if sstBuildNumber:
            sst = sstBuildNumber.group(1)
            print("SSTDecoders %s" % sst)
        else:
            print(ErrorTag % "Can not found SSTDecoders")
        STTDecoders = r'\\imcsmb.imu.intel.com\pftools_decoders\xmm7360'
        self.sharepointTable.append(('STT Decoders', STTDecoders + '\\'+ sst))

    def run(self, buildname):
        self.initBeeWorkspace(buildname)
        home = "/nfs/site/home/%s" % self.useraccount 

        cmdline = home + ('/bin/dailybuild.sh %s' % buildname)
        print('Run %s' % cmdline)
        self.comunicateWithSH(cmdline)
        
        confverion = self.getInitConfigVersion(buildname)
        self.sharepointTable.append(('Content / Components:', confverion))

    def writeXlsxFile(self, filename, buildname):
        # wirte checklist
        xlsxHelper = util_excel.XlsxHelper("./data/RELEASE_CHECKLIST_TEMPLATE.xlsx")
        xlsxHelper.write('C1', buildname)
        xlsxHelper.write('C10', self.blrelUrl)
        # RELEASE_CHECKLIST_05.1720.01.xlsx
        # tag2  ICE7360_05.1720.03
        xlsxHelper.save(filename)

    def constructResultUrl(self, keysearch):
        content = self._gethartsResult(keysearch)
        tables = []
        jsondata = json.loads(content)
        for tabledata in jsondata:
            tables.append(tabledata['tsName'])
        baseurl = 'http://harts.imu.intel.com/harts6/ViewSelectedTestReport.do?tsNames=toggle_all;'
        for i in tables:
            baseurl += i+';'
        return baseurl
        
    def _gethartsResult(self, keysearch):
        hartsurl = 'http://harts.imu.intel.com/harts6/GetDetailsForBuildSearch.do?tsName='
        content = self.browser.open_without_parser(hartsurl+keysearch)
        return content
        
def Download():
    br = spformhelper.SPFormHelper('./bin/IEDriverServer.exe')
    br.downloadCqUtpSms()
    result = raw_input("IS Download Finised: ")
    while result != 'Y':
        time.sleep(1000)
        
def DailyBuild():

   # Download()
    dbu = DailyBuilder()
    tag1, tag2 = dbu.getTopBuildName()
    tag1, tag2 = utils.sortBuildName(tag1, tag2)
    base = tag2[0:-3]
    cur_tag = dbu.getCurrentBuildName(base)
    
    # debug
    #if not cur_tag:
    diff = dbu.getDifference(cur_tag, tag2)
    if len(diff) == 0:
        print('======================')
        print("[+] Warning: There is no different, Please double check it")
    #else:
     #   diff = dbu.getDifference(tag1, tag2)
    dbu.writeSharefile(diff)
    dbu.getDataForBuildName(tag2)
    sufixname=tag2[8:]
    # upload the isharefile and ReleaseContent file
    #dbu.run(tag2.strip())
    
    releasechecklistfile = 'RELEASE_CHECKLIST_%s.xlsx' % sufixname
    dbu.writeXlsxFile(releasechecklistfile, tag2)
    SHARE_FOLDER_ROOT='/nfs/imu/disks/sw_builds/XMM7360/Release/MODEM_%s/MAIN/%s/'
    #MODEM_05.1720\MAIN\ICE7360_05.1720.03
    detfile = SHARE_FOLDER_ROOT % (tag2[8:-3], tag2)
    dbu.uploadfile(releasechecklistfile, detfile + releasechecklistfile)
    print('\n\n==============END=================\n\n')
              
    print('\n\n===============Table Data====================')
    for key, value in dbu.sharepointTable:
        print("%s: %s" % (key, value))
    print('===============End====================\n\n\n')
    
    print('=========update refresh the sharepoint ================')
              
    br = spformhelper.SPFormHelper('./bin/IEDriverServer.exe')
    
    br.fillForm(base, dbu.sharepointTable)

if __name__ == '__main__':
    DailyBuild()
