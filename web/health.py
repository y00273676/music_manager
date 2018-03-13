#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import logging
import tornado
import traceback
import os
import json
from tornado import gen
from web.base import WebBaseHandler
from control.health import get_all_table_status, repair_db_table

logger = logging.getLogger(__name__)
        
class DBCheck(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'check':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            res = get_all_table_status()
            if isinstance(res, list):
                result['data'] = res
            self.send_json(result)
            
        elif op == 'repair':
            tname = self.get_argument('name', '')
            result = {}
            result['code'] = 1
            if tname:
                result['msg'] = repair_db_table(tname)
            else:
                result['msg'] = '参数错误！'
            result['data'] = None
            self.send_json(result)
