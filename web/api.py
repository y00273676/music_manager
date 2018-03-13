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

from control.api import get_musicinfos

logger = logging.getLogger(__name__)


class ApiHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'musicinfo':
            _res = {}
            _res['code'] = 1
            _res['msg'] = "错误！"
            _res['data'] = None
            #get arguments
            musicno = try_to_int(self.get_argument('no', '0'))

            lista = get_musicinfos(musicno)
            if lista:
                for item in lista:
                    if item['songid'] == musicno:
                        _res['code'] = 0
                        _res['msg'] = "数据加载完成！"
                        _res['data'] = item
                        break
            else:
                _res['msg'] = "获取数据失败，请稍后重试！"
 
            self.send_json(_res)
        else:
            raise tornado.web.HTTPError(405)

