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
import glob
import string


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int
import ConfigParser

from control.boxsetting import add_new_setting
from control.boxset import update_setting
from control.boxset import update_set
from control.boxset import update_flag
from control.boxset import get_all_set_list
from control.boxipset import get_all_set_info
from control.boxipset import update_setip
from control.boxs import update_init_ini
from control.boxs import delete_file_ini
from control.boxs import find_ip_ishave
from control.boxs import find_stb_ishave
from control.boxs import find_stb_name
from control.getlocalip import getLocalIp
from control.servergroups import find_file_servers
from control.serverutils import actionCommand
from control.rooms import get_all_rooms_info


logger=logging.getLogger(__name__)

class BoxsHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('boxs.html')

    @gen.coroutine
    def post(self):

        mtype=self.get_argument('type')

        logger.debug("有反应")
        print mtype

        _res = {}
        _res['code'] = 0

        if  mtype=="1":
            # _res['msg'] = "修改成功！"
            mdata=self.get_argument('mdata')

            changetype=self.get_argument('changetype')
            mjsondata=json.loads(mdata)

            if(changetype=="delete"):
                for item in mjsondata['filename']:
                    delete_file_ini(item)
                    _res['msg'] = "删除成功！"
            elif(changetype=="setting"):
                pass

            self.send_json(_res)
        elif mtype=="3":
            _res = {}
            _res['code'] = 0
            _res['msg'] = 'ip都正确'
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            str_val = cf.get("sec_a", "boxpath")
            for server in find_file_servers():
                ip=server['FileServer_IpAddress']
                print "ip",ip
                if ip=='127.0.0.1':
                    _res['msg'] = ip+"ip地址有误"
                    continue
                if ip==getLocalIp("eth0"):
                    continue
                try:
                    actionCommand(str_val,ip)
                    _res['result']=ip+"同步成功"
                except:
                    _res['code'] = 1
                    _res['result']=ip+"同步失败"
            
            self.send_json(_res)    

        else:
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            files=[];
            print "str_val"
            for filename in glob.glob(str_val+"*.ini"):
                conjson={}
                update_init_ini(filename)
                name=filename.replace(str_val,"")
                mname=name.replace(".ini","")
                conjson['filename']=mname
                conjson['isuse']=find_ip_ishave(filename)
                conjson['Stbtype']=find_stb_ishave(filename)
                conjson['Name']=find_stb_name(filename)
                files.append(conjson)

            infojson={}
            infojson['box']=files
            infojson['server']=find_file_servers()
            infojson['fangtai']=get_all_rooms_info()
            self.send_json(infojson)












