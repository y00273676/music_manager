#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lib import http
from orm import orm as _mysql

def get_all():
    ret = None
    res = _mysql.fileservers.get_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
    return ret

def get_all_fileservers(isMain):
    ret = None
    res = _mysql.fileservers.get_by_all(isMain)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
    return ret