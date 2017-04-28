#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

import sys
sys.path.append('..')
from utils.parser import WebParser
from utils.utils import Browser

f = open('../data/loginpage','r')

def test_webbrowser():
    browser = Browser(debug=True, content=open('../data/PIT.html', 'r').read())
    #<div class="pane desc indent-multiline">ICE7360_05.1719.01</div>
    tag = browser.find('div', attrs={'class':'pane desc indent-multiline'})
    print(tag.label())
    tags = browser.find_all('div', attrs={'class':'pane desc indent-multiline'})
    for tag in tags:
        print(tag.label())

test_webbrowser()
