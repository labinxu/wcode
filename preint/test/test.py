import sys
sys.path.append('..')
from utils.parser import WebParser
from utils.utils import Browser
f = open('../data/loginpage','r')
def test_webparser():
    webparser = WebParser()
    webparser.feed(f.read())
    webparser.close()
    print(webparser.links)

def test_webbrowser():
    browser = Browser(debug=True, content=f.read())

    tag = browser.find('input',{'name':'csrfmiddlewaretoken'})
    print(tag.attrs)

test_webbrowser()
