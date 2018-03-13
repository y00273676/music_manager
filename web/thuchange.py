#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:25:22
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
import os

from control.systemsetting import set_main_server
from control.systemsetting import set_erpserver
from control.systemsetting import set_main_server_ip
from control.modbc import set_is_setting
from control.modbc import set_main_server_first
from control.readthunder import read_all_info
from control.readthunder import set_all_thunder_data

from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int
from control.modbc import read_thunder_changecode
from control.modbc import set_main_ip_odbc
from control.serverutils import restartService
from control.sercrtdog import get_doginfo_by_local

logger=logging.getLogger(__name__)

class ChangeHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        _res = {}
        _res['code'] = 4
        _res['msg'] = "无效！"
        self.send_json(_res)

    @gen.coroutine
    def post(self):
        print  "aaaaaaa"
        mtype=self.get_argument('mtype')
        mdata=self.get_argument('mdata')
        _strcode="utf8"
        cf = ConfigParser.ConfigParser()
        cf.read('path.ini')
        str_val = cf.get("sec_a", "systemparh")
        
        if mtype=="0":
            _res = {}
            _res['code'] = 1
            _res['msg'] = "修改出错"
#             print mdata
            dictdata=json.loads(mdata)
            if len(dictdata)!=0:
#                 mainserver=dictdata['mainserver']
                erpserver=dictdata['erpserver']
#                 set_main_server(str_val,mainserver,_strcode)
                set_erpserver(str_val,erpserver,_strcode)
                
#                 ktv=mjsondata['ktv']
#                 cloudset=mjsondata['cloudset']
                misc=mjsondata['misc']
                set_misc(str_val,misc,_strcode)
#                 set_ktv(str_val,ktv,_strcode)
#                 up_cloud_setting(cloudset)
                _res['code'] = 0
                _res['msg'] = "修改成功！"
            self.send_json(_res)
        elif mtype=="1":
            _res = {}
            _res['code'] = 1
            _res['msg'] = "修改出错"
            dictdata=json.loads(mdata)
            if len(dictdata)!=0:
                set_main_server_first(dictdata,"utf8")
                set_is_setting()
                restartService('twm')
                _res['code'] = 0
                _res['msg'] = "修改成功！"
            self.send_json(_res)
         #获取主数据库ip的地址   
        elif mtype=="2":
            _res = {}
            _res['code'] = 0
            _res['msg'] = "获取信息成功"
            _res['result']=read_all_info()
            self.send_json(_res)
        elif mtype=="3":
            dictdata=json.loads(mdata)
            changecode=dictdata['changecode']
            #获取本地的版本号
            localcode=read_thunder_changecode()
            #如果获取的本地的版本号大于前来获取的
            _res = {}
            _res['code'] = 0
            mtjson={}
            if int(localcode)>int(changecode):
                _res['msg'] = "获取信息成功"
                mtjson['type']=0
                mtjson['thunder']=read_all_info()
                mtjson['versioncode']=localcode
                _res['result']=mtjson
                
            else:
                mtjson['type']=1
                _res['msg'] = "版本没有最新的"
            self.send_json(_res)
        elif mtype=="4":
            _res = {}
            _res['code'] = 1
            _res['msg'] = "修改出错"
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            str_val = cf.get("sec_a", "systemparh")
            dictdata=json.loads(mdata)
            if len(dictdata)!=0:
                set_main_server_ip(str_val,dictdata['DataBaseServerIp'],"utf8")
                set_main_ip_odbc(dictdata)
                restartService('twm')
                _res['code'] = 0
                _res['msg'] = "修改成功！"
                
            self.send_json(_res)
        elif mtype=="5":
            _res = {}
            _res['code'] = 0
            #获取文件内容
            _res['doginfo']=get_doginfo_by_local()
            self.send_json(_res)
        elif mtype=="6":
            dictdata=json.loads(mdata)
            if os.path.exists(dictdata['filename']):
                os.remove(dictdata['filename'])
            _res = {}
            _res['code'] = 0
            #获取文件内容
            self.send_json(_res)
        elif mtype=="7":
            dictdata=json.loads(mdata)
            _res = {}
            _res['code'] = 0
            _res['msg'] = "获取信息成功"
            _res['result']=set_all_thunder_data(dictdata)
            self.send_json(_res)
            
            
            
         
            
        
        