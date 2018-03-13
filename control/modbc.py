#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-21 15:56:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import ConfigParser
from lib.iniconfig import IniConfig
import codecs
import chardet



def read_is_setting():
    mydata={}
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "ishasset")
    mydata['ishasset']=str_a
    return mydata

def read_thunder_changecode():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "thunderini")
    return str_a


def read_dog_ip():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "dogip")
    return str_a

def read_dog_describe():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "dogdescribe")
    return str_a

def set_dog_info(dogip,dogdescribe):
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "dogip", dogip)
    cf.set("initthunder", "dogdescribe", dogdescribe)
    cf.write(open("initstart.ini", "w"))
    
def set_dog_info_ip(dogip):
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "dogip", dogip)
    cf.write(open("initstart.ini", "w"))
    
def set_thunder_changecode(codevision):
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "thunderini", codevision)
    cf.write(open("initstart.ini", "w"))
    

def set_is_setting():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "ishasset", "1")
    cf.write(open("initstart.ini", "w"))  

    
def read_path_ini():
    mydata={}
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_a = cf.get("sec_a", "systemparh")
    mydata['systemparh']=str_a
    str_b = cf.get("sec_a", "odbcpath")
    mydata['odbcpath']=str_b
    str_c = cf.get("sec_a", "odbcinstpath")
    mydata['odbcinstpath']=str_c
    return mydata

def get_all_thunder_ini():
    
    f = open(read_path_ini()['systemparh'],"r")
    data = f.read()
    chardet.detect(data)
    return read_all_setting(read_path_ini()['systemparh'],'utf8')
   

def read_all_setting(filename,strcode):
    datajson={}
    cf = IniConfig()
    # cf.read(filename)
    cf.readfp(codecs.open(filename, "r", strcode))
    sections = cf.sections()
    mainserver=cf.items("MainServer")
    #erpserver=cf.items("ErpServer")
    misc=cf.items("Misc")
    #ktv=cf.items("KTV")
    #erp=cf.items("ERP")

    _mjson={}
    _mprjson={}
    _mmijson={}
    _mktvjson={}
    _merpjson={}

    for colum in mainserver:
        _mjson[colum[0]]=colum[1]
    #for columone in erpserver:
    #    _mprjson[columone[0]]=columone[1]

    for columtwo in misc:
        _mmijson[columtwo[0]]=columtwo[1]
    #for columtwo in ktv:
    #    _mktvjson[columtwo[0]]=columtwo[1]
    #for columtwo in erp:
    #    _merpjson[columtwo[0]]=columtwo[1]


    datajson['mainserver']=_mjson
    #datajson['erpserver']=_mprjson
    datajson['misc']=_mmijson
    #datajson['erp']=_merpjson
    #datajson['ktv']=_mktvjson
    
    return datajson



def set_main_server(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    f = open(read_path_ini()['systemparh'],"r")
    data = f.read()
    

    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("MainServer", "DataBaseServerName", item['DataBaseServerName'])
    cf.set("MainServer", "DataBaseServerIp", item['DataBaseServerIp'])
    cf.set("MainServer", "UserName", item['UserName'])
    cf.set("MainServer", "Password", item['Password'])
    
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))
    #
    set_odbc_ini(mypath['odbcpath'],jsondata,strcode)
    set_my_sql(mypath['odbcinstpath'],jsondata,strcode)
    
def set_main_ip_odbc(jsondata):
    mypath=read_path_ini()
    set_odbc_ini(mypath['odbcpath'],jsondata,'utf8')
    set_my_sql(mypath['odbcinstpath'],jsondata,'utf8')
    
    
def set_main_server_first(jsondata,strcode):
    
    try:
        item=jsondata;
        mypath=read_path_ini()
        cf = IniConfig()
    
        cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
        cf.set("MainServer", "DataBaseServerIp", item['DataBaseServerIp'])
        cf.set("MainServer", "UserName", item['UserName'])
        cf.set("MainServer", "Password", item['Password'])
        cf.set("MainServer", "FileServerIP", item['FileServerIP'])
        #获取本机ip的地址
    #     cf.set("MainServer", "FileServerIP", item['FileServerIp'])
        cf.write(codecs.open(mypath['systemparh'], "w", strcode))
        set_odbc_ini(mypath['odbcpath'],jsondata,strcode)
        set_my_sql(mypath['odbcinstpath'],jsondata,strcode)
        return 0
    except:
        return 1
    

    

def set_modbc_erpserver(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("ErpServer", "DataBaseServerName", item['DataBaseServerName'])
    cf.set("ErpServer", "DataBaseServerIp", item['DataBaseServerIp'])
    cf.set("ErpServer", "UserName", item['UserName'])
    cf.set("ErpServer", "Password", item['Password'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))


def set_erp(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("ERP", "DataBaseName", item['DataBaseName'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))

def set_ktv(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("KTV", "Version", item['Version'])
    cf.set("KTV", "DataBaseName", item['DataBaseName'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))

def set_misc(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))

    cf.set("Misc", "Salutatory", item['Salutatory'])
    cf.set("Misc", "StayTime", item['StayTime'])

    cf.set("Misc", "LoginPhoto", item['LoginPhoto'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))


def set_video_server(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("VideoServer", "AssignMethod", item['AssignMethod'])
    cf.set("VideoServer", "LoadMethod", item['LoadMethod'])
    cf.set("VideoServer", "Hosttask", item['Hosttask'])
    cf.set("VideoServer", "RandPlayType", item['RandPlayType'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))
    
def set_odbc_ini(filename,jsondata,strcode):
    item=jsondata;
    cf=IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("krok","SERVER",item['DataBaseServerIp'])
    cf.set("krok","USER",item['UserName'])
    cf.set("krok","PASSWORD",item['Password'])
    
    cf.set("mysql","SERVER",item['DataBaseServerIp'])
    cf.set("mysql","USER",item['UserName'])
    cf.write(codecs.open(filename, "w", strcode))
    
def set_my_sql(filename,jsondata,strcode):
    item=jsondata;
    cf=IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("MYSQL","SERVER",item['DataBaseServerIp'])
    cf.set("MYSQL","USER",item['UserName'])
    cf.write(codecs.open(filename, "w", strcode))
    
def comp_by_ip(x,y):
    aa=int(x['Room_IpAddress'].split(".")[-1])
    bb=int(y['Room_IpAddress'].split(".")[-1])
    if aa<bb:
        return -1
    elif aa==bb:
        return 0
    else :
        return 1
    
    
    
    
 
    
    
    
    
    
    
