#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

import sys, os, re, urllib, urlparse
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def Sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password):
    '''''
    @subject: subject
    @msg:content
    @toaddrs:
    @fromaddr:
    @smtpaddr:smtp server
    @password:
    '''
    mail_msg = MIMEMultipart()
    if not isinstance(subject,unicode):
        subject = unicode(subject, 'utf-8')
    mail_msg['Subject'] = subject
    mail_msg['From'] = fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)
        s.login(fromaddr, password)
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())
        s.quit()
    except Exception as e:
        print("Error: unable to send email")
        print(traceback.format_exc())

if __name__ == '__main__':
    fromaddr = "wsndnr@163.com"
    smtpaddr = "smtp.163.com"
    toaddrs = ["wsndnr@163.com"]
    subject = "Hello wsndnr"
    password = "zhutousan110"
    msg = "hi lbx"
    Sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password)

if __name__ == '__main__':
    fromaddr = "wsndnr@163.com"
    smtpaddr = "smtp.163.com"
    toaddrs = ["wsndnr@163.com"]
    subject = "Hello wsndnr"
    password = "zhutousan110"
    msg = "hi lbx"
    Sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password)
