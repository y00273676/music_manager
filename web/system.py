#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import platform
import datetime
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from web.base import WebBaseHandler

logger = logging.getLogger(__name__)
import socket
hostname = socket.gethostname()

class SystemHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        pl_info = platform.uname()

        sys_info = {
            'hostname' : pl_info[1],
            'os': pl_info[0],
            'kernel': pl_info[2],
            'time': datetime.datetime.now(),
        }
        self.render('system.html', sys_info=sys_info)

