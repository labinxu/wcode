# -*- coding:utf-8 -*-
import utils

# #######################
INPUT_ARGS = ''

def debugWritefile(data,filename):
    with open(filename,'w') as f:
        f.write(data)

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
                continue
            else:
                # status:
                r = r[0:11]
                if r[]
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
