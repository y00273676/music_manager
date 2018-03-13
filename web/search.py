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
from control.search import get_all_artist_search, get_all_song_search

logger = logging.getLogger(__name__)

class ArtistSearchHandler(WebBaseHandler):
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
            res = get_song_search_bypage(page, psize)
            total = 0
            searches = []
            if isinstance(res, dict):
                total = res['total']
                searches = res['matches']

            pageinfo = self.page_info('/search/artist', total, psize, page)

            self.render('searchartist.html', pageinfo=pageinfo, searches=searches, short_desc=self.short_desc)
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None

            #get date from controller:
            res = get_all_artist_search()
            if isinstance(res, list):
                result['data'] = {}
                result['data']['matches'] = res
                result['data']['total'] = len(res)
            self.send_json(result)
        elif op == 'get':
            raise tornado.web.HTTPError(405)
        elif op == 'update':
            raise tornado.web.HTTPError(405)
        elif op == 'add':
            raise tornado.web.HTTPError(405)
        elif op == 'del':
            raise tornado.web.HTTPError(405)
        else:
            raise tornado.web.HTTPError(405)

class SongSearchHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if not self.check_login():
            return
        if op == None:
            raise tornado.web.HTTPError(405)
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None

            #get date from controller:
            res = get_all_song_search()
            if isinstance(res, list):
                result['data'] = {}
                result['data']['matches'] = res
                result['data']['total'] = len(res)
            self.send_json(result)
        elif op == 'get':
            raise tornado.web.HTTPError(405)
        elif op == 'update':
            raise tornado.web.HTTPError(405)
        elif op == 'add':
            raise tornado.web.HTTPError(405)
        elif op == 'del':
            raise tornado.web.HTTPError(405)
        else:
            raise tornado.web.HTTPError(405)

