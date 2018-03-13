#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-21 15:56:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import codecs
import chardet
import hashlib
import ConfigParser

from lib import http
from orm import orm as _mysql
from lib.iniconfig import IniConfig
from control.fileservers import sp_add_theme
from control.fileservers import sp_modify_theme
from control.fileservers import sp_delete_theme
from control.getlocalip import getLocalIp


def up_cloud_setting(cloudset):
    update_systemset("中转服务器IP",cloudset['centerinip'])
    update_systemset("中转服务器外网IP",cloudset['centeroutip'])
    update_systemset("本地VPN域名",cloudset['localname'])
    update_systemset("SSID",cloudset['ssid'])
    update_systemset("SSID_Pwd",cloudset['ssidpw'])

def up_cloudmusic_setting(cloudmusic):
    update_systemset("CloudMusic_uname", cloudmusic['loginname'])
    update_systemset("CloudMusic_realdown", cloudmusic['realdown'])
    if 'loginpassword' in cloudmusic.keys() and cloudmusic['loginpassword']:
        #don't change the password if submit a empty string
        update_systemset("CloudMusic_passwd", hashlib.md5(cloudmusic['loginpassword']).hexdigest().lower())

def update_systemset(settingname,settingvalue):
    params = {}
    params['SettingInfo_Name'] = settingname
    params['SettingInfo_Value'] = settingvalue

    return _mysql.systemsettinginfo.update(settingname, params)

def find_data_setting():
    res = _mysql.systemsettinginfo.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def read_all_setting(filename,strcode):
    datajson={}
    cf = IniConfig()
    
    f = open(filename,"r")
    data = f.read()
    print chardet.detect(data)
    # cf.read(filename)
    cf.readfp(codecs.open(filename))
    sections = cf.sections()
    mainserver=cf.items("MainServer")
    erpserver=cf.items("ErpServer")
    misc=cf.items("Misc")
    ktv=cf.items("KTV")
    erp=cf.items("ERP")

    _mjson={}
    _mprjson={}
    _mmijson={}
    _mktvjson={}
    _merpjson={}

    for colum in mainserver:
        _mjson[colum[0]]=colum[1]
    for columone in erpserver:
        _mprjson[columone[0]]=columone[1]

    for columtwo in misc:
        _mmijson[columtwo[0]]=columtwo[1]
    for columtwo in ktv:
        _mktvjson[columtwo[0]]=columtwo[1]
    for columtwo in erp:
        _merpjson[columtwo[0]]=columtwo[1]


    datajson['mainserver']=_mjson
    datajson['erpserver']=_mprjson
    datajson['misc']=_mmijson
    datajson['erp']=_merpjson
    datajson['ktv']=_mktvjson
    print 'xxxx', type(datajson['mainserver']['DataBaseServerIp'])
    print datajson
    return datajson

def set_main_server(filename,jsondata,strcode):
    item=jsondata;
    cf = IniConfig()

    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("MainServer", "DataBaseServerName", item['DataBaseServerName'])
    cf.set("MainServer", "DataBaseServerIp", item['DataBaseServerIp'])
    cf.set("MainServer", "UserName", item['UserName'])
    cf.set("MainServer", "Password", item['Password'])
    localIP =getLocalIp("eth0")
    cf.set("MainServer", "FileServerIP", localIP)
    cf.write(codecs.open(filename, "w", strcode))
    
def set_main_server_ip(filename,ip,strcode):
    cf = IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("MainServer", "DataBaseServerIp",ip)
    cf.write(codecs.open(filename, "w", strcode))
    
#     set_main_server_ip    


def set_erpserver(filename,jsondata,strcode):
    item=jsondata;
    cf = IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("ErpServer", "DataBaseServerName", item['DataBaseServerName'])
    cf.set("ErpServer", "DataBaseServerIp", item['DataBaseServerIp'])
    cf.set("ErpServer", "UserName", item['UserName'])
    cf.set("ErpServer", "Password", item['Password'])
    cf.write(codecs.open(filename, "w", strcode))
    set_erp_conf(item['DataBaseServerIp'])
    
def set_erp_conf(ip):
    try:
        cf = IniConfig()
        cf.readfp(codecs.open("/usr/local/freetds/etc/freetds.conf", "r", "utf8"))
    #     cf.readfp(codecs.open("orm/freetds.conf", "r", "utf8"))
        cf.set("ThunderERP", "host", ip)
        cf.write(codecs.open("/usr/local/freetds/etc/freetds.conf", "w", "utf8"))
        return 0
    except:
        return 1
