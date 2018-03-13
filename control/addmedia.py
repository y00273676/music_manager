#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_addmedia():
    ret = None
    res = _mysql.addmedia.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def get_addmedia_by_pathAndName(path,name):
    res = _mysql.addmedia.get_by_pathAndName(path,name)
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    else:
        return None

    
def add_new_addmedia(AddMedia_Name,AddMedia_Path,AddMedia_Type,AddMedia_Size,AddMedia_SerialNo):
    params = {}
    params['AddMedia_Name'] = AddMedia_Name
    params['AddMedia_Path'] = AddMedia_Path
    params['AddMedia_Type'] = AddMedia_Type
    params['AddMedia_Size'] = AddMedia_Size
    params['AddMedia_SerialNo'] = AddMedia_SerialNo
    AddMedia_ID = _mysql.addmedia.add(params)
    return AddMedia_ID

def delete_addmedia_by_id(sid,sno):
    return _mysql.addmedia.delete(sid,sno)

def active_addmedia_by_id(sid):
    return _mysql.addmedia.active(sid)