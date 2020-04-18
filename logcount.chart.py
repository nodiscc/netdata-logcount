# -*- coding: utf-8 -*-
# Description: logcount python.d module for netdata
# Author: nodiscc (nodiscc@gmail.com)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from bases.FrameworkServices.SimpleService import SimpleService

priority = 90000
update_every = 10

ORDER = [
    'messages'
]

CHARTS = {
    'messages': {
        'options': [None, 'Messages by level', 'messages', 'messages', 'logcount.messages', 'stacked'],
        'lines': [
            ['info', None, 'absolute'],
            ['error', None, 'absolute'],
            ['warning', None, 'absolute']
        ]
    }
}

RE_error = re.compile(r'error,.*')
RE_warning = re.compile(r'warning,.*')
RE_info = re.compile(r'info,.*')

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS

        self.data = dict()
        self.path = '/var/run/logcount'
        self.modtime = ''
        self.data['error'] = 0
        self.data['warning'] = 0
        self.data['info'] = 0

    def check(self):
        return True

    def get_data(self):
        if not is_readable(self.path) or is_empty(self.path):
            self.debug("{0} is unreadable or empty".format(self.path))
            self.data['error'] = 1
            self.data['warning'] = 0
            self.data['info'] = 0
            return self.data

        try:
            if not self.is_changed():
                self.debug("{0} modification time is unchanged, returning previous values".format(self.path))
                return self.data
            file = open(self.path, 'r')
        except:
            self.error("Error while opening {0}".format(self.path))
            self.data['error'] = 1
            self.data['warning'] = 0
            self.data['info'] = 0
            return self.data

        self.modtime = os.path.getmtime(self.path)
        lines = file.read()
        self.debug("LINES: {}".format(lines))

        try:
            self.data['error'] = re.findall(RE_error, lines)[0].split(',')[1]
        except IndexError as e:
            self.data['error'] = 0
        self.debug("ERROR MESSAGES: {}".format(self.data['error']))

        try:
            self.data['warning'] = re.findall(RE_warning, lines)[0].split(',')[1]
        except IndexError as e:
            self.data['warning'] = 0
        self.debug("WARNING MESSAGES: {}".format(self.data['warning']))

        try:
            self.data['info'] = re.findall(RE_info, lines)[0].split(',')[1]
        except IndexError as e:
            self.data['info'] = 0
        self.debug("INFO MESSAGES: {}".format(self.data['info']))

        return self.data

    def is_changed(self):
        return self.modtime != os.path.getmtime(self.path)

def is_readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)

def is_empty(path):
    return os.path.getsize(path) == 0
