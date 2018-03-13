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
from control.mainpage import get_all_mainpage, get_all_mainpage_bypage, \
        get_mainpage_by_id,\
        update_mainpage, add_new_mainpage, delete_mainpage_by_id

logger = logging.getLogger(__name__)

class MainPageHandler(WebBaseHandler):
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
            res = get_all_mainpage_bypage(page, psize)
            total = 0
            pages = []
            if isinstance(res, dict):
                total = res['total']
                pages = res['matches']

            pageinfo = self.page_info('/mainpage', total, psize, page)

            self.render('mainpage.html', pageinfo=pageinfo, pages=pages, short_desc=self.short_desc)
        elif op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get date from controller:
            res = get_all_mainpage()
            if isinstance(res, dict):
                result['code'] = 0
                result['data'] = res
            self.send_json(result)
            #self.render('page.html', total=total, pages=pages, short_desc=self.short_desc)
        elif op == 'get':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            sid = try_to_int(self.get_argument('id', '0'))
            if sid > 0:
                sect = get_mainpage_by_id(sid)
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
                res = delete_mainpage_by_id(sid)
                if res:
                    ret['code'] = 0
                    ret['msg'] = '删除信息成功！'
                else:
                    ret['msg'] = '删除信息失败！'
            self.send_json(ret)
        else:
            self.render('page.html')

    @gen.coroutine
    def post(self, op):
        if not self.check_login():
            return
        if op == 'update':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            pageid = try_to_int(self.get_argument('pageid', '0'))
            pagename = self.get_argument('pagename', '')
            pagedesc = self.get_argument('pagedesc', '')
            channelid = try_to_int(self.get_argument('channelid', ''))
            bgimage = self.get_argument('filepath', '')
            pubdate = self.get_argument('pubdate', '')
            pubstate = try_to_int(self.get_argument('pubstate', ''))

            if pageid <= 0:
                ret['msg'] = '无效的ID值'
                self.send_json(ret)
                return
            if channelid <= 0:
                ret['msg'] = '渠道信息无效！'
                self.send_json(ret)
                return
            if pagename == '':
                ret['msg'] = '页面名称不能为空！'
                self.send_json(ret)
                return
            else:
                res = update_mainpage(pageid, pagename, pagedesc, 
                        channelid, bgimage, pubdate, pubstate)
                if res:
                    ret['code'] = 0
                    ret['msg'] = '保存信息成功！'
                else:
                    ret['msg'] = '保存信息失败！'
            self.send_json(ret)
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            pagename = self.get_argument('pagename', '')
            pagedesc = self.get_argument('pagedesc', '')
            channelid = try_to_int(self.get_argument('channelid', ''))
            bgimage = self.get_argument('bgimage', '')
            pubdate = self.get_argument('pubdate', '')
            pubstate = try_to_int(self.get_argument('pubstate', ''))


            if channelid <= 0:
                ret['msg'] = '渠道信息无效！'
                self.send_json(ret)
                return
            if pagename == '':
                ret['msg'] = '页面名称不能为空！'
                self.send_json(ret)
                return
            res = add_new_mainpage(pagename, pagedesc, 
                    channelid, bgimage, pubdate, pubstate)
            if res:
                ret['code'] = 0
                ret['msg'] = '信息添加成功！'
            else:
                ret['msg'] = '信息保存失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)

