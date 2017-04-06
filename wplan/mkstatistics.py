# -*- coding:utf-8 -*-
import mechanize
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import utils

# #######################
INPUT_ARGS = ''
ASSIGNEE=''

def debugWritefile(data,filename):
    with open(filename,'w') as f:
        f.write(data)

# jira web
def login(user, passwd):
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)  
    br.set_handle_referer(True)  
    br.set_handle_robots(False)  
    br.set_handle_frameworkrefresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)  
    br.set_debug_http(False)
    response = br.open('https://jira01.devtools.intel.com/login.jsp?os_destination=%2Fsecure%2FDashboard.jspa')
    br.select_form(nr=1)
    br['os_username'] = INPUT_ARGS.user
    br['os_password'] = INPUT_ARGS.passwd
    br.submit()
    return br

# #######################
def getComments(jiraId):

    global INPUT_ARGS
    br = login(INPUT_ARGS.user, INPUT_ARGS.passwd)
    response = br.open('https://jira01.devtools.intel.com/browse/%s' % jiraId)
    data = br.response().read()
    print("Query %s" % jiraId)
    return parseHtml(data)

def checkComments(comments):
    for comment in comments:
        if olderThan(comment[0],7):
            return ASSIGNEE
        else:
            return 'In Progress'

def checkTime(time):
    #if it's between week
    pass

def olderThan(time, days):
    deltatime = datetime.now() - time
    if deltatime.days- days > 0:
        return True

def parseHtml(data):
    global ASSIGNEE
    soup = BeautifulSoup(data,'html.parser')

    # find Assignee
    assigneeTag = soup.find('span',attrs={'id':"assignee-val"})
    ASSIGNEE = assigneeTag.find('span',attrs={'class':"user-hover"}).text.strip()
    #attr = {'class':"issue-data-block activity-comment twixi-block  expanded"}
    attrs = {'class':"twixi-wrap verbose actionContainer"}

    commentsTag = soup.findAll('div',attrs=attrs)
    commentAttrs = {'class':'action-body flooded'}

    comments =[]
    for itemTag in commentsTag:
        user = itemTag.find('a', attrs={'class':"user-hover user-avatar"})
        user = user.text

        timeTag = itemTag.find('time')
        timeText = datetime.strptime(timeTag['datetime'], "%Y-%m-%dT%H:%M:%S+%f")

        commentTag = itemTag.find('div',attrs={'class':"action-body flooded"})
        comment = commentTag.find('p')
        comment = comment.text.strip('\n\r\t')
        comments.append((timeText, user, comment))
    return comments


def countRowFailuers(data):
    data = [item.strip().lower() for item in data]
    count = 0
    for d in data:
        if d == 'fail':
            count += 1
    return count


def countFailuers(data):
    pass


GComments ={}
def parseComments(jiraId):
    global GComments
    content = ''
    if GComments.has_key(jiraId):
        content = GComments[jiraId]
    else:
        comments = getComments(jiraId)
        comment = checkComments(comments)
        GComments[jiraId] = comment
    return content


def fixStatus(r):
    if r[9].strip().lower() in ['pending', 'triage', 'verify']:
        r[9] = 'In Progress'
    return r


def parse(filename):
    result = []
    with open(filename) as f:
        begin = False
        counter = False;
        counterNum = 0
        markLine = ''
        for l in f.readlines():
            r = l.split(INPUT_ARGS.seperator)

            if(not begin):
                if(r[0].strip()=='Module'):
                   begin = True
                result.append(r);
                continue
            else:
                if(r[1].strip() == ''):
                    result.append(r)
                    continue
                else:
                    r = r[0:11]
                    if len(r)<11:
                        extendList = (len(r)-11) * ['']
                        r.extend(extendList)
                    r = fixStatus(r)
                    r[-1] = r[-1].strip()

            result.append(r)
            failCells = r[2:6]

            # get comments from jira
            try:
                jiraId = utils.GetJiraId(r[7])
                checkComments = True
            except Exception,e:
                jiraId = r[7].strip()
                # failNum = countRowFailuers(failCells)
                if jiraId != '':
                    r[6] = str(-1)#failNum
                    checkComments = False

            if(jiraId != '' and checkComments):
                if INPUT_ARGS.run_mode=='real':
                    comment = parseComments(jiraId)
                    print("JiraId %s comment %s" % (jiraId, comment))

            # fail number
            failNumber = len(r)>6 and r[6].strip() or ''

            if(failNumber != ''):
                if(counterNum != 0):
                    # set markLine
                    if counterNum != int(markLine[6].strip()):
                        markLine[-1] = "%s\%s" % (str(counterNum), markLine[6])
                        markLine[6] = str(counterNum)
                    counterNum = 0

                failNumber = int(failNumber)
                counter = False
                totalFails=countRowFailuers(failCells)
                if(failNumber != totalFails):
                    markLine = r
                    counterNum = totalFails
                    counter = True
            else:
                if(counter):
                    # next count
                    counterNum += countRowFailuers(failCells)

    return result


def output(result):
    table = []
    if INPUT_ARGS.output_type == 'txt':
        seperator = INPUT_ARGS.seperator
    else:
        seperator = ','

    rowFormat = "%s"+seperator
    for row in result:
        rowstr = ''
        for cell in row:
            if(cell.strip()==''):
                rowstr += seperator
            else:
                rowstr += rowFormat % cell
        table.append(rowstr+'\n')

    with open(INPUT_ARGS.output_file, 'w') as f:
        f.writelines(table)


def cmdline(args=None):
    import argparse
    global INPUT_ARGS

    parser = argparse.ArgumentParser()
    if(args != None):
        return parser.parse_args(args)

    parser.add_argument('-u', '--user',
                        action='store',
                        dest='user',
                        help='user to login')

    parser.add_argument('-p', '--passwd',
                        action='store',
                        help='password for user')

    parser.add_argument('-s', '--seperator', action="store",
                        dest='seperator',
                        default='|',
                        help='seperator for source file')

    parser.add_argument('-o', '--output', action="store",
                        dest='output_file',
                        default='cts_result_st.txt',
                        help='output file')

    parser.add_argument('-t', '--type', action="store",
                        dest='output_type',
                        default='txt',
                        help='output file')
    
    parser.add_argument('-i', '--input', action='store',
                        dest='input_file',
                        required=True,
                        default='./data/cts_report.txt',
                        help='input file')

    parser.add_argument('-m','--mode',
                        dest='run_mode',
                        default='real',
                        help='run mode debug or real')

    INPUT_ARGS = parser.parse_args()

    return INPUT_ARGS;


def main():
    args = cmdline()
    result = parse(args.input_file)
    output(result)

if __name__=='__main__':
    main()
