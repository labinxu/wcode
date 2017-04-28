#!/usr/bin/python
# -*- coding: utf-8 -*-

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
"""
import urllib
from utils.utils import Browser


def check_login(response):
    """
    @param response: the web page content
    post_data:csrfmiddlewaretoken=Ba3xaIXEOalzR3QyTF1rpp5CJe30PsMs&next=%2F&
    username=labinxux&password=Mar@0303
    """

    return True if response.find('logou') != -1 else False

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


def get_diff_tags():
    """
    get the different about PIT publisher and nonprsvg publisher
    """

    browser = Browser()
    pit_publisher_url = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM-PIT_PUBLISHER/'
    browser.open(pit_publisher_url)
    attrs = {'class':'pane desc indent-multiline'}
    pit_publisher_tag = browser.find('div', attrs)
    pit_version = pit_publisher_tag.label()
    print('pit_version: %s' % pit_version)
    nonprsvg_pit_publisher_url = \
'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/'
    browser.open(nonprsvg_pit_publisher_url)
    nonprsvg_pit_publisher_tag = browser.find('div', {'class': 'pane desc indent-multiline'})
    nonprsvg_pit_version = nonprsvg_pit_publisher_tag.label()
    print('nonprsvg_pit_version: %s' % nonprsvg_pit_version)


if __name__ == '__main__':
    get_diff_tags()
