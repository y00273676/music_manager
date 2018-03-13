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
from control.image import get_all_image, add_new_image, update_image, \
        delete_image_by_id, get_image_by_id, get_image_by_sectionid

logger = logging.getLogger(__name__)

class ImageHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if not self.check_login():
            return
        if op == None:
            #get arguments
            sectionid = try_to_int(self.get_argument('sectionid', '0'))
            if sectionid <=0:
                raise tornado.web.HTTPError(500)
            #get date from controller:
            res = get_image_by_sectionid(sectionid)
            if isinstance(res, list):
                images = res
            else:
                images = []
            self.render('image.html', images=images, short_desc=self.short_desc)
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get date from controller:
            res = get_all_image()
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
            #self.render('image.html', total=total, page=page, psize=psize, images=images, short_desc=self.short_desc)
        elif op == 'get':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            sid = try_to_int(self.get_argument('id', '0'))
            if sid > 0:
                sect = get_image_by_id(sid)
                if isinstance(sect, dict):
                    ret['code'] = 0
                    ret['data'] = sect
            self.send_json(ret)
        elif op == 'update':
            raise tornado.web.HTTPError(405)
        elif op == 'add':
            raise tornado.web.HTTPError(405)
        elif op == 'del':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            sid = try_to_int(self.get_argument('id', '0'))
            if sid > 0:
                res = delete_image_by_id(sid)
                if res:
                    ret['code'] = 0
                    ret['msg'] = '删除image信息成功！'
                else:
                    ret['msg'] = '删除模块区域信息失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)

    @gen.coroutine
    def post(self, op):
        if not self.check_login():
            return
        if op == 'update':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            imageid = try_to_int(self.get_argument('singleID', ''))
            sectionid = self.get_argument('picmenu', '')
            picorder = try_to_int(self.get_argument('picorder', ''))
            picdesc = self.get_argument('picdesc', '0')
            picurl = self.get_argument('filepath', '')

            if imageid <= 0:
                ret['msg'] = '图片信息ID不能为空！'

            if sectionid == '':
                ret['msg'] = '模块区域代码不能为空！'
            if picorder== '':
                ret['msg'] = '显示顺序不能为空且应为数字！'
            if picdesc == '':
                ret['msg'] = '图片说明不能为空！'
            if picurl == '':
                ret['msg'] = '图片链接不能为空，请确认文件上传成功！'
            res = update_image(imageid, sectionid, picorder, picdesc, picurl)
            if res:
                ret['code'] = 0
                ret['msg'] = '图片信息修改成功！'
            else:
                ret['msg'] = '添加图片信息失败！'
            self.send_json(ret)
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            sectionid = self.get_argument('picmenu', '')
            picorder = self.get_argument('picorder', '')
            picdesc = self.get_argument('picdesc', '0')
            picurl = self.get_argument('filepath', '')
            if sectionid == '':
                ret['msg'] = '模块区域代码不能为空！'
            if picorder== '':
                ret['msg'] = '显示顺序不能为空且应为数字！'
            if picdesc == '':
                ret['msg'] = '图片说明不能为空！'
            if picurl == '':
                ret['msg'] = '图片链接不能为空，请确认文件上传成功！'

            res = add_new_image(sectionid, picorder, picdesc, picurl)
            if res:
                ret['code'] = 0
                ret['msg'] = '图片信息添加成功！'
            else:
                ret['msg'] = '保存信息失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)
