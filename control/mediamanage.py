#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_mediamanage(page, psize):
    ret = None
    res = _mysql.mediamanage.get_by_all(page,psize)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret
def get_by_count():
    count=_mysql.mediamanage.get_by_count()
    ret = {}
    ret['total'] = count
    return ret
    
def add_new_mediamanage():
    mediamanage_id = _mysql.mediamanage.add()
    return mediamanage_id
