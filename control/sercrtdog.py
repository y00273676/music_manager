#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:25:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import os
import json
from ctypes import *
from control.servers import get_server_ips
from control.postthunder import postHttp
from control.getlocalip import getLocalIp
from lib.iniconfig import IniConfig
from control.modbc import *
import chardet
import codecs
def get_dogname():
    class ss(Structure):
        _fields_=[
                ("name", c_byte*32),
                ]
    filename="/opt/thunder/lib/libGetDogInfo.so"
    lib = cdll.LoadLibrary(filename)
    t = ss()
    dog= lib.GetDogName(pointer(t))

    tt = create_string_buffer(33)

    memmove(tt, byref(t), 32)
    temp = tt.value.__str__().decode('GBK').encode('utf8')
    return temp.strip()

def get_dog_serverip():
    class ss(Structure):
        _fields_=[
                ("name", c_byte*32),
                ]
    filename="/opt/thunder/lib/libGetDogInfo.so"
    lib = cdll.LoadLibrary(filename)
    t = ss()
    dog= lib.GetDogServerIP(pointer(t))

    tt = create_string_buffer(33)

    memmove(tt, byref(t), 32)
    temp = tt.value.__str__().decode('GBK').encode('utf8')
    mdog={}
    mdog['result']=dog
    mdog['value']=temp.strip()
    return mdog

def get_dog_maxuser():
    class ss(Structure):
        _fields_=[
                ("name", c_byte*32),
                ]
    filename="/opt/thunder/lib/libGetDogInfo.so"
    lib = cdll.LoadLibrary(filename)
    t = ss()
    dog= lib.GetMaxUser(pointer(t))

    tt = create_string_buffer(33)

    memmove(tt, byref(t), 32)
    temp = tt.value.__str__().decode('GBK').encode('utf8')
    return temp.strip()

def get_dog_userinfo():
    class ss(Structure):
        _fields_=[
                ("name", c_byte*32),
                ]
    filename="/opt/thunder/lib/libGetDogInfo.so"
    lib = cdll.LoadLibrary(filename)
    t = ss()
    dog= lib.GetUserInfo(pointer(t))

    tt = create_string_buffer(33)

    memmove(tt, byref(t), 32)
    temp = tt.value.__str__().decode('GBK').encode('utf8')
    return temp.strip()

def get_doginfo_byip():
    mdog = get_dog_serverip()
    if mdog['result'] != 0:
        iniip = read_dog_ip()
        if iniip!='':
            return get_doginfo_by_ini(iniip)
        else:
            mdata={}
            mdata['dogip']='1010'
            mdata['result']=mdog['result']
            return mdata
        
    ip = mdog['value']
    if ip in get_server_ips():
        try:
            print("dogserver ip is : %s" % ip)
            #判断是不是本机
            if ip == getLocalIp("eth0"):
                return get_doginfo_by_local()
            else:
                mjson={}
                mjson['doginfo'] = "get"
                #读取文件
                doginfo = postHttp(ip, mjson, "5")
                jsondata = json.loads(doginfo)
                return jsondata['doginfo']
        except:
            mdata = {}
            mdata['name'] = get_dogname()
            mdata['dogip'] = get_dog_serverip()['value']
            mdata['maxuser'] = get_dog_maxuser()
            mdata['remaintime'] = ""
            return mdata
        
    else:
        mdata = {}
        mdata['name'] = get_dogname()
        mdata['dogip'] = get_dog_serverip()['value']
        mdata['maxuser'] = get_dog_maxuser()
        mdata['remaintime'] = ""
        return mdata
    
def get_doginfo_by_ini(ip):
    if ip in get_server_ips():
        try:
            print ip
            #判断是不是本机
            if ip==getLocalIp("eth0"):
                return get_doginfo_by_local()
            else:
                mjson={}
                mjson['doginfo']="get"
                #读取文件
                doginfo=postHttp(ip,mjson,"5")
                jsondata=json.loads(doginfo)
                return jsondata['doginfo']
        except:
            mdata={}
            mdata['dogip']='1010'
            mdata['result']="请稍后再试"
            return mdata
    else:
        mdata={}
        mdata['dogip']='1010'
        mdata['result']="请稍后再试"
        return mdata
    
    
    
def get_doginfo_by_local():
    read_path='/opt/thunder/bin/mainktvserver/' 
    filename=os.path.join(read_path, 'licenseinfo')
    
    cf = IniConfig()
    
    f = open(filename,"r")
    data = f.read()
    cf.readfp(codecs.open(filename,'r','gbk'))
    
    doginfo = cf.items("DOGINFO")
    print ('^' * 17)
    print ("%s" % doginfo)

    mdata = {}
    for colum in doginfo:
        mdata[colum[0]] = colum[1]
    mdata['dogip']=getLocalIp("eth0")
    #set_dog_info(getLocalIp("eth0"),mdata['describe'])
    return mdata

def delete_beiyong_dog():
    pass





