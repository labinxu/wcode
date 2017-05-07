import hashlib
import sys
import os

def sortBuildName(tag1, tag2):
    #tag1 = 'ICE7360_05.1719.05'
    #tag2 = 'ICE7360_05.1719.01'
    tag_1 = tag1.split('.')
    tag_2 = tag2.split('.')
    for i in range(1, len(tag_1)):
        if int(tag_1[i]) > int(tag_2[i]):
            return tag2, tag1
    return tag1, tag2

def getMD5SHA1(filename):
    fd=open(filename,"rb") #
    fd.seek(0)             #
    line=fd.readline()     #
    md5=hashlib.md5()
    md5.update(line)
    sha1=hashlib.sha1()
    sha1.update(line)
    while line:
        line=fd.readline()
        md5.update(line)
        sha1.update(line)
    fmd5=md5.hexdigest()
    fsha1=sha1.hexdigest()
    fd.close()
    return fmd5, fsha1
