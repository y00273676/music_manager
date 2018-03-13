#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_artists():
    res = _mysql.artists.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def get_all_artists_bypage(page, psize):
    ret = None
    total = _mysql.artists.get_all_count()
    if (page - 1) * psize > total:
        res = {}
    else:
        res = _mysql.artists.get_all_bypage(page, psize)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = total
    return ret


def get_artists_by_id(sid):
    res = _mysql.artists.get_by_id(sid)
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    else:
        return None

def update_artists(artsid, name, title, desc, artslist, bgimage):
    params = {}
    params['artsname'] = name
    params['artstitle'] = title
    params['artsdesc'] = desc
    params['artslist'] = ','.join(artslist)
    params['bgimage'] = bgimage
 
    return _mysql.artists.update(artsid, params)

def add_new_artists(name, title, desc, artslist, bgimage):
    params = {}
    params['artsname'] = name
    params['artstitle'] = title
    params['artsdesc'] = desc
    params['artslist'] = ','.join(artslist)
    params['bgimage'] = bgimage

    artists_id = _mysql.artists.add(params)
    if artists_id and artists_id > 0:
        return True
    else:
        return False

def delete_artists_by_id(sid):
    return _mysql.artists.delete(sid)


