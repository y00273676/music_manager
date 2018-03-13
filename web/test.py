#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from web.base import WebBaseHandler

logger = logging.getLogger(__name__)
import socket
hostname = socket.gethostname()

class TestHandler(WebBaseHandler):

    @gen.coroutine
    def get(self):
        response = {
            'hostname' : hostname,
            'code' : 1,
            'msg' : 'ok',
            'time': time.time(),
            'settings': self.application.settings
        }

