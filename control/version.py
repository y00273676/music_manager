#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback

from lib import http
from orm import orm as _mysql

def get_all_version(page, psize):
    ret = None
    total = _mysql.version.get_all_count()
    if (page - 1) * psize > total:
        vers = {}
    else:
        vers = _mysql.version.get_all(page, psize)
    if isinstance(vers, list) and len(vers) > 0:
        ret = {}
        ret['matches'] = vers
        ret['total'] = total
    return ret

def get_version_by_id(sid):
    res = _mysql.version.get_by_id(sid)
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    else:
        return None

def update_version(verid, vercode, channelid, systemversion, verdesc, versize, auto_update, force_update, ver_url, userid):
    params = {}
    params['verid'] = vercode
    params['vercode'] = vercode
    params['channelid'] = channelid
    params['systemversion'] = systemversion
    params['verdesc'] = verdesc
    params['versize'] = versize
    params['ver_url'] = ver_url
    params['auto_update'] = auto_update
    params['userid'] = userid
    params['force_update'] = force_update

    return _mysql.version.update(verid, params)

def add_new_version(vercode, channelid, systemversion, verdesc, versize, auto_update, force_update, ver_url, userid):
    params = {}
    params['vercode'] = vercode
    params['channelid'] = channelid
    params['systemversion'] = systemversion
    params['verdesc'] = verdesc
    params['versize'] = versize
    params['ver_url'] = ver_url
    params['auto_update'] = auto_update
    params['userid'] = userid
    params['force_update'] = force_update

    version_id = _mysql.version.add(params)
    if version_id > 0:
        return True
    else:
        return False

def delete_version_by_id(sid):
    return _mysql.version.delete(sid)

def get_system_ver():
    ver = ''
    ver_file = '/etc/version'
    try:
        if os.path.exists(ver_file):
            ver = open(ver_file).read()
            if len(ver) > 32:
                ver = ver[:32]
        else:
            ver = '0.0.0-20170000'
    except Exception as ex:
        print traceback.format_exc()
    return ver.strip()
 


