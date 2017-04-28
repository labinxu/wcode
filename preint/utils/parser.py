#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

from HTMLParser import HTMLParser
import re


class HTMLTag:
    """
    html tag
    """
    def __init__(self, tagname, attrs):
        self.name = tagname
        self.text = None
        if isinstance(attrs, dict):
            self.attrs = attrs
        else:
            self.attrs = dict(attrs)
        self.content = None

    def set_content(self, content):
        """
        input:
        @content: content of tag
        """
        self.content = content

    def label(self):
        """
        return content
        """

        if self.text:
            return self.text

        patt = re.compile('(<.*>)(.*)')
        self.text = patt.match(self.content).group(2).strip()
        return self.text

class WebParser(HTMLParser):
    """
    input:
    a web content parser base on HTMLParser
    """

    def __init__(self, data):
        HTMLParser.__init__(self)
        self.data = data.replace('\n', ' ')
        self.content = {' ': []}
        self.tag_stack = []
        self.last_tag = None
        self.last_pos = 0
        self.feed(self.data)

    def add_tag(self, tag, attrs):
        """
        input:
        @tag: tag name
        @attrs: tag's attributes
        """
        self.last_tag = HTMLTag(tag, attrs)
        if tag not in self.content:
            self.content[tag] = [self.last_tag]
        else:
            self.content[tag].append(self.last_tag)
        return self.last_tag

    def handle_starttag(self, tag, attrs):
        """
        input:
        @tag: tag name
        @attrs: tag's attributes
        """
        self.add_tag(tag, attrs)
        self.last_pos = self.getpos()

    def handle_data(self, data):
        """
        recognize data, html content string
        :param data:
        :return:
        """
        if self.last_tag:
            #print('tag {0}: data: {1}'.format(self.last_tag.name, data))
            self.last_tag.text =data.strip()

    def handle_endtag(self, tag):
        """
        input
        @tag: tag name
        """

        self.last_tag.set_content(self.data[self.last_pos[1]: self.getpos()[1] ])

    def handle_startendtag(self, tag, attrs):
        """
        input:
        @tag: tag name
        @attrs: tag's attributes
        """
        self.add_tag(tag, attrs)
    def find_all(self, tagname, attrs):
        """
        input:
        @tagname: tag name
        @attrs: tag's attributes
        """
        tags = self.content[tagname]
        return [x for x in tags if set(attrs.items()).issubset(x.attrs.items()) ]

    def find(self, tagname, attrs):
        """
        input:
        @tagname: tag name
        @attrs: tag's attributes
        """
        for tag in self.content[tagname]:
            if set(attrs.items()).issubset(tag.attrs.items()):
                return tag
        return None
