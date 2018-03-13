#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import setting
import logging
import traceback
import tornado
import json
import re

from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int
from tsjob.cloudlogin import CloudLoginTask

from control.configs import get_all_config,update_setconfig
from control.modbc import get_all_thunder_ini

logger=logging.getLogger(__name__)

class ConfigHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            _res = dict(code=0, msg='ok', result=None)
            ret = get_all_config()
            _res['result'] = ret
            _res['dbhost'] = get_all_thunder_ini()['mainserver']['DataBaseServerIp']

            self.send_json(_res)
            return
 
            #list all room info
            pass
        elif op == 'get':
            pass
        else:
            raise tornado.web.HTTPError(405)

    @gen.coroutine
    def post(self, op):
        if op == 'update':
            '''
            '''
            _res = dict(code=0, msg='保存成功！', result=None)
            cfg = json.loads(self.request.body)
            ret = update_setconfig(cfg)
            if ret:
                if 'CloudMusic_passwd' in cfg.keys() and cfg['CloudMusic_passwd']:
                    CloudLoginTask.get_auth_info()
                    _bres, _msg = CloudLoginTask.cloud_login_msg()
                    if _bres:
                        _res['msg'] += "云端帐号登录测试成功！"
                    else:
                        _res['msg'] += "云端帐号登录测试失败！云端消息：%s" % _msg
            else:
                _res['code'] = 1
                _res['msg'] = "保存失败!"

            self.send_json(_res)
            return
        else:
            raise tornado.web.HTTPError(405)