#     cf.write(codecs.open("orm/freetds.conf", "w", "utf8"))


def set_erp(filename,jsondata,strcode):
    item=jsondata;
    cf = IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("ERP", "DataBaseName", item['DataBaseName'])
    cf.write(codecs.open(filename, "w", strcode))

def set_ktv(filename,jsondata,strcode):
    item=jsondata;
    cf = IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("KTV", "Version", item['Version'])
#     cf.set("KTV", "DataBaseName", item['DataBaseName'])
    cf.write(codecs.open(filename, "w", strcode))

def set_misc(filename,jsondata,strcode):
    item=jsondata;
    cf = IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))

    cf.set("Misc", "Salutatory", item['Salutatory'])
    cf.set("Misc", "StayTime", item['StayTime'])

#     cf.set("Misc", "LoginPhoto", item['LoginPhoto'])
    cf.write(codecs.open(filename, "w", strcode))


def set_video_server(filename,jsondata,strcode):
    cf = IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("VideoServer", "AssignMethod", item['AssignMethod'])
    cf.set("VideoServer", "LoadMethod", item['LoadMethod'])
    cf.set("VideoServer", "Hosttask", item['Hosttask'])
    cf.set("VideoServer", "RandPlayType", item['RandPlayType'])
    cf.write(codecs.open(filename, "w", strcode))

def set_host_setting():
    pass

def set_fws_setting():
    pass




def set_hcset():
    pass

def set_pay():
    pass

def sp_add_theme_con(kwargs):
    jsondata={}
    jsondata['theme_name']=kwargs['theme_name']
    jsondata['theme_charset']=""
    jsondata['font_facename']=""
    jsondata['font_weight']='900'
    jsondata['pic_local_path']=("/opt/thunder/www/Skin/"+kwargs['theme_name']+".img")
    jsondata['pic_http_path']='Skin'
    jsondata['font_local_name']=''
    jsondata['font_http_name']=''
    jsondata['font_color1']="16777215"
    
    if kwargs['theme_name']=='Mpj' or kwargs['theme_name']=='MpjTurn':
        jsondata['font_color2']="6612710"
        jsondata['font_color3']="51455"
        jsondata['font_color4']="16777215"
        jsondata['font_color5']="14474460"
        jsondata['font_color6']="15865464"
    else:
        jsondata['font_color2']="13634756"
        jsondata['font_color3']="359139"
        jsondata['font_color4']="0"
        jsondata['font_color5']="16711830"
        jsondata['font_color6']="16777215"
    
    
    jsondata['font_color7']="16645866"
    jsondata['font_color8']="16777215"

    jsondata['theme_reserved1']=""
    jsondata['theme_reserved2']=""
    jsondata['theme_reserved3']=""
    jsondata['theme_reserved4']="0"
    jsondata['theme_reserved5']="1"
    jsondata['theme_reserved6']="0"
    return sp_add_theme(jsondata)

def sp_modify_theme_con(kwargs):
    jsondata={}
    jsondata['theme_id']=kwargs['theme_id']
    jsondata['theme_name']=kwargs['theme_name']
    jsondata['theme_charset']=""
    jsondata['font_facename']=""
    jsondata['font_weight']=kwargs['font_weight']
    jsondata['pic_local_path']=kwargs['pic_local_path']
    jsondata['pic_http_path']=kwargs['pic_http_path']
    jsondata['font_local_name']=kwargs['font_local_name']
    jsondata['font_http_name']=kwargs['font_http_name']
    jsondata['font_color1']=""
    jsondata['font_color2']=""
    jsondata['font_color3']=""
    jsondata['font_color3']=""
    jsondata['font_color3']=""
    jsondata['font_color6']=""
    jsondata['font_color7']=""
    jsondata['font_color8']=""

    jsondata['theme_reserved1']=""
    jsondata['theme_reserved2']=""
    jsondata['theme_reserved3']=""
    jsondata['theme_reserved4']=""
    jsondata['theme_reserved5']=""
    jsondata['theme_reserved6']=""
    print kwargs
    return sp_modify_theme(kwargs)


def sp_delete_theme_con(kwargs):
    jsondata={}
    jsondata['theme_id']=kwargs['theme_id']
    jsondata['theme_name']=kwargs['theme_name']
    return sp_delete_theme(jsondata)

def is_allright_ip(ip):
    cmd='ping -c 2 -i 0.4 -w 0.2 -q %s'%ip
    try:
        backinfo=os.popen(cmd)
        print 'backinfo',backinfo
        return str(backinfo)
    except:
        return "1"
    




