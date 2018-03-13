#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
import os
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.mediamanage import get_all_mediamanage,get_by_count,add_new_mediamanage

logger = logging.getLogger(__name__)
        
class mediamanage(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
	print 'my op is %s' % (op)
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))
     
            #get date from controller:
            res = get_all_mediamanage(page, psize)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        if op == 'count':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            res = get_by_count()
            result['data']=res
            self.send_json(result)
            
    @gen.coroutine
    def options(self, op):
        self.send_json('')
    
    @gen.coroutine
    def post(self, op):
        if op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            res = add_new_mediamanage()
            ret['data'] = res
            self.send_json(ret)
