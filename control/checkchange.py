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
import chardet

from control.postthunder import postHttp
from control.readthunder import read_all_info
from control.readthunder import set_all_thunder_data
from control.modbc import read_thunder_changecode
from control.modbc import set_thunder_changecode
from control.getlocalip import getLocalIp
from fileservers import sp_findthunder_ini
from fileservers import sp_updatathunder_init
from systemsetting import read_all_setting
from systemsetting import set_erp_conf
def check_change_version_code():
    #第一步去主服务器上获取,并携带本地的code
    allinfo={}
    #获取主服务器地址
    tminfo=read_all_info()
    mainservser=tminfo['mainserver']
    ip=mainservser['DataBaseServerIp']
    if ip=="127.0.0.1":
        return 2
    #获取本机的ip地址
    if ip==getLocalIp("eth0"):
        return 3
    #获取本地的code
    changecode=read_thunder_changecode()
    
    allinfo['changecode']=changecode
    recodata=postHttp(ip,allinfo,"3")
    dictdata=json.loads(recodata)
    if dictdata['code']==0:
        ttype=(dictdata["result"])
        if ttype['type']==0:
            thunderinfo=ttype[thunder]
            #设置本地的文件
            set_all_thunder_data(thunderinfo)
            #并且设置本地的文件的code
            set_thunder_changecode(ttype["versioncode"])
            return 0
        else:
            return 1
    return 1

def get_thunder_ini_db():
    #获取主服务器地址
    tminfo=read_all_info()
    mainservser=tminfo['mainserver']
    ip=mainservser['DataBaseServerIp']
    if ip=="127.0.0.1":
        return 2
    #获取本机的ip地址
    if ip==getLocalIp("eth0"):
        return 3
    content=sp_findthunder_ini()
    if content=='':
        return 1
    else:
        result=writer_thunder_ini(content)
        #去更改文件
        writer_other_setting()
        if result==0:
            return 0
        else:
            return 3
        
def writer_other_setting():
    #写入本机ip
    thunderdata=read_all_setting()
    mainserver=thunderdata['mainserver']
    mdata={}
    mdata['DataBaseServerIp']=mainserver['DataBaseServerIp']
    mdata['UserName']=mainserver['UserName']
    mdata['Password']=mainserver['Password']
    localIP =getLocalIp("eth0")
    mdata['FileServerIP']=localIP
    set_main_server_first(mdata,"utf8")
    #写主服务器的ip地址
    #写conf
    mainserver=thunderdata['erpserver']
    set_erp_conf(mainserver['DataBaseServerIp'])
    
       
    
def writer_thunder_ini(content):
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "systemparh")
    try:
        f = codecs.open(str_val, "w", "utf-8")
#         txt = unicode(content, "utf-8")
        f.write(content)
        f.close()
        return 0
    except:
        return 1
    

    
def read_thunder_ini_to_db():
    #//写到本地文件、
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "systemparh")
    try:
        f=codecs.open(str_val,'r',encoding='utf8')
        content=f.read()
        sp_updatathunder_init(content)
        return 0
    except:
        return 1
    
    
    
if __name__=='__main__':
    get_thunder_ini_db()
        
    

    
 
        
        #写入数据
        
        
    
    
    
    
    
    
            
