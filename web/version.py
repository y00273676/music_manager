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
from control.version import get_all_version, get_version_by_id, add_new_version,\
        update_version, delete_version_by_id

logger = logging.getLogger(__name__)

class VersionHandler(WebBaseHandler):
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
            res = get_all_version(page, psize)
            total = 0
            versions = []
            if isinstance(res, dict):
                total = res['total']
                versions = res['matches']

            pageinfo = self.page_info('/version', total, psize, page)

            self.render('version.html', pageinfo=pageinfo, versions=versions, short_desc=self.short_desc)
        elif op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))

            #use default value if it's not valid
            if page < 1:
                page = 1
            if psize < 5 or psize > 51:
                psize = 15

            #get date from controller:
            res = get_all_version(page, psize)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
            #self.render('version.html', total=total, versions=versions, short_desc=self.short_desc)
        elif op == 'get':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            sid = try_to_int(self.get_argument('id', '0'))
            if sid > 0:
                sect = get_version_by_id(sid)
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
                res = delete_version_by_id(sid)
                if res:
                    ret['code'] = 0
                    ret['msg'] = u'删除版本信息成功！'
                else:
                    ret['msg'] = u'删除版本信息失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)
            
    @gen.coroutine
    def post(self, op):
        self.check_login()
        if op == 'update':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            verid = try_to_int(self.get_argument('verid', ''))
            sysversion = self.get_argument('sysversion', '')
            channelid = try_to_int(self.get_argument('channelid', ''))
            vercode = self.get_argument('vercode', '')
            verdesc = self.get_argument('verdesc', '')
            versize = try_to_int(self.get_argument('verlength', ''))
            auto_update = self.get_argument('verradio', '')
            force_update = try_to_int(self.get_argument('sureradio', ''))
            ver_url = self.get_argument('filepath', '')

            if verid <= 0:
                ret['msg'] = u'版本信息无效！'
                self.send_json(ret)
                return
            if channelid <= 0: 
                ret['msg'] = u'渠道不能为空！'
                self.send_json(ret)
                return
            if vercode == '':
                ret['msg'] = u'版本名称不能为空！'
                self.send_json(ret)
                return
            if verdesc == '':
                ret['msg'] = u'版本说明不能为空！'
                self.send_json(ret)
                return
            if versize <= 0:
                ret['msg'] = u'版本文件大小不能为空且必须为数字！'
                self.send_json(ret)
                return
            if ver_url == '':
                ret['msg'] = u'版本文件路径不能为空，请确认文件上传成功！'
                self.send_json(ret)
                return

            userid = try_to_int(self.user['UserNo'])
            if userid <= 0:
                #if user info invalid, logout directly
                self.redirect('/logout')
                return

            res = update_version(verid, vercode, channelid, sysversion, verdesc, versize, auto_update, force_update, ver_url, userid)
            if res:
                ret['code'] = 0
                ret['msg'] = u'版本信息保存成功！'
            else:
                ret['msg'] = u'版本信息保存失败！'
            self.send_json(ret)
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''
            #verid=&vercode=1.1.1&vercompare=1&verdesc=asdf&verlength=309&hidden_file=c349443c1e7dcfe8d73d0be2a323708e
            #.apk&filepath=http%3A%2F%2Fwstest.kssws.ks-cdn.com%2Fcloud%2Fapk%2F2016-05%2Fc349443c1e7dcfe8d73d0be2a323708e
            #.apk&verradio=2&sureradio=0
            #ver_channel = self.get_argument('channel', '')
            channelid = try_to_int(self.get_argument('channelid', ''))
            sysversion = self.get_argument('sysversion', '')
            vercode = self.get_argument('vercode', '')
            verdesc = self.get_argument('verdesc', '')
            versize = try_to_int(self.get_argument('verlength', ''))
            auto_update = self.get_argument('verradio', '')
            force_update = try_to_int(self.get_argument('sureradio', ''))
            ver_url = self.get_argument('filepath', '')


            if channelid <= 0: 
                ret['msg'] = u'渠道不能为空！'
                self.send_json(ret)
                return
            if vercode == '':
                ret['msg'] = u'版本名称不能为空！'
                self.send_json(ret)
                return
            if verdesc == '':
                ret['msg'] = u'版本说明不能为空！'
                self.send_json(ret)
                return
            if versize <= 0:
                ret['msg'] = u'版本文件大小不能为空且必须为数字！'
                self.send_json(ret)
                return
            if ver_url == '':
                ret['msg'] = u'版本文件路径不能为空，请确认文件上传成功！'
                self.send_json(ret)
                return

            userid = try_to_int(self.user['UserNo'])
            if userid <= 0:
                self.redirect('/logout')
                return

            res = add_new_version(vercode, channelid, sysversion, verdesc, versize, auto_update, force_update, ver_url, userid)
            if res:
                ret['code'] = 0
                ret['msg'] = u'版本信息添加成功！'
            else:
                ret['msg'] = u'版本信息保存失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)


