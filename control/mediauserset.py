#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_mediauserset():
    ret = None
    res = _mysql.autoplay.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def add_new_mediauserset( MediaUserSet_Id,MediaUserSet_MediaId, MediaUserSet_Shunxu):

    params = {}
    params['MediaUserSet_Id'] = MediaUserSet_Id
    params['MediaUserSet_MediaId'] = MediaUserSet_MediaId
    params['MediaUserSet_Shunxu'] = MediaUserSet_Shunxu
    MediaUserSet_Id = _mysql.mediauserset.add(params)
    return MediaUserSet_Id

def exchange( id1, id2):
    no = _mysql.mediauserset.exchange( id1, id2)
    return no

def delete_mediauserset_by_id(id):
    bol = _mysql.mediauserset.delete(id)
    return bol

def get_maxId():
    return _mysql.mediauserset.get_maxId()
