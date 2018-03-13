#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:25:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql
import ConfigParser
from lib.iniconfig import IniConfig
import codecs
import json

import chardet
from control.systemsetting import read_all_setting
from control.systemsetting import set_main_server
from control.systemsetting import set_erpserver
from control.systemsetting import set_misc
from control.systemsetting import set_erp
from control.systemsetting import set_ktv
from control.systemsetting import update_systemset
from control.postthunder import postHttp
from control.modbc import set_main_ip_odbc


def read_all_info():
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "systemparh")
    _strcode="gbk"
    allinfo=read_all_setting(str_val,_strcode)
    return allinfo
#     ip="10.0.3.111"
#     state=postHttp(ip,allinfo,"2")
    
def get_main_thunder_info(localip):
    tminfo=read_all_info()
    mainservser=tminfo['mainserver']
    ip=mainservser['DataBaseServerIp']
    #需要知道主服务器的ip
#     ip="10.0.3.111"
    if localip==ip:
        return 1
    else:
        try:
            mallinfo=postHttp(ip,tminfo,"2")
            print "xxxxxxxx",mallinfo
            #获取到所有的信息然后填写到ini文件
            mreturn=json.loads(mallinfo)
            #看看是否是有变化
            mjsondata=mreturn['result']
            set_all_thunder_data(mjsondata)
            return 0
        except:
            return 2
        
def set_other_ip_thunder(localip):
    tminfo=read_all_info()
    mainservser=tminfo['mainserver']
    ip=mainservser['DataBaseServerIp']
    #需要知道主服务器的ip
#     ip="10.0.3.111"
    if localip==ip:
        return 1
    else:
        try:
            print 'ipxxxx',localip
            mallinfo=postHttp(localip,tminfo,"7")
            #获取到所有的信息然后填写到ini文件
            mreturn=json.loads(mallinfo)
            #看看是否是有变化
            mjsondata=mreturn['result']
            
            return mjsondata
        except:
            return 2
       

def set_all_thunder_data(mjsondata):
    _strcode="utf8"
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "systemparh")
#     str_val = 'orm/thunder.ini'
    misc=mjsondata['misc']
    mainserver=mjsondata['mainserver']
    erpserver=mjsondata['erpserver']
    erp=mjsondata['erp']
    ktv=mjsondata['ktv']
    

    set_main_server(str_val,mainserver,_strcode)
    set_erpserver(str_val,erpserver,_strcode)
    set_misc(str_val,misc,_strcode)
    set_erp(str_val,erp,_strcode)
    set_ktv(str_val,ktv,_strcode)
    
    
    set_main_ip_odbc(mainserver)
    
    return 0


    
