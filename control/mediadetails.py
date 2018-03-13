#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_mediadetails(page, psize, text):
    ret = None
    res = _mysql.mediadetails.get_by_all(page,psize,text)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret
def get_by_count(text,type):
    count=_mysql.mediadetails.get_by_count(text,type)
    ret = {}
    ret['total'] = count
    return ret
    
