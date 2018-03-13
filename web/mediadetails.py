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
from control.mediadetails import get_all_mediadetails,get_by_count

logger = logging.getLogger(__name__)
        
class mediadetails(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get date from controller:
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))
            text = self.get_argument('text', '')
            res = get_all_mediadetails(page, psize, text)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        if op == 'count':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            text = self.get_argument('text', '') 
            type = self.get_argument('type', '') 
            res = get_by_count(text,type)
            result['data']=res
            self.send_json(result)
            
    @gen.coroutine
    def options(self, op):
        self.send_json('')
        
    @gen.coroutine
    def post(self, op):
        if op == 'upload':
            upload_path=os.path.join(os.path.dirname(__file__),'files')  
            if not os.path.isdir(upload_path):
                os.makedirs(upload_path)
            file_metas=self.request.files['file']   
            for meta in file_metas:
                filename=meta['filename']
                filepath=os.path.join(upload_path,filename)
                with open(filepath,'wb') as up:   
                    up.write(meta['body'])
        result = {}
        result['result']='success'
        result['path']=filepath
        self.send_json(result)
