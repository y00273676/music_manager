#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-03 13:51:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
import ConfigParser
from lib.iniconfig import IniConfig
import os
import os.path
from orm import orm as _mysql

def find_file_servers():
    res = _mysql.fileservers.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def find_all_servers_ip():
    mydataarr=[]
    temp=find_file_servers()
    if temp==None:
        temp=[]
    for content in temp:
        print content
        ip=content['FileServer_IpAddress'];
        mydataarr.append(ip)
    return mydataarr
    



def updata_file_servers(server_id,jsondata):
    try:
        params = {}
        params['FileServer_Name'] = jsondata['FileServer_Name']
        params['FileServer_IpAddress'] = jsondata['FileServer_IpAddress']
        params['FileServer_OS'] = jsondata['FileServer_OS']
        params['FileServer_IsValid'] = jsondata['FileServer_IsValid']
        params['FileServer_Group_ID'] = jsondata['FileServer_Group_ID']
        params['FileServer_IsMainGroup'] = jsondata['FileServer_IsMainGroup']
        return _mysql.fileservers.update(flag, params)
    except:
        return False

def add_file_servers(jsondata):
     try:
        params = {}
        params['FileServer_Name'] = jsondata['FileServer_Name']
        params['FileServer_IpAddress'] = jsondata['FileServer_IpAddress']
        params['FileServer_OS'] = jsondata['FileServer_OS']
        params['FileServer_IsValid'] = jsondata['FileServer_IsValid']
        params['FileServer_Group_ID'] = jsondata['FileServer_Group_ID']
        params['FileServer_IsMainGroup'] = jsondata['FileServer_IsMainGroup']
        return _mysql.fileservers.add(flag, params)
     except:
        return None

def delete_file_servers_id(server_id):
    try:
        return _mysql.fileservers.delete(server_id)
    except Exception, e:
        return False

def find_server_groups():
    res = _mysql.servergroups.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def updata_server_groups(server_id,jsondata):
        params = {}
        params['ServerGroup_Name'] = jsondata['ServerGroup_Name']
        return _mysql.servergroups.updata(server_id, params)

def find_id_info():
    res = _mysql.servergroups.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def add_defult_groups():
    if find_id_info()!=None:
        return
    else:
        mt={}
        mt['ServerGroup_Name']="Main"
        mt['ServerGroup_IsValid']="1"
        add_server_groups(mt)
        
        mt={}
        mt['ServerGroup_Name']="Slave"
        mt['ServerGroup_IsValid']="1"
        add_server_groups(mt)
        
        
        

def add_server_groups(jsondata):

        params = {}
        num=0
        if find_id_info()!=None:
            for mid in find_id_info():
                if num<mid['ServerGroup_ID']:
                    num=mid['ServerGroup_ID']

        params['ServerGroup_ID'] =num+1
        params['ServerGroup_Name'] = jsondata['ServerGroup_Name']
        params['ServerGroup_IsValid'] = jsondata['ServerGroup_IsValid']
        print params
        return _mysql.servergroups.add(params)


def delete_server_groups_id(server_id):
        return _mysql.servergroups.delete(server_id)




