#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author LBX
copyright
"""
import asynchat
import logging

class EchoHandler(asynchat.async_chat):
    def __init__(self, sock):
        self.received_data = []
        self.logger = logging.getLogger('EchoHandler')
        asynchat.async_chat.__init__(self, sock)

        self.process_data = self._process_command
        self.set_terminator('\n')

    def collect_incoming_data(self, data):
        self.logger.debug(
            'collect_incoming_data() -> (%d bytes) %r',
            len(data), data)

        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        self.process_data()

    def _process_command(self):
        command = ''.join(self.received_data)
        self.logger.debug('_process_command() %r', command)
        command_verb, command_arg = command.strip().split(' ')
        expected_data_len = int(command_arg)
        self.set_terminator(expected_data_len)
        self.process_data = self._process_message
        self.received_data = []

    def _process_message(self):
        to_echo = ''.join(self.received_data)
        self.logger.debug('_process_message() echoing %r', to_echo)
        self.push(to_echo)
        self.close_when_done()
