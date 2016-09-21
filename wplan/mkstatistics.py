# -*- coding:utf-8 -*-
import requests
import mechanize
import copy

# #######################
INPUT_ARGS = ''


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
def get_comments(jiraId):
    global INPUT_ARGS
    br = login(INPUT_ARGS.user, INPUT_ARGS.passwd)
    response = br.open('https://jira01.devtools.intel.com/browse/%s' % jiraId)
    print(br.response().read())

def countRowFailuers(data):
    data = [item.strip().lower() for item in data]
    count = 0
    for d in data:
        if d == 'fail':
            count += 1
    return count


def countFailuers(data):
    pass


def parse(filename):
    result = []
    with open(filename) as f:
        begin = False
        counter = False;
        counterNum=0
        for l in f.readlines():
            r = l.split(INPUT_ARGS.seperator)
            if(counter):
                # next count
                if(len(r)>6 and r[6].strip() != ''):
                    counterNum += countRowFailuers(r[2:6])

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
            # fail number
            failNumber = len(r)>6 and r[6].strip() or ''

            if(failNumber != ''):
                if(counterNum != 0):
                    # pre-line number
                    last =copy.copy(result[-1][6])
                    result[-1][6] = "%s\%s" % (counterNum, last)
                    counterNum = 0

                failNumber = int(failNumber)
                counter = False
                # count the failures
                totalFails=countRowFailuers(r[2:6])
                if(totalFails == 0):
                    print(l)
                    print(r[2:6])
                if(failNumber != totalFails):
                    counterNum = totalFails
                    counter = True
    return result


def output(result):
    table = []
    seperator = INPUT_ARGS.seperator
    rowFormat = "%s"+INPUT_ARGS.seperator
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

    parser.add_argument('-s', '--seperator', action="store",
                        dest='seperator',
                        default='|',
                        help='seperator for source file')

    parser.add_argument('-o', '--output', action="store",
                        dest='output_file',
                        default='cts_result_st.txt',
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
