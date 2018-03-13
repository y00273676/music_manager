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
from control.artists import get_all_artists, get_all_artists_bypage, \
        add_new_artists, update_artists, \
        delete_artists_by_id, get_artists_by_id

logger = logging.getLogger(__name__)

class ArtistsHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if not self.check_login():
            return
        if op == None:
            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '70'))

            #use default value if it's not valid
            if page < 1:
                page = 1
            if psize < 5 or psize > 70:
                psize = 70

            #get date from controller:
            res = get_all_artists_bypage(page, psize)
            total = 0
            artslist = {}
            if isinstance(res, dict):
                total = res['total']
                artslist = res['matches']
            pageinfo = self.page_info('/artists', total, psize, page)

            self.render('artists.html', pageinfo=pageinfo, artslist=artslist, short_desc=self.short_desc)
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get date from controller:
            res = get_all_artists()
            if isinstance(res, list):
                result['data'] = {}
                result['data']['matches'] = res
                result['data']['total'] = len(res)
            self.send_json(result)
        elif op == 'get':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            sid = try_to_int(self.get_argument('id', '0'))
            if sid > 0:
                res = get_artists_by_id(sid)
                if isinstance(res, dict):
                    ret['code'] = 0
                    #res['artistssongs'] = res['artistssongs'].replace(',', '\n')
                    ret['data'] = res
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
                res = delete_artists_by_id(sid)
                if res:
                    ret['code'] = 0
                    ret['msg'] = u'删除歌星推荐信息成功！'
                else:
                    ret['msg'] = u'删除歌星推荐信息失败！'
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
            artsid = try_to_int(self.get_argument('artsid', ''))
            artsname = self.get_argument('artsname', '')
            artstitle = self.get_argument('artstitle', '')
            artsdesc = self.get_argument('artsdesc', '')
            bgimage = self.get_argument('filepath', '')
            artslist = self.get_argument('artslist', '')
            artistsorder = try_to_int(self.get_argument('artistsorder', ''))

            if artsid <= 0:
                ret['code'] = 1
                ret['msg'] = u'推荐信息ID不正确，请重新加载页面！'
                self.send_json(ret)
                return

            if artsname == '' or len(artsname) > 70:
                ret['code'] = 1
                ret['msg'] = u'推荐名称不能为空！'
                self.send_json(ret)
                return

            if artstitle == '' or len(artstitle) > 70:
                ret['code'] = 1
                ret['msg'] = u'推荐标题不能为空且不能超过70字！'
                self.send_json(ret)
                return

            arts= artslist.strip().split('\n')
            arts = self._strip_artiste_list(arts)
            if len(arts) == 0 or len(arts) > 70:
                ret['code'] = 1
                ret['msg'] = u'推荐歌星不能为空且最多不能超过70个！'
                self.send_json(ret)
                return

            #if bgimage == '':
            #    ret['code'] = 1
            #    ret['msg'] = u'图片链接不能为空，请确认文件上传成功！'
            #    self.send_json(ret)
            #    return
            res = update_artists(artsid, artsname, artstitle, artsdesc, arts, bgimage)
            if res:
                ret['code'] = 0
                ret['msg'] = u'推荐歌星信息修改成功！'
            else:
                ret['msg'] = u'推荐歌星信息修改失败！'
            self.send_json(ret)
        elif op == 'add':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            ret['msg'] = ''

            artsname = self.get_argument('artsname', '')
            artstitle = self.get_argument('artstitle', '')
            artsdesc = self.get_argument('artsdesc', '')
            bgimage = self.get_argument('filepath', '')
            artslist = self.get_argument('artslist', '')
            artistsorder = try_to_int(self.get_argument('artistsorder', ''))

            if artsname == '' or len(artsname) > 70:
                ret['code'] = 1
                ret['msg'] = u'推荐名称不能为空！'
                self.send_json(ret)
                return

            if artstitle == '' or len(artstitle) > 70:
                ret['code'] = 1
                ret['msg'] = u'推荐标题不能为空且不能超过70字！'
                self.send_json(ret)
                return

            arts= artslist.strip().split('\n')
            arts = self._strip_artiste_list(arts)
            if len(arts) == 0 or len(arts) > 70:
                ret['code'] = 1
                ret['msg'] = u'推荐歌星不能为空且最多不能超过70个！'
                self.send_json(ret)
                return


            res = add_new_artists(artsname, artstitle, artsdesc, arts, bgimage)
            if res:
                ret['code'] = 0
                ret['msg'] = u'推荐信息添加成功！'
            else:
                ret['msg'] = u'推荐信息添加失败！'
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)

    def _strip_artiste_list(self, arts):
        '''
        align the song list:
        1. strip for each song number
        2. strip the repeated song number
        '''
        new_list = []
        for s in arts:
            num = s.strip()
            if num == '':
                continue
            if num not in new_list:
                new_list.append(num)
        return new_list

