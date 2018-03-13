#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:25:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import json
from ctypes import *
from lib.iniconfig import IniConfig
import chardet
import codecs
import glob
import base64

#from control.servergroups import 
from control.servers import get_server_ips
from control.getlocalip import getLocalIp
from control.serverutils import action_config_command
from control.serverutils import action_delete_command
from control.serverutils import action_other_command_docker
from control.postthunder import postHttp

def get_all_file(path,format):
    mpicarr=[]
    print "xxxxx",path+"*."+format
    for filename in glob.glob(path+"*."+format):
#         filename.split('/')[-1]
        mpicarr.append(filename.split('/')[-1])
    
    return mpicarr

def get_base64_pic(path):
    f=open(path,'rb') #二进制方式打开图文件
    ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
    f.close()
    return ls_f

def read_all_other_setting(filename):
    item=[]
    cf = open(filename,"r")
    data = cf.read()
    print chardet.detect(data)
    
    f = codecs.open(filename, "r",'gbk')
#     f.readfp(codecs.open(filename, "r", chardet.detect(data)['encoding']))
    while True:
        line = f.readline()

        if line:
            pass    # do something here
            line=line.strip()
            if(line=='[ITEM]'):
                datajson={}
                item.append(datajson)
            else:
                key_val=line.split("=")
                if(len(key_val)>1):
                    datajson[key_val[0]]=key_val[1]
                else:
                    datajson["select"]=key_val[0]
        else:
            break
    f.close()
    return item

def set_config_syscn(file):
    for server in get_server_ips():
        ip=server
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            action_config_command(file,ip)
        except:
          pass
      
def set_config_delete(file):
    for server in get_server_ips():
        ip=server
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            mydata={}
            mydata['filename']=file
            postHttp(ip,mydata,"6")
        except:
          pass

def syn_other_file():
    msg=[]
    for server in get_server_ips():
        ip=server
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            #同步到其他服务器
            result=action_other_command_docker('/opt/thunder/www/',ip)
            action_other_command_docker('/data/OpenRoomToPlay/',ip)
            action_other_command_docker('/data/AD/',ip)
            if result==1:
                msg.append(ip+"同步失败，请检查服务器是否配置或者网络是否畅通")
            else:
                msg.append(ip+"同步成功")
        except:
            msg.append(ip+"同步失败")
          
    return msg



def syn_all_file(ip):
    msg=[]
    print "ip",ip
    if ip=='127.0.0.1':
        return msg
    if ip==getLocalIp("eth0"):
        return msg
    try:
        #同步到其他服务器
        result=action_other_command_docker('/opt/thunder/www/',ip)
        action_other_command_docker('/data/OpenRoomToPlay/',ip)
        action_other_command_docker('/data/AD/',ip)
        if result==1:
            msg.append(ip+"同步失败，请检查服务器是否配置或者网络是否畅通")
        else:
            msg.append(ip+"同步成功")
    except:
        msg.append(ip+"同步失败")
          
    return msg
