#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""

import asyncore
# import logging
import socket
from asynchat_echo_handler import EchoHandler


class EchoServer(asyncore.dispatcher):
    """
    xxx
    """
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(1)

    def handle_accept(self):
        client_info = self.accept()
        EchoHandler(sock=client_info[0])
        self.handle_close()

    def handle_close(self):
        self.close()
