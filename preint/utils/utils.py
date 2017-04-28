import urllib2
import cookielib
import parser
import bs4

class Browser:
    '''
    brower for html
    '''

    def __init__(self, debug=False, content='', htmlparser=bs4.BeautifulSoup):
        self.mode = debug
        self.htmlparser = htmlparser
        self.parser = None
        if debug:
            self.content = content
            self.parser = self.htmlparser(self.content)
        else:
            self.init_cookie(ckname='tmpcookie')
            
    def _init_htmlparser(self, data):
        self.parser = self.htmlparser(data)
        
    def submit(self, url, data):
        self.reset_parser()
        response = self.opener.open(url, data)
        self.content = response.read()
        self._init_htmlparser(self.content)
    def text(self, beg, end):
        return self.content[beg:end]
        
    def init_cookie(self, ckname):
        '''
        init the brower cookie
        '''
        self.cookie = cookielib.LWPCookieJar(ckname)
        cksupport = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(cksupport)
        urllib2.install_opener(self.opener)

    def reset_parser(self):
        # if self.parser:
        #     self.parser.close()
        self.parser = None

    def open(self, url):
        # init parser again
        #response = urllib2.urlopen(url)
        response = self.opener.open(url)
        self.content = response.read()
        self._init_htmlparser(self.content)
        return self.content
    
    def find(self, tagname, attrs):
        tag = self.parser.find(tagname,attrs=attrs)
        #if tagname not in self.parser.content:
        #    print('%s not in' % tagname)
        #    return None
        #
        #for key, value in attrs.items():
        #    for tag in self.parser.content[tagname]:
        #        if key in tag.attrs and value == tag.attrs[key]:
        #            return tag
        return tag

