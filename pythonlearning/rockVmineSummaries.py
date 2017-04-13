__author__ = 'labinxu'
import urllib2


# read from uci data repository
target_url = 'https://archive.ics.uci.edu/ml/machine-learning\
-databases/undocumented/connectionist-bench/sonar/sonar.all-data'

data = urllib2.urlopen(target_url)
for line in data:
    print(line)
