#!/usr/bin/python

#!/usr/bin/python

import mechanize
import commands

lsoutput = commands.getoutput('ls')
print(lsoutput)
# def getUrl(url='www.baidu.com'):
#     br=mechanize.Browser()
#     br.open(url)
#     br.select_form(nr=0)
