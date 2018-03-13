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
from control.mediauserset import get_all_mediauserset,add_new_mediauserset,exchange,delete_mediauserset_by_id,get_maxId

logger = logging.getLogger(__name__)
        
class mediauserset(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
     
            #get date from controller:
            res = get_all_mediauserset()
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        elif op == 'max':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = get_maxId()
            result['code'] = 0
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
            try:
                MediaUserSet_Id = self.get_argument('MediaUserSet_Id', '')
                MediaUserSet_MediaId = self.get_argument('MediaUserSet_MediaId', '')
                MediaUserSet_Shunxu = self.get_argument('MediaUserSet_Shunxu', '')
                
                if MediaUserSet_Id == '':
                    ret['msg'] = u'公播ID不能为空！'
                    self.send_json(ret)
                    return
                
                if MediaUserSet_MediaId == '':
                    ret['msg'] = u'歌曲ID不能为空！'
                    self.send_json(ret)
                    return
                
                if MediaUserSet_Shunxu == '':
                    ret['msg'] = u'歌曲顺序不能为空！'
                    self.send_json(ret)
                    return
    
                res = add_new_mediauserset( MediaUserSet_Id, MediaUserSet_MediaId, MediaUserSet_Shunxu)
                if res > 0:
                    ret['code'] = 0
                    ret['msg'] = u'公播歌曲信息添加成功！'
                else:
                    ret['msg'] = u'公播歌曲信息保存失败！'
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)
            
        elif op == 'exchange':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            id1 = self.get_argument('MediaId1', '')
            id2 = self.get_argument('MediaId2', '')
            res = exchange( id1, id2)
            if res > 0:
                result['code'] = 0
                result['msg'] = '操作成功'
            self.send_json(result)
            
        elif op == 'del':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            id = self.get_argument('MediaUserSet_MediaId', '')
            bol = delete_mediauserset_by_id(id)
            if bol:
                result['code'] = 0
                result['msg'] = '删除成功'
            else:
                result['msg'] = '删除失败'
            self.send_json(result)
            
