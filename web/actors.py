#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import json
import setting
import logging
import tornado
import os
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.actors import get_all_actors,get_by_count,update_actor,add_actor

logger = logging.getLogger(__name__)
        
class actors(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))
            text = self.get_argument('text', '') 
            #get date from controller:
            res = get_all_actors(page, psize,text)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        elif op == 'count':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            text = self.get_argument('text', '') 
            res = get_by_count(text)
            result['data']=res
            self.send_json(result)
    @gen.coroutine
    def post(self, op):
        if op == 'update':
            result = dict(code=0, msg='保存成功', data=None)
            a_info = json.loads(self.request.body)
            if 'actor_no' in a_info.keys():
                ret = update_actor(a_info)
            else:
                ret = add_actor(a_info)
            if ret:
                self.send_json(result)
            else:
                result['code'] = 1
                result['msg'] = '保存失败'
                self.send_json(result)
            return

