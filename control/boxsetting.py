#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 17:35:43
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql

def add_new_setting(optionid,ktvid, optionname,name, appvalue, boxtype, result,typename):
    params = {}
    params['optionid'] = optionid
    params['ktvid'] = ktvid
    params['optionname'] = optionname
    params['name'] = name
    params['appvalue'] = appvalue
    params['boxtype'] = boxtype
    params['result'] = result
    params['typename'] = typename
    option_id = _mysql.boxsetting.add(params)
    if option_id > 0:
        return True
    else:
        return False

def update_setting(optionid,ktvid, optionname,name, appvalue, boxtype, result,typename):
    params = {}
    params['optionid'] = optionid
    params['ktvid'] = ktvid
    params['optionname'] = optionname
    params['name'] = name
    params['appvalue'] = appvalue
    params['boxtype'] = boxtype
    params['result'] = result
    params['typename'] = typename

    return _mysql.boxsetting.update(optionid, params)
