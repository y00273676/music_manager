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
from control.actortype import get_all_actortype

logger = logging.getLogger(__name__)
        
class actortype(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            res = get_all_actortype()
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        

