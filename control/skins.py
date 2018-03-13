#!/usr/bin/env python
# -*- coding: utf-8 -*-

from orm import orm as _mysql
import glob

def get_all_skins():
    res = _mysql.skins.get_all()
    if isinstance(res, list) and len(res) > 0:
        return dict(matches=res, total=len(res))
    return None

def get_skin(skinid):
    res = _mysql.skins.get_by_id()
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    return None


def delete_skin(skinid):
    return _mysql.skins.delete(skinid)

def add_skin(info):
    '''
    更新皮肤信息
    '''
    return _mysql.skins.add(info)

def get_local_skin_packages():
    skins=[]
    str_val='/opt/thunder/www/Skin/'
    for filename in glob.glob(str_val + "*.img"):
        name = filename.replace(str_val, "")
        mname = name.replace(".img","")
        skins.append(mname)
    return skins
    
 

