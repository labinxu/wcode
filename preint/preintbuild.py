#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

from utils.utils import Browser

import urllib

hosturl = 'https://oc6web.intel.com/login?next=/'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
               'Referer' : 'https://oc6web.intel.com/',
               'Accept': 'text/html, application/xhtml+xml, */*',
               'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
               'Accept-Encoding': 'gzip, deflate'
           }
def check_login(response):
    """
    @param: response submit login response
    @param:
    @return: True if string logout has been found else False
    @raise exception:
    """

    result = response.find('logout') != 1
    return result


def login_preint(username, password):
    """
    @param:username 
    @param: password
    @return: True if login successful
    @raise exception: None
    #csrfmiddlewaretoken=
    Ba3xaIXEOalzR3QyTF1rpp5CJe30PsMs&next=%2F&username=labinxux&password=Mar@0303
    """

    loginurl = 'https://oc6web.intel.com/login?next=/'
    browser = Browser()
    browser.open(loginurl)
    tag = browser.find('input', {'name':'csrfmiddlewaretoken'})
    postData = {'csrfmiddlewaretoken': tag.attrs['value'], 'next':' ', 'username': username, 'password':password}
    postData = urllib.urlencode(postData)
    browser.submit(loginurl, postData)
    return check_login(browser.content), browser

class PreintBuilder():
    def __init__(self, spurl,
                 pburl='https://oc6web.intel.com/login?next=/'):
        """
        @param: spurl sharepoint url
        @param: preint build url
        """
        self.spurl = spurl
        self.pburl = pburl
        # patchsid, patchs url
        self.patchs={}

    def login_sharepoint(self, username, password):
        """
        @param: username
        @param: password
        @return: True or False
        """
        pass

    def login_preint(self, username, password):
        """
        @param: username
        @param: password
        @return: True if login successful
        @raise exception: None
        #csrfmiddlewaretoken=
    Ba3xaIXEOalzR3QyTF1rpp5CJe30PsMs&next=%2F&username=labinxux&password=Mar@0303
        """

        browser = Browser()
        browser.open(self.pburl)
        tag = browser.find('input', {'name':'csrfmiddlewaretoken'})
        postData = {'csrfmiddlewaretoken': tag.attrs['value'], 'next':' ', 'username': username, 'password':password}
        postData = urllib.urlencode(postData)
        browser.submit(self.pburl, postData)
        return check_login(browser.content), browser

    def trigger_build(self, postData):
        """
        trigger a new print build
        @param: postData ,build data
        """
        pass

    def getCurrentPatchs(self):
        """
        @param: self
        get the preint ticket's information which will be build.
        """
        pass

    def createNewShareTicket(self, postData):
        """
        @param: postData
        @return share ticket ID
        """
        pass

    def retrigger(self, buildId):
        """
        @param: buildId
        """
        pass

    def checkBuildStatus(self):
        """
        monitor the preint build id and send email
        or
        """
        pass

if __name__ == '__main__':
    pass
