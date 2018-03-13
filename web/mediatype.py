#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
import json
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.mediatype import get_all_mediatype,update_mediatype,add_mediatype

logger = logging.getLogger(__name__)
        
class mediatype(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            res = get_all_mediatype()
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
            MediaType_ID = try_to_int(self.get_argument('MediaType_ID', ''))
            MediaType_Name = self.get_argument('MediaType_Name', '')
            MediaType_Description = self.get_argument('MediaType_Description', '')
            MediaType_IsMovie = self.get_argument('MediaType_IsMovie', '')
            MediaType_IsKaraok = self.get_argument('MediaType_IsKaraok', '')
            MediaType_IsAds = self.get_argument('MediaType_IsAds', '')
            MediaType_NewTypeID = self.get_argument('MediaType_NewTypeID', '')

            if MediaType_ID <= 0:
                ret['msg'] = u'歌曲类型ID错误！'
                self.send_json(ret)
                return
            if MediaType_Name == '':
                ret['msg'] = u'歌曲类型名称不能为空！'
                self.send_json(ret)
                return
 
            res = update_mediatype(MediaType_ID,MediaType_Name,MediaType_Description,MediaType_IsMovie,MediaType_IsKaraok,MediaType_IsAds,MediaType_NewTypeID)
            if res:
                ret['code'] = 0
                ret['msg'] = u'语种信息修改成功！'
            else:
                ret['msg'] = u'语种信息修改失败！'
            self.send_json(ret)
            
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            jsonData=json.loads(self.request.body)
            add_mediatype(**jsonData)

