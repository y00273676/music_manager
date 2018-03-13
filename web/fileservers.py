#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.getfileservice import get_all_fileservers,get_all

logger = logging.getLogger(__name__)


class fileservers(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            
            isMain = self.get_argument('isMain', '0')
            
            res = get_all_fileservers(isMain)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        elif op == 'listAll':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            
            res = get_all()
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)

        
