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
import socket
import os
import os.path

from lib.types import try_to_int
from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from control.sercrtdog import *
from control.serverutils import restartService
from control.getlocalip import getLocalIp
from control.modbc import *
from control.boxs import dog_all_inianddata
from control.servers import get_server_ips

logger=logging.getLogger(__name__)

class DogHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        self.render('sercrtdog.html')
        
    @gen.coroutine
    def options(self):
        self.send_json('')
   
    @gen.coroutine
    def post(self, op):
        #mtype=self.get_argument('type')
        ret = {}
        #查询
        #if mtype=="1":
        if op == 'get':
            ret['serverip'] = []
            try:
                servers = get_server_ips()
                ret['serverip'] = servers
                doginfo = get_doginfo_byip()
                if doginfo['dogip'] == '1010':
                    ret['code'] = 2
                    ret['result'] = doginfo['result']
                    self.send_json(ret)
                    return
                ret['doginfo'] = doginfo
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                ret['code'] = 1
                ret['result'] = None
            self.send_json(ret)
            return
        #elif mtype=="2":
        elif op == 'upfile':
            #上传认证文件
            result = {}
            try:
                upload_path='/opt/thunder/bin/mainktvserver/' 
                fileN= "license.bin"
                filepath=os.path.join(upload_path,fileN)
                if os.path.exists(upload_path):
                    pass
                else:
                    os.mkdir(upload_path)
                file_metas=self.request.files['file'] 
                meta=file_metas[0]
                with open(filepath,'wb') as up:   
                    up.write(meta['body'])
                    up.close()
                result['code']=0
                result['msg']='操作成功'
            except:
                result['code']=1
                result['msg']='操作失败'
                
            try:
                dog_all_inianddata()
                restartService('mainktv')
            except:
                pass
            set_dog_info_ip(getLocalIp("eth0"))
            
            self.send_json(result)
            return
        #elif mtype=="3":
        elif op == 'setpwd':
            #设置加密狗密码
            mdata=self.get_argument('mdata')
            jsondata=json.loads(mdata)
           
            ret = {}
            upload_path='/opt/thunder/bin/mainktvserver/'
            if  jsondata['sercrt']=='':
                ret['code']=1
            else:
                try:
#                     upload_path='config/' 
                    fileN= "licensepasswd"
                    filepath=os.path.join(upload_path,fileN)
                    f=open(filepath,'w')
                    f.write(jsondata['sercrt'])
                    f.close()
                    dog_all_inianddata()
                    restartService('mainktv')
                    ret['code']=0
                    ret['msg']='操作成功'
                except:
                    ret['code']=1
                    ret['msg']='权限异常'
            self.send_json(ret)
            return
        #elif mtype=="4":
        elif op == 'delpwd':
            #删除密码
            ret = {}
            upload_path='/opt/thunder/bin/mainktvserver/'
            try:
                print 1111
#                 upload_path='conf/'
                fileN= "licensepasswd"
                filename=os.path.join(upload_path,fileN)
                print filename
                if os.path.exists(filename):
                    os.remove(filename)
                dog_all_inianddata()
                restartService('mainktv')
                ret['code']=0
                ret['msg']='操作成功'
            except:
                ret['code']=1
                ret['msg']='权限异常'
            self.send_json(ret)
            return
