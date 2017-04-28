#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

import urllib2
import cookielib
from parser import WebParser
## copy library bs4 interface
# import bs4


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
