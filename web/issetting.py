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

from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int
from control.modbc import get_all_thunder_ini
from control.modbc import read_is_setting
from control.modbc import set_is_setting
from control.modbc import set_main_server_first
from control.servergroups import find_all_servers_ip
from control.postthunder import postHttp
from control.getlocalip import getLocalIp
from control.checkchange import read_thunder_ini_to_db
from control.serverutils import restartService
from control.readthunder import read_all_info
from control.readthunder import set_all_thunder_data
from control.version import get_system_ver
import socket

from orm.mm import isvild_sql


logger=logging.getLogger(__name__)


class InitSetHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        mdata={}
        #mdata['isset'] = read_is_setting()
        mdata['isset'] = dict(ishasset=1)
        mdata['thunder'] = get_all_thunder_ini()
        sys_info = {}
        sys_info['version'] = get_system_ver()
        mdata['system'] = sys_info
        self.send_json(mdata)
    
    @gen.coroutine
    def options(self):
        self.send_json('')   
    @gen.coroutine
    def post(self):
        ret = {}
       
        
        mdata={}
        mdata['DataBaseServerIp']=self.get_argument('DataBaseServerIp', '127.0.0.1')
#         mdata['UserName']=self.get_argument('UserName', 'root')
#         mdata['Password']=self.get_argument('Password', 'Thunder#123')
        mdata['UserName']='root'
        mdata['Password']='Thunder#123'
        localIP =getLocalIp("eth0")
        mdata['FileServerIP']=localIP
        mflag=0
        if isvild_sql(mdata)==0:

            if set_main_server_first(mdata,"utf8")==0:
                set_is_setting()
                if localIP==mdata['DataBaseServerIp']:
                    read_thunder_ini_to_db()
                    
                    #分发给各个子服务器
                    #获取各个服务器ip
                    try:
                        allip=find_all_servers_ip()
                        jsondata={}
                        for ip in allip:
                            if ip==getLocalIp("eth0"):
                                pass
                            else:
                                state=postHttp(ip,mdata,"4")
                                if state!=0:
                                    print ip+"修改失败"
                    except:
                        pass
                    
                
                mflag=1
                ret['code'] = 0
                ret['result'] = "设置成功,将要重启！"
                
            else:
                ret['code'] = 1
                ret['result']="配置添加失败"
            
            
            #重启服务器

            
#             allip=find_all_servers_ip()
#             print allip
# #                 jsondata={}
#             for ip in allip:
#                 if ip=="10.0.0.3":
#                     pass
#                 else:
#                     state=postHttp(ip,mdata,"1")
#                     if state!=0:
#                         print ip+"修改失败"

        else:
            ret['code'] = 1
            ret['result'] = "设置数据库不正确，请重新设置"
        self.send_json(ret)
        if mflag==1:
            try:
                restartService('twm')
            except:
                pass
        
