#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-19 16:04:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql
import ConfigParser
from lib.iniconfig import IniConfig


def get_all_set_info():
    res = _mysql.menpaiad.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def updata_menpai(jsondata):
    
    return _mysql.menpaiad.updata(jsondata['MenPaiAdSetting_Id'],jsondata)
 

def add_menpai(jsondata):
    res = _mysql.menpaiad.add(jsondata)
    if res!= None:
        return "0"
    else:
        return "1" 
    
def delete_menpai(adid):
    res = _mysql.menpaiad.delete(adid)
    return res

def delete_menpaiall():
    
    res = _mysql.menpaiad.deleteall()
    return res

def delete_menpai_roomid(roomid):
    res = _mysql.menpaiad.deletebyroom(roomid)
    return res

def get_all_mediadetails(page, psize, text ,type):
    ret = {}
    ret['matches']=[]
    ret['total']=0
    res = _mysql.mediadetails.get_by_all(page,psize,text,type)
    if isinstance(res, list) and len(res) > 0:
        
        ret['matches'] = res
        ret['total'] = len(res)
    return ret






