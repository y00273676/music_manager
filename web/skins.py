#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from tornado import gen
from web.base import WebBaseHandler
from lib.types import try_to_int
import tornado

from control.skins import get_all_skins, get_local_skin_packages,\
        add_skin,delete_skin

logger=logging.getLogger(__name__)

class SkinsHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            _res = dict(code=0, msg='ok', result=None)
            res = get_all_skins()
            if isinstance(res, dict):
                _res['result'] = res
            self.send_json(_res)
            return
        elif op == 'local':
            _res = dict(code=0, msg='ok', result=None)
            res = get_local_skin_packages()
            _res['result'] = res
            self.send_json(_res)
            return
        else:
            raise tornado.web.HTTPError(405)

    @gen.coroutine
    def post(self, op):
        if op == 'add':
            _res = dict(code=0, msg='添加成功', result=None)
            skin_name = self.get_argument('skin_name', '')
            if skin_name:
                ret = add_skin(dict(skin_name=skin_name, skin_desc=skin_name))
                if not ret:
                    _res['code'] = 1
                    _res['msg'] = '添加失败'
            else:
                _res['code'] = 1
                _res['msg'] = '无效的皮肤名称'
            self.send_json(_res)
            return
        elif op == 'del':
            _res = dict(code=0, msg='删除成功', result=None)
            skin_id = try_to_int(self.get_argument('skin_id', '0'))
            if skin_id > 0:
                ret = delete_skin(skin_id)
                if not ret:
                    _res['code'] = 1
                    _res['msg'] = '删除失败'
            else:
                _res['code'] = 1
                _res['msg'] = '无效的参数'
            self.send_json(_res)
            return
 
        else:
            raise tornado.web.HTTPError(405)

