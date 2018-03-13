#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.section import get_all_section, get_all_section_bypage, get_section_by_id,\
        update_section, add_new_section, delete_section_by_id

logger = logging.getLogger(__name__)

class SectionHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if not self.check_login():
            return
        if op == None:
            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))

            #use default value if it's not valid
            if page < 1:
                page = 1
            if psize < 5 or psize > 51:
                psize = 15

            #get date from controller:
            res = get_all_section_bypage(page, psize)
            total = 0
            sections = []
            if isinstance(res, dict):
                total = res['total']
                sections = res['matches']

            pageinfo = self.page_info('/section', total, psize, page)

            self.render('section.html', pageinfo=pageinfo, sections=sections, short_desc=self.short_desc)
        elif op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get date from controller:
            res = get_all_section()
            if isinstance(res, list):
                result['code'] = 0
                result['data'] = {}
                result['data']['matches'] = res
                result['data']['total'] = len(res)
            self.send_json(result)
            #self.render('section.html', total=total, sections=sections, short_desc=self.short_desc)
        elif op == 'get':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            sid = try_to_int(self.get_argument('id', '0'))
            if sid > 0:
                sect = get_section_by_id(sid)
                if isinstance(sect, dict):
                    ret['code'] = 0
                    ret['data'] = sect
            #print str(ret)
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
                res = delete_section_by_id(sid)
                if res:
                    ret['code'] = 0
                    ret['msg'] = '删除模块区域信息成功！'
                else:
                    ret['msg'] = '删除模块区域信息失败！'
            self.send_json(ret)
        else:
            self.render('section.html')

    @gen.coroutine
    def post(self, op):
        if not self.check_login():
            return
        if op == 'update':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            #verid=1&moudlecode=HOME_01&moudledesc=%E4%B8%BB%E9%A1%B5%E8%83%8C%E6%99%AF&imgwidth=1920&imgheight=1081
            se_id = try_to_int(self.get_argument('sectionid', '0'))
            sectioncode = self.get_argument('sectioncode', '')
            sectiondesc = self.get_argument('sectiondesc', '')
            imgwidth = self.get_argument('imgwidth', '0')
            imgheight = self.get_argument('imgheight', '0')
            if se_id <= 0:
                ret['msg'] = '无效的ID值'
                self.send_json(ret)
            elif sectioncode == '' or sectiondesc == '':
                ret['msg'] = '模块区域代码或者模块区域描述不能为空！'
                self.send_json(ret)
            else:
                res = update_section(se_id, sectioncode, sectiondesc, imgwidth, imgheight)
                if res:
                    ret['code'] = 0
                    ret['msg'] = '模块区域保存成功！'
                else:
                    ret['msg'] = '保存信息失败！'
            self.send_json(ret)
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            #verid=1&moudlecode=HOME_01&moudledesc=%E4%B8%BB%E9%A1%B5%E8%83%8C%E6%99%AF&imgwidth=1920&imgheight=1081
            #se_id = try_to_int(self.get_argument('sectionid', '0'))
            sectioncode = self.get_argument('sectioncode', '')
            sectiondesc = self.get_argument('sectiondesc', '')
            imgwidth = self.get_argument('imgwidth', '0')
            imgheight = self.get_argument('imgheight', '0')
            if sectioncode == '' or sectiondesc == '':
                ret['msg'] = '模块区域代码或者模块区域描述不能为空！'
            elif imgwidth <= 0 or imgheight <= 0:
                ret['msg'] = '模块区域高度和宽度不能小于0！'
            else:
                res = add_new_section(sectioncode, sectiondesc, imgwidth, imgheight)
                if res:
                    ret['code'] = 0
                    ret['msg'] = '模块区域保存成功！'
                else:
                    ret['msg'] = '保存信息失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)

