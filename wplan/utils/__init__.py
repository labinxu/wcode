
import re

def GetJiraId(text):
    pattern = re.compile("(https://jira01.devtools.intel.com/browse/)(OAM-\d{5})")
    ret  = pattern.findall(text)
    if(ret == []):
        raise Exception('no jira id found!')
    return ret[0][1]


class Args:
    def __init__(self):
        self.user = 'labinxu'
        self.passwd = 'Sep@0909'
        self.input_file=''

