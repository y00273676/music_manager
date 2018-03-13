#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from lib import http
from orm import orm as _mysql

def get_all_config():
    res = _mysql.configs.get_all()
    _res = {}
    if isinstance(res, list) and len(res) > 0:
        for item in res:
            _res[item['config_name']] = item
    return _res

def update_setconfig(config):
    if 'CloudMusic_passwd' in config.keys():
        if config['CloudMusic_passwd']:
            config['CloudMusic_passwd'] = hashlib.md5(config['CloudMusic_passwd']).hexdigest().lower()
        else:
            config.pop('CloudMusic_passwd')
    return _mysql.configs.update(config)

def get_config(cname):
    ret = _mysql.configs.get_by_name(cname)
    if isinstance(ret, list):
        return ret[0]
    return ret
