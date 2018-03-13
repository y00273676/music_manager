#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_mediafile(page, psize):
    ret = None
    res = _mysql.mediafile.get_by_all(page,psize)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret
def get_by_count():
    count=_mysql.mediafile.get_by_count()
    ret = {}
    ret['total'] = count
    return ret

def add_new_mediafile(media_no, media_file):
    return _mysql.mediafile.add(media_no,  media_file)
