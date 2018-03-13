#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import traceback
from lib import http
from orm import orm as _mysql
from orm.mm import getMedia_sequenceNoPY, sp_GetFirstAvailableID, getMedia_sequenceNoPY, addActorGetNo, sp_AddActor


logger = logging.getLogger(__name__)

def get_all_actors(page, psize,text):
    ret = None
    res = _mysql.actors.get_by_all(page, psize, text)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def get_by_count(text):
    count = _mysql.actors.get_by_count(text)
    ret = {}
    ret['total'] = count
    return ret

def update_actor(obj):
    return _mysql.actors.update_actor(obj)

def new_actor_no():
    pass

def add_actor(obj):
    return _mysql.actors.merge_actor(obj)
    
