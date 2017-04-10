#!/usr/bin/python

import threading
import paramiko
import subprocess


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/labinxu/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))


if __name__ == '__main__':
    ssh_command('127.0.0.1', 'cnlxu','bajie110', 'ls')
