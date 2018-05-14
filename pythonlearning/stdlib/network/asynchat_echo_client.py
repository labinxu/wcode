#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""
import asynchat
import logging
import socket

class EchoClient(asynchat.async_chat):
    ac_in_buffer_size = 128
    ac_out_buffer_size = 128

    def __init__(self, host, port, message):
        self.message = message
        self.received_data = []
        self.logger = logging.getLogger('EchoClient')
        asynchat.async_chat.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s',(host, port))
        self.connect((host, port))

    def handle_connect(self):
        self.logger.debug('handle_connect')
        self.push(bytes('ECHO %d\n' % len(self.message)))
        self.push_with_producer(EchoProducer(self.message                                            ))
        self.set_terminator(len(self.message))

    def collect_incoming_data(self, data):
        self.logger.debug('collect_incoming_data() -> (%d)  %r',
                          len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            self.logger.debug('RECEIVED COPY MESSAGE')
        else:
            self.logger.debug('ERROR IN TRANSMISSION')
            self.logger.debug('EXPECTED %r', self.message)
            self.logger.debug('RECEIVED %r', received_message)

class EchoProducer(asynchat.simple_producer):
    logger = logging.getLogger('EchoProducer')
    def more(self):
        response = asynchat.simple_producer.more(self)
        self.logger.debug('more() -> (%s bytes) %r',
                          len(response), response)
        return response
