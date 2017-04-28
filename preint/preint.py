
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
    if(response.find('logou') != -1):
        return True
    else:
        return False
 

def login_preint(username, password):
    loginurl = 'https://oc6web.intel.com/login?next=/'
    browser = Browser()
    page = browser.open(loginurl)
    tag = browser.find('input', {'name':'csrfmiddlewaretoken'})
    postData = {'csrfmiddlewaretoken': tag.attrs['value'], 'next':' ', 'username': username, 'password':password}
    postData = urllib.urlencode(postData)
    browser.submit(loginurl, postData)
    return check_login(browser.content), browser
    
    #csrfmiddlewaretoken=Ba3xaIXEOalzR3QyTF1rpp5CJe30PsMs&next=%2F&username=labinxux&password=Mar@0303

def login(username, password):
    status, browser = login_preint(username, password)
    if status:
        print('login successful')
        
def get_diff_tags():
         browser = Browser()
        
        PIT_PUBLISHER_URL = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM-PIT_PUBLISHER/'
        browser.open(PIT_PUBLISHER_URL)
        pit_publisher_tag = browser.find('div',{'class':'pane desc indent-multiline'})
        
        NONPRSVG_PIT_PUBLISHER_URL = 'https://tcloud6-delivery.rds.intel.com/b/job/XMM7360_MODEM_NONPRSVG_PIT_PUBLISHER/'
        browser.open(NONPRSVG_PIT_PUBLISHER_URL)
        nonprsvg_pit_publisher_tag = browser.find('div',{'class':'pane desc indent-multiline'})
        
        
if __name__ == '__main__':
    get_diff_tags()
