#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

import urllib2
import cookielib
from parser import WebParser
import requests
from requests_kerberos import HTTPKerberosAuth, REQUIRED
        
## copy library bs4 interface
# import bs4

# http://python-notes.curiousefficiency.org/en/latest/python_kerberos.html
class Browser:
    '''
    brower for html
    '''

    def __init__(self, content='', htmlparser=WebParser, debug=False):
        """
        @param: content web page content
        @param: htmlparser web page parser HTMLParser or bs4.BeautifulSoup
        """

        self.mode = debug
        self.htmlparser = htmlparser
        self.parser = None
        if debug:
            self.content = content
            self.parser = self.htmlparser(self.content)
        else:
            self.init_cookie(ckname='tmpcookie')

    def _init_htmlparser(self, data):
        """
        @param: data for parser
        """

        self.parser = self.htmlparser(data)

    def submit(self, url, data):
        """
        @param: url url for open
        @param: data ,post data
        @return: content, the submit result page
        """
        self.reset_parser()
        response = self.opener.open(url, data)
        
        self.content = response.read()
        self._init_htmlparser(self.content)
        return self.content

    def init_cookie(self, ckname):
        '''
        init the brower cookie
        '''
        self.cookie = cookielib.LWPCookieJar(ckname)
        cksupport = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(cksupport)
        #self.opener.addheaders = [{}]
        urllib2.install_opener(self.opener)

    def reset_parser(self):
        """
        @param:
        @param:
        @return:
        """

        # if self.parser:
        #     self.parser.close()
        self.parser = None
    def open_with_requests(self, url, auth=True):
        if not auth:
            return
        kerberos_auth = HTTPKerberosAuth(mutual_authentication=REQUIRED,
            sanitize_mutual_error_response=False)
        r = requests.get(url, auth=kerberos_auth, verify=False)
        self.content = r.text.encode('utf-8')
        return r
    def post_with_requests(self, url, auth=True):
        import json
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
        r = requests.post(url,auth=kerberos_auth, data=json.dumps(payload), headers=headers)
        return r
    def open_without_parser(self, url):
        """
        @param: url page url
        """

        # init parser again
        response = urllib2.urlopen(url)
        #response = self.opener.open(url)
        self.content = response.read()
        return self.content

    def open(self, url):
        """
        @param: url page url
        """

        # init parser again
        #response = urllib2.urlopen(url)
        response = self.opener.open(url)
        self.content = response.read()
        self._init_htmlparser(self.content)
        return self.content

    def get_parser(self):
        """
        @return: return the web page parser
        """
        return self.parser

    def find_all(self, tagname, attrs):
        """
        @param: tagname
        @param: attrs
        """
        return self.parser.find_all(tagname, attrs)

    def find(self, tagname, attrs):
        """
        @param: tagname
        @param: attrs
        """
        return self.parser.find(tagname, attrs=attrs)
