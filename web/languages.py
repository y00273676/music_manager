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
from control.languages import get_all_languages,update_languages,add_new_language

logger = logging.getLogger(__name__)
        
class languages(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
     
            #get date from controller:
            res = get_all_languages()
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)

    @gen.coroutine
    def post(self, op):
        if op == 'update':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            Language_ID = try_to_int(self.get_argument('Language_ID', ''))
            Language_Name = self.get_argument('Language_Name', '')
            Language_Description = self.get_argument('Language_Description', '')

            if Language_ID <= 0:
                ret['msg'] = u'语种ID错误！'
                self.send_json(ret)
                return
            if Language_Name == '':
                ret['msg'] = u'语种名称不能为空！'
                self.send_json(ret)
                return
 
            res = update_languages(Language_ID,Language_Name,Language_Description)
            if res > 0:
                ret['code'] = 0
                ret['msg'] = u'语种信息修改成功！'
                ret['data'] = res
            else:
                ret['msg'] = u'语种信息修改失败！'
            self.send_json(ret)
        
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            
            Language_ID = self.get_argument('Language_ID', '')
            Language_Name = self.get_argument('Language_Name', '')
            Language_Description = self.get_argument('Language_Description', '')

            if Language_Name == '':
                ret['msg'] = u'语种名称不能为空！'
                self.send_json(ret)
                return

            res = add_new_language(Language_ID, Language_Name, Language_Description)
            if res > 0:
                ret['code'] = 0
                ret['msg'] = u'榜单歌曲信息添加成功！'
            else:
                ret['msg'] = u'榜单歌曲信息保存失败！'
            self.send_json(ret)
            
