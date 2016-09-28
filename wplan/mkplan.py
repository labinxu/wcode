#!/usr/bin/env python

import re
import os
INPUT_ARGS = ''

def get_abi_to_test(argument):
    switcher = {
        1: "x86",
        2: "",
    }
    return switcher.get(argument, "nothing")
result = ''

def parseAbiType(abiData):
    pass
    # ##########################################
    # res=[]
    # for i, rr in enumerate(r[-6:-2]):

            #     if(rr.lower() == 'fail'):
    #         abi = abitype[i]
    #         res.append(abi)
    #     if(res == []):
    #         break

            # #######################################
    # ## check abi
    # abis = set(res)
    # ABIS = set(abitype.values())
    # ret_abis = abis & ABIS
    # abi_ret = 0
    # for i in ret_abis:
    #     abi_ret |= i
    # print(abi_ret)



def getJiraId(text):
    pattern = re.compile("(https://jira01.devtools.intel.com/browse/)(OAM-\d{5})")
    ret  = pattern.findall(text)
    if(ret == []):
        return text.strip()
    return ret[0][1]


def parseJiraIds(jiraIds):
    return [id.strip().lower() for id  in jiraIds.split(',')]


def shouldTest(jiraId,jiraIds):
    if(jiraId == ''):
        return True

    return jiraId != '' and jiraId.lower() in jiraIds


def parse(filename):
    with open(filename) as f:
        result = {}
        begin = False
        module = ''
        jiraId = ''
        jiraIds = []
        if INPUT_ARGS.jiraids != None:
            jiraIds = parseJiraIds(INPUT_ARGS.jiraids)
            print(jiraIds)
        for l in f.readlines():
            r = l.split(INPUT_ARGS.seperator)
            ##########################################
            ## check begin
            if(not begin):
                if(r[0]=='Module'):
                    begin = True
                continue

            r = r[0:INPUT_ARGS.cut_column]

            # jira ticket
            if(r[-1].strip() != ''):
                jiraId = getJiraId(r[-1].strip())

            if(r[0].strip() != ''):
                module = r[0].strip()
                print(module)

            if(jiraIds != []):
                if(not shouldTest(jiraId, jiraIds)):
                    continue
            # not test
            if(r[1].strip() == ''):
                continue

            rret=[]
            ##### check result
            # add module

            rret.append(module)
            # add testcase
            rret.append(r[1].strip())
            if(not result.has_key(jiraId)):
                result[jiraId]=[]
            result[jiraId].append(rret)


        # display
        return result

def get_file_name(path):
    return os.path.split(path)[1]

def output_plan(result):
    f = open(INPUT_ARGS.output_file, 'wr')
    xmlhead = '<?xml version="1.0" encoding="utf-8"?>\n'
    xmlhead += '<configuration description="Runs failures in %s"/>\n' % INPUT_ARGS.output_file
    xmlhead += ' '*4+'<include name="%s"/>\n' % INPUT_ARGS.test_type
    xmlhead += ' '*4+'<option name="compatibility:plan" value=%s />\n' % get_file_name(INPUT_ARGS.output_file)
    f.write(xmlhead)
    xmlFormat = ' '*4 + '<option name="%s" value="%s %s"/>\n'
    for jiraid, caseset in result.items():
        string = ''
        for case_content in caseset:
            casestr=''
            if(len(case_content) !=2 ):
                continue
            xmlStr = xmlFormat % ("compatibility:include-filter" ,case_content[0], case_content[1])
            f.write(xmlStr)

    xmlStr = '</configuration>'
    f.write(xmlStr)

def cmdline():
    import argparse
    global INPUT_ARGS
    parser = argparse.ArgumentParser()

    parser.add_argument('-c','--cut', action='store',
                        dest="cut_column",
                        default=8,
                        type=int,
                        help='cut column index')
    parser.add_argument('-j', '--jiraid', action="store",
                        dest='jiraids',
                        default=None,
                        help='jira id for plan xml')

    parser.add_argument('-s', '--seperator', action="store",
                        dest='seperator',
                        default='|',
                        help='seperator for source file')

    parser.add_argument('-o', '--output', action="store",
                        dest='output_file',
                        default='plan.xml',
                        help='output file')

    parser.add_argument('-i', '--input', action='store',
                        dest='input_file',
                        required=True,
                        help='input file')

    parser.add_argument('-t', '--type', action='store',
                        dest='test_type',
                        default='cts',
                        help='cts or gts')

    INPUT_ARGS = parser.parse_args()
    return INPUT_ARGS;

def main():
    INPUT_ARGS = cmdline()
    result = parse(INPUT_ARGS.input_file)
    output_plan(result)

if __name__ == '__main__':
    main()
