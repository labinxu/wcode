# -*- coding:utf-8 -*-
import utils

# #######################
INPUT_ARGS = ''

def debugWritefile(data,filename):
    with open(filename,'w') as f:
        f.write(data)

def parse(filename):

    result = {}
    result['In progress']={}
    result['Patch Ready']={}
    result['Patch Merged']={}
    inProgress='In Progress'
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
                # jiraid, failed number, comments
                try:
                    status = r[9].strip()
                except IndexError,e:
                    print(l)
                    continue
                if not result.has_key(status):
                    result[status]={}
                    componment = r[8].strip()
                    if not result[status].has_key(componment):
                        result[status][componment]=[]
                try:
                    result[status][componment].append("%s %s. %s"%(r[7],r[6],r[-1].strip()))
                except KeyError,e:
                    print(status, componment)


        return result

def output(result):
    docxStr=''
    for status, componments in result.items():
        docxStr += "*%s\n"%status
        for  componment, contents in componments.items():
            docxStr += "**%s\n"%componment
            for content in contents:
                docxStr += "***%s\n" % content

    with open(INPUT_ARGS.output_file,'w') as f:
        f.writelines(docxStr)


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
