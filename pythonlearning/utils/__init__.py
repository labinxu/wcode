import os
import sys
if '2.' in sys.version.split('|')[0]:
    import urllib2 as ul
else:
    import urllib
    import urllib.request as ul
    # python 3.x中urllib库和urilib2库合并成了urllib库。。
# 其中urllib2.urlopen()变成了urllib.request.urlopen()
#      urllib2.Request()变成了urllib.request.Request() 
# get data


def getData(url, datadir):
    '''
    @param url: data's url
    @param datadir,dir
    '''
    data = None
    file = None
    datafile = url[url.rfind('/')+1:]
    # datafile = datafile.replace('.', '_')
    datafile = os.path.join(datadir, datafile)
    print(datafile)
    if not os.path.exists(datadir):
        os.mkdir(datadir)
        # read from uci data repository
        target_url = url  # data urls
        # 'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data'
        data = ul.urlopen(target_url)
        file = open(datafile, 'w')
        file.write(data.read())
    else:
        file = open(datafile, 'r')
        data = file

    return data
