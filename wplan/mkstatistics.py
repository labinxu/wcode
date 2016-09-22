# -*- coding:utf-8 -*-
import requests
import mechanize
from bs4 import BeautifulSoup
import utils

# #######################
INPUT_ARGS = ''

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
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)  
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


def parseHtml(data):
    attrs = {'class':"issue-data-block activity-comment twixi-block  expanded"}
    soup = BeautifulSoup(data,'html.parser')
    commentsTag = soup.findAll('div',attrs=attrs)
    commentAttrs = {'class':'action-body flooded'}
    comments = {}
    for itemTag in commentsTag:
        user = itemTag.find('a', attrs={'class':"user-hover user-avatar"})
        user = user.text

        time = itemTag.find('time')
        time = time.text

        content = itemTag.find('div',attrs={'class':"action-body flooded"})
        content = content.text
        if not comments.has_key(user):
            comments[time]=[]

        comments[time].append((user,content))

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
        content = doParseComment(comments)
        GComments[jiraId] = content
    return content


def doParseComment(comments):
    item = comments.items()[-1]
    comment = item[-1][-1][-1]
    return comment


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
                    r[-1]=r[-1].strip()

            result.append(r)

            # get comments from jira
            try:
                jiraId = r[7].strip() != '' and utils.GetJiraId(r[7]) or ''
            except Exception,e:
                pass

            if(jiraId != ''):
                comment = parseComments(jiraId)
                print("JiraId %s comment %s" % (jiraId, comment))

            # fail number
            failNumber = len(r)>6 and r[6].strip() or ''
            failCells = r[2:6]
            if(failNumber != ''):

                if(counterNum != 0):
                    # set markLine

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

    with open(INPUT_ARGS.output_file,'w') as f:
        f.writelines(table)


def cmdline(args=None):
    import argparse
    global INPUT_ARGS

    parser = argparse.ArgumentParser()
    if(args != None):
        return parser.parse_args(args)

    parser.add_argument('-u','--user',
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

    INPUT_ARGS = parser.parse_args()

    return INPUT_ARGS;


def main():
    args = cmdline()
    result = parse(args.input_file)
    output(result)

if __name__=='__main__':
    main()
