#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import time
import setting
import logging
import tornado
import os
import traceback
from tornado import gen
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.addmedia import get_all_addmedia, add_new_addmedia, delete_addmedia_by_id,get_addmedia_by_pathAndName,active_addmedia_by_id
from control.medias import upload_media
from control.mediafile import add_new_mediafile
from sql import noAndPathMap
from orm.mm import getIpIsMain,insertMeidaFilesForAddMedia
import commands
logger = logging.getLogger(__name__)

class addmedia(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None

            res = get_all_addmedia()
            if isinstance(res, dict):
                result['data'] = res
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
                AddMedia_Name = self.get_argument('AddMedia_Name', '')
                AddMedia_Path = self.get_argument('AddMedia_Path', '')
                AddMedia_Type = self.get_argument('AddMedia_Type', '')
                AddMedia_Size = self.get_argument('AddMedia_Size', '')
                AddMedia_SerialNo = self.get_argument('AddMedia_SerialNo', '')
                out = commands.getoutput('df | grep /video/disk')
                out = out.split('\n')
                for i,j in enumerate(out):
                    out[i] = out[i].split(' ')
                    out[i] = [k for k in out[i] if k!='']
                path = []
                for i, j in enumerate(out):
                    path.append(j[4])
                for i, j in enumerate(path):
                    path[i] = int(re.sub('\D', '', j))
                rate = path.index(min(path))
                upload_path = out[rate][5]

                AddMedia_Path_New = os.path.join(upload_path, AddMedia_Path)
                command = 'mv {} {}'.format(AddMedia_Path, AddMedia_Path_New)
                commands.getoutput(command)
                add_new_mediafile(AddMedia_SerialNo, AddMedia_Path_New)
                upload_media(AddMedia_SerialNo, AddMedia_Path_New, AddMedia_Name)
                ret['code'] = 0
                ret['msg'] = u'添加成功！'
            except:
                ret['error'] = traceback.format_exc()
                ret['msg'] = u'添加失败！'
            self.send_json(ret)

        elif op == 'del':
            ret = {}
            try:
                ret['code'] = 1
                ret['data'] = None
                sid = try_to_int(self.get_argument('AddMedia_ID', '0'))
                sno = try_to_int(self.get_argument('AddMedia_SerialNo', '0'))
                if sid > 0 or sno > 0:
                    res = delete_addmedia_by_id(sid,sno)
                    if res:
                        ret['code'] = 0
                        ret['msg'] = u'删除成功！'
                    else:
                        ret['msg'] = u'删除失败！'
            except:
                print traceback.format_exc()
            self.send_json(ret)
