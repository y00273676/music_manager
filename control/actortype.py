#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

from lib import http
from orm import orm as _mysql

logger = logging.getLogger(__name__)

def get_all_actortype():
    ret = None
    res = _mysql.actortype.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret
 
################## for import medias info:###########################

class actorTypes(object):
    '''
    actually a memcache inside of python class
    '''
    id2name = {}
    name2id = {}
    def __init__(self):
        pass

def load_actortype():
    actorTypes.id2name = {}
    actorTypes.name2id = {}
    res = _mysql.actortype.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        for carr in res:
            actorTypes.id2name[carr['actortype_id']] = carr['actortype_name']
            actorTypes.name2id[carr['actortype_name']] = carr['actortype_id']
    return True

def add_new_actortype(ac_name):
    tinfo = {}
    logger.info("add actortype: (%s)" % ac_name)
    tinfo['actortype_name'] = ac_name
    tinfo['actortype_desc'] = ac_name
 
    res = _mysql.actortype.add_actortype(tinfo)
    if res:
        actorTypes.id2name[res] = ac_name
        actorTypes.name2id[ac_name] = res
        return res
    else:
        return None

def actortype_id2name(ac_id):
    if len(actorTypes.id2name) == 0:
        load_actortype()
    return actorTypes.id2name.get(ac_id)

def actortype_name2id(ac_name):
    if len(actorTypes.name2id) == 0:
        load_actortype()
    return actorTypes.name2id.get(ac_name)
   
