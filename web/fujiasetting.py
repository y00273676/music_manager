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
import socket
import os


from tornado import gen
from lib.http import request_json
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.get_pic_video import *
from control.fileservers import *
#from control.servergroups import *
from control.servers import get_server_ips
logger=logging.getLogger(__name__)

class FujiaHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('fujiasetting.html')
        
    @gen.coroutine
    def options(self):
        self.send_json('')


    @gen.coroutine
    def post(self):
        mtype=self.get_argument('type')
        mvalue=self.get_argument('value')
        #需要上传文件的代码
        if mtype=='1' or mtype=='2':
            result = {}
            if len(get_server_ips()) <= 0:
                result['code']=1
                result['msg']='没有添加视频服务器'
                self.send_json(result)
            fileN=self.get_argument('fileName')
            print 'xxx',fileN
            
            inipath="orm/allconfig.ini"
            myconfig={}
            for config in read_all_other_setting(inipath):
                if mvalue==config['key']:
                    myconfig=config
                    break
#             upload_path='config/' 
            upload_path=myconfig['path']
            print mvalue
            
            #添加到数据库
            filepath=os.path.join(upload_path,fileN)
            print "filepath",filepath
            if myconfig['needdb']=='1':
                tempdb={}
                tempdb['filename']=fileN
                tempdb['path']=filepath
                sp_favourable_add(tempdb)

            if os.path.exists(upload_path):
                pass
            else:
                os.mkdir(upload_path)
            print "aa","111111111"
            file_metas=self.request.files['file'] 
            meta=file_metas[0]
            with open(filepath,'wb') as up:   
                up.write(meta['body'])
            up.close()
            result['msg']='操作成功'
            result['code']=0
            try:
                set_config_syscn(filepath)
            except:
                result['code']=1
                result['msg']='同步出错'
            self.send_json(result)
        elif mtype=='3':
            result = {}
            if len(get_server_ips()) <= 0:
                result['code']=1
                result['msg']='没有添加视频服务器'
                self.send_json(result)
            fileN=self.get_argument('fileName')
            print 'xxx',fileN
            inipath="orm/allconfig.ini"
            myconfig={}
            for config in read_all_other_setting(inipath):
                if mvalue==config['key']:
                    myconfig=config
                    break
#             upload_path='config/' 
            upload_path=myconfig['path']
            print mvalue
            #添加到数据库
            filepath=os.path.join(upload_path,fileN)
            print "filepath",filepath
            if myconfig['needdb']=='1':
                tempdb={}
                tempdb['filename']=fileN
                tempdb['path']=filepath
                sp_favourable_add(tempdb)

            if os.path.exists(upload_path):
                pass
            else:
                os.mkdir(upload_path)
            start= try_to_int(self.get_argument('start', '0'))
            end= try_to_int(self.get_argument('end', '0'))
            size = 0
            if os.path.exists(filepath):
                if start==0:
                    os.remove(filepath)
            if size < end:
                file_metas=self.request.files['file'] 
                meta=file_metas[0]
                with open(filepath,'ab') as up:   
                    up.write(meta['body'])
                up.close()
            result['msg']='操作成功'
            result['code']=0
            #判断是否已经完成
            totalsize=self.get_argument('size')
            print totalsize
            if os.path.exists(filepath):
                filesize=os.path.getsize(filepath)
                if  int(totalsize)==filesize:
                    try:
                        print '同步',end,int(totalsize)
                        set_config_syscn(filepath)
                    except:
                        result['code']=1
                        result['msg']='同步出错'
            self.send_json(result)
        elif mtype=='4':
            path="orm/allconfig.ini"
            
            result = {}
            result['code']=0
            result['msg']='获取成功'
            result['data']=read_all_other_setting(path)
            
            self.send_json(result)
            
        elif mtype=='5':
           
            inipath="orm/allconfig.ini"
            myconfig={}
            for config in read_all_other_setting(inipath):
                if mvalue==config['key']:
                    myconfig=config
                    break
            result = {}
            
            filearr=[]
            picstrjson={}
            print myconfig['filename']
            if myconfig['filename']!='':
                for filename in (myconfig['filename']).split('|'):
                    if os.path.exists(myconfig['path']+filename):
                        filearr.append(filename)
            else:
                filearr=get_all_file(myconfig['path'],myconfig['format'])
            print filearr
            myconfig['ishave']=filearr
            myconfig['filestr']=picstrjson
            aa=[]
            aa.append(myconfig)
            result['code']=0
            result['msg']='获取成功'
            result['data']=aa
            result['ishaserver']="0"
            if len(get_server_ips()) <= 0:
                result['ishaserver']="1"
            self.send_json(result)
        elif mtype=='6':
            inipath="orm/allconfig.ini"
            myconfig={}
            for config in read_all_other_setting(inipath):
                if mvalue==config['key']:
                    myconfig=config
                    break
            result = {}
           
            if os.path.exists(myconfig['path']+myconfig['filename']):
                os.remove(myconfig['path']+myconfig['filename'])
                set_config_delete(myconfig['path']+myconfig['filename'])
           
            result['code']=0
            result['msg']='删除成功'
            self.send_json(result)
        elif mtype=='7':
            inipath="orm/allconfig.ini"
            myconfig={}
            for config in read_all_other_setting(inipath):
                if mvalue==config['key']:
                    myconfig=config
                    break
            result = {}
            picname=self.get_argument('picname')
            print myconfig
            if myconfig['needdb']=='1':
                try:
                    sp_favourable_delect(picname)
                except:
                    pass
                
           
            if os.path.exists(myconfig['path']+picname):
                os.remove(myconfig['path']+picname)
                set_config_delete(myconfig['path']+picname)
            result['code']=0
            result['msg']='删除成功'
            self.send_json(result)
            
        elif mtype=='8':
            result = {}
            result['code']=0
            result['msg']='获取成功'
            result['serverip']=get_server_ips()
            self.send_json(result)
        elif mtype=='9':
            result = {}
            result['code']=0
            mymsg=syn_other_file()
            if len(mymsg)==0:
                result['msg']='当前只有一台服务器'
            else:
                result['msg']=mymsg
            self.send_json(result)

            
                
        
            
            
            
        
        
        
