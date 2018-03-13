#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-18 15:22:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
import ConfigParser
from lib.iniconfig import IniConfig
import os
import os.path
import chardet
import codecs

from control.systemsetting import set_main_server
from control.systemsetting import set_erpserver
from control.servergroups import find_file_servers
from control.getlocalip import getLocalIp
from control.serverutils import action_other_command_docker
from control.fileservers import *
from control.readthunder import set_other_ip_thunder
from control.get_pic_video import *
from control.serverutils import actionCommand
import shutil


def delete_file_ini(filename):
    cf = IniConfig()
    cf.read('path.ini')

    #获取路径的基本地址
    str_val = cf.get("sec_a", "boxpath")
    print str_val
    mname=str_val+filename+".ini"
    print mname

    if os.path.exists(mname):
        os.remove(mname)
        if os.path.exists(mname):
            return False

    return True

def find_ip_ishave(filename):
    cf=IniConfig();
    cf.read(filename)
    ip=cf.get("STB","IP")
    if ip=="":
        return 0
    return 1

def find_stb_ishave(filename):
    cf=IniConfig();
    cf.read(filename)
    ip=cf.get("STB","STBType")
    return ip

def find_stb_name(filename):
    cf=IniConfig();
    cf.read(filename)
    ip=cf.get("STB","IP")
    return ip

def find_stbip_name(filename):
    cf=IniConfig();
    cf.read(filename)
    ip=cf.get("STB","IP")
    if ip:
        return ip
    else:
        return None

def find_stb_aa_name(filename):
    cf=IniConfig();
    cf.read(filename)
    ip=cf.get("STB","Name")
    return ip

def find_stb_info_defult(filename):
    cf=IniConfig()
    cf.read(filename)
    sections = cf.sections()
    #查看是否有sections
    IP=cf.get("STB","IP")
    STBType=cf.get("STB","STBType")
    Name=cf.get("STB","Name")
    isuse=0
    if IP:
        isuse= 1
    if len(sections)==1:
        cf.add_section("PROSET")
        cf.write(codecs.open(filename, "w", "utf8"))
    
    return (isuse,IP,STBType,Name)
    




def update_init_ini(filename):
    cf = IniConfig()
    f = open(filename,"r")
    data = f.read()
    cf.readfp(codecs.open(filename, "r", chardet.detect(data)['encoding']))
#     cf.read(filename)
    #检查是否含有下面一个标签
    sections = cf.sections()
    if len(sections)==1:
        cf.add_section("PROSET")
        cf.write(codecs.open(filename, "w", "utf8"))
#         cf.write(open(filename, "w"))


def remove_set_ini(filename,section):
    cf = IniConfig()
    cf.read(filename)
    cf.remove_section(section)
    cf.add_section(section)
    cf.write(open(filename, "w"))

def get_all_set_list_ini(filename):
    datajson={}
    cf = IniConfig()
    f = open(filename,"r")
    data = f.read()
    print chardet.detect(data)
    cf.readfp(codecs.open(filename, "r", chardet.detect(data)['encoding']))
    sections = cf.sections()
    stb=cf.items("STB")
    proset=cf.items("PROSET")
    _mjson={}
    _mprjson={}
    for colum in stb:
        _mjson[colum[0]]=colum[1]
    for columone in proset:
        _mprjson[columone[0]]=columone[1]


    datajson['box']=_mjson
    datajson['option']=_mprjson
    print datajson
    return datajson

def get_all_config_ini(filename):
    item=[]

    cf = open(filename,"r")
    data = cf.read()
    print chardet.detect(data)
    f.readfp(codecs.open(filename, "r", chardet.detect(data)['encoding']))
    while True:
        line = f.readline()
        print "11111111"

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
def set_stb_syscn():
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "boxpath")
    if find_file_servers()==None:
        return
    starr={}
    for server in find_file_servers():
        ip=server['FileServer_IpAddress']
        print "ip",ip
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            actionCommand(str_val,ip)
        except:
            continue

def set_stb_syscn_by_file(filename):
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "boxpath")
    if find_file_servers()==None:
        return
    starr={}
    for server in find_file_servers():
        ip=server['FileServer_IpAddress']
        print "ip",ip
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            path=os.path.join(str_val,filename)
            actionCommand(path,ip)
        except:
            continue


def is_a_nect(ip):
    iparr=ip.split('.')
    locaarr=(getLocalIp("eth0")).split('.')
    if iparr[0]==locaarr[0] and iparr[1]==locaarr[1] and iparr[2]==locaarr[2]:
        return 0
    else:
        return 1

def tongbu_file(ip):
    str_licenseinfo='/opt/thunder/bin/mainktvserver/'
    try:
        cf = ConfigParser.ConfigParser()
        cf.read('path.ini')
        str_val = cf.get("sec_a", "boxpath")
        if ip=='127.0.0.1':
            return 0
        if ip==getLocalIp("eth0"): 
            return 0
        #同步license
        action_other_command_docker(str_licenseinfo,ip)
        
        if action_other_command_docker(str_val,ip)==1:
           return 1
        return 0
    except:
        return 1
    

def tong_all_inianddata():
    mymsg=[]
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "boxpath")
    if find_file_servers()==None:
        return
    starr={}
    for server in find_file_servers():
        ip=server['FileServer_IpAddress']
        print "ip",ip
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            actionCommand(str_val,ip)
            tongbu_file(ip)
            set_other_ip_thunder(ip)
            syn_all_file(ip)
            mymsg.append(str(ip)+"同步成功|");
        except:
            mymsg.append(str(ip)+"同步失败|");
            continue
    return mymsg
    
   
    
    
def dog_all_inianddata():
    mymsg=[]
    str_licenseinfo='/opt/thunder/bin/mainktvserver/'
    if find_file_servers()==None:
        return
    starr={}
    for server in find_file_servers():
        ip=server['FileServer_IpAddress']
        print "ip",ip
        if ip=='127.0.0.1':
            continue
        if ip==getLocalIp("eth0"):
            continue
        try:
            action_other_command_docker(str_licenseinfo,ip)
            mymsg.append(str(ip)+"同步成功|")
        except Exception,e:
            print 'exception',e
            mymsg.append(str(ip)+"同步失败|")
            continue
    return mymsg

def copyfile(re_path,tag_path):
    #需要复制一下
    if os.path.exists(tag_path):
        os.remove(tag_path)
    shutil.copy(re_path,tag_path)

    
    
   
    
    
    


