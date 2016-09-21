# -*- coding:utf-8 -*-

INPUT_ARGS = ''
def get_abi_to_test(argument):
    switcher = {
        1: "x86",
        2: "",
    }
    return switcher.get(argument, "nothing")
result = ''
def parse(filename):
    f = open(filename)
    abitype= {}
    # abitype[0] = 'x86'
    # abitype[1] = 'x86_64'
    # abitype[2] = 'armeabi-v7a'
    # abitype[3] = 'arm64-v8a'
    abitype[0] = 1 #'x86'
    abitype[1] = 1 #'x86_64'
    abitype[2] = 2 #'armeabi-v7a'
    abitype[3] = 2 #'arm64-v8a'

    result = {}
    begin = False
    module = ''
    jiraId = ''
    for l in f.readlines():
        r = l.split(',')
        if(begin):
            r = r[0:8]
            if(r[0] != ''):
                module = r[0]

            if(r[-1] != ''):
                jiraId = r [-1]

            if(r[1] == ''):
                continue
            ##########################################

            res=[]
            for i, rr in enumerate(r[-6:-2]):

                if(rr.lower() == 'fail'):
                    abi = abitype[i]
                    res.append(abi)
            if(res == []):
                break

            #######################################
            ## check abi
            abis = set(res)
            ABIS = set(abitype.values())
            ret_abis = abis & ABIS
            abi_ret = 0
            for i in ret_abis:
                abi_ret |= i
            # print(abi_ret)

            rret=[]
            ##### check result
            # add module
            rret.append(module)
            # add testcase
            rret.append(r[1])
            if(not result.has_key(jiraId)):
                result[jiraId]=[]
            result[jiraId].append(rret)
        ##########################################
        ## check begin
        if(r[0]=='Module'):
            begin = True
            continue
    # display
    f.close()
    return result


def output_plan(result):
    f = open(INPUT_ARGS.output_file, 'wr')
    xmlhead = '<?xml version="1.0" encoding="utf-8"?>\n'
    xmlhead += '<configuration description="Runs failures in %s"/>\n' % INPUT_ARGS.output_file
    xmlhead += ' '*4+'<include name="%s"/>\n' % INPUT_ARGS.test_type
    f.write(xmlhead)
    xmlFormat = ' '*4 + '<option name="%s" value="%s"/>\n'
    for jiraid, caseset in result.items():
        string = ''
        for case_content in caseset:
            casestr=''
            if(len(case_content) !=2 ):
                continue
            xmlStr = xmlFormat % (case_content[0], case_content[1])
            f.write(xmlStr)

    xmlStr = '</configuration>'
    f.write(xmlStr)

def cmdline():
    import argparse
    global INPUT_ARGS
    parser = argparse.ArgumentParser()

    parser.add_argument('--jiraid', action="store",
                        dest='jiraIds',
                        help='jira id for plan xml')

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
    args = cmdline()
    result = parse(args.input_file)
    output_plan(result)

main()
