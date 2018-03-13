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
from control.carriers import get_all_carriers

logger = logging.getLogger(__name__)
        
class carriers(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            res = get_all_carriers()
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
    
