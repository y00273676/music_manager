#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-20 10:34:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$



import time
import setting
import logging
import hashlib
import traceback
import json
import re
import ConfigParser


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from control.fileservers import sp_modifyadvertisementstatus
from control.fileservers import sp_modifygapbetweenmedias
from control.configures import get_all_config_info

class KtvSettingHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        mfrom =self.get_argument('from');
        if mfrom=='0':
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            self.send_json(_res)
        elif mfrom=='1':

            _res = {}
            _res['code'] = 0
            config=get_all_config_info()[18]
            mjson={}
            type=config['config_value']
            mjson['type']=type
            mjson['time']='2'
            _res['result'] =  mjson

            _res['msg'] = "修改成功！"
            self.send_json(_res)


    @gen.coroutine
    def post(self):
        pass
