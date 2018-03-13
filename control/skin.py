#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-25 11:27:33
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql


def get_all_skin_info():
    res = _mysql.skin.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def get_part_skin_info(skin_room_serialno):
    res = _mysql.skin.get_part_all(skin_room_serialno)
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def add_new_skin(roomid,skin_room_serialno, skin_theme_id, skin_name):
    params = {}
    params['skin_id'] = roomid
    params['skin_room_id'] = roomid
    params['skin_room_serialno'] = skin_room_serialno
    params['skin_theme_id'] = skin_theme_id
    params['skin_theme_name'] =skin_name
    print params
    skin_id = _mysql.skin.add(params)
    if skin_id and skin_id > 0:
        return True
    else:
        return False

def updata_new_skin(jsondata):
    params = {}
    params['skin_room_serialno'] =  int(jsondata['Room_SerialNo'])
    params['skin_theme_id'] =  int(jsondata['skin_theme_id'])
    params['skin_theme_name'] =  jsondata['skin_name']
    ret=_mysql.skin.updata(int(jsondata['Room_Old_SerialNo']),params)
    return ret

def delete_skin(room_no):
    ret=_mysql.skin.delete(room_no)
    return ret


