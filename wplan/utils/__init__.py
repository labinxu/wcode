
import re

def GetJiraId(text):
    pattern = re.compile("(https://jira01.devtools.intel.com/browse/)(OAM-\d{5})")
    ret  = pattern.findall(text)
    if(ret == []):
        raise Exception('no jira id found!')
    return ret[0][1]
