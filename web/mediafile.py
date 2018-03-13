#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
import os
from tornado import gen
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.mediafile import get_all_mediafile,get_by_count,add_new_mediafile
from control.medias import get_file_by_no
import commands
from sql import noAndPathMap
import re

logger = logging.getLogger(__name__)



class mediafile(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None

            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))

            res = get_all_mediafile(page, psize)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
        elif op == 'count':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            res = get_by_count()
            result['data']=res
            self.send_json(result)
        elif op == 'exists':
            _res = {}
            _res['code'] = 1
            _res['msg'] = 'ok'
            _res['result'] = None
            mno = self.get_argument('no', '')
            if not mno:
                _res['code'] = 0
                _res['msg'] = '无效的歌曲编号！'
                self.send_json(_res)
                return
            fpath = get_file_by_no(mno)
            if fpath:
                _res['msg'] = '成功取得文件路径！'
                _res['result'] = fpath
            else:
                _res['code'] = 0
                _res['msg'] = '没有找到文件路径！'
            self.send_json(_res)
            return
        else:
            pass

    @gen.coroutine
    def options(self, op):
        self.send_json('')

    @gen.coroutine
    def post(self, op):
        if op == 'uploads':
            result = {}
            upload_path=''
            fileN= self.get_argument('fileName', '')
            no = fileN[0:fileN.find(".")]
            if noAndPathMap.has_key(no):

                upload_path = noAndPathMap[no]

            start= try_to_int(self.get_argument('start', '0'))
            end= try_to_int(self.get_argument('end', '0'))
            filepath=os.path.join(upload_path,fileN)
            size = 0
            if os.path.exists(filepath):
#                 size=os.path.getsize(filepath)
                if start==0:
                    os.remove(filepath)

            if size < end:
                file_metas=self.request.files['file']
                meta=file_metas[0]
                with open(filepath,'ab') as up:
                    up.write(meta['body'])
                up.close()

            result['result']='success'
            result['data']=size
            result['path']=filepath
            self.send_json(result)

        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            MediaFile_MediaManage_ID = try_to_int(self.get_argument('MediaFile_MediaManage_ID', ''))
            MediaFile_Name = try_to_int(self.get_argument('MediaFile_Name', ''))
            res = add_new_mediafile(MediaFile_MediaManage_ID, MediaFile_Name)
            ret['data'] = res
            self.send_json(ret)

