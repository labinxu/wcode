import urllib2
import cookielib
import parser


class Browser:
    '''
    brower for html
    '''

    def __init__(self, debug=True, content=''):
        if not debug:
            self.init_cookie(ckname='tmpcookie')

        self.content = content
        self.parser = parser.WebParser()
        self.parser.feed(self.content)

    def init_cookie(self, ckname):
        '''
        init the brower cookie
        '''

        self.cookie = cookielib.LWPCookieJar(ckname)
        cksupport = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(cksupport)
        urllib2.install_opener(self.opener)

    def get_page(self, url):
        '''
        return the url page
        '''
        if self.parser:
            self.parser.close()
            self.parser = None
        else:
            # init parser again
            pass

    def find(self, tagname, attrs):
        print('find function')
        if tagname not in self.parser.content:
            print('%s not in' % tagname)
            return None

        for key, value in attrs.items():
            for tag in self.parser.content[tagname]:
                if key in tag.attrs and value == tag.attrs[key]:
                    return tag
        return None

