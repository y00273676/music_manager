#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

class mediaCarriers(object):
    id2name = {}
    name2id = {}
    def __init__(self):
        pass

def get_all_carriers():
    ret = None
    res = _mysql.carriers.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def load_carriers():
    mediaCarriers.id2name = {}
    mediaCarriers.name2id = {}
    res = _mysql.carriers.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        for carr in res:
            mediaCarriers.id2name[carr['Carrier_ID']] = carr['Carrier_Name']
            mediaCarriers.name2id[carr['Carrier_Name']] = carr['Carrier_ID']
    return True

def add_new_carrier(carr_name):
    res = _mysql.carriers.add_new(carr_name)
    if res:
        mediaCarriers.id2name[res] = carr_name
        mediaCarriers.name2id[carr_name] = res
        return True
    else:
        return False

def carriers_id2name(carr_id):
    if len(mediaCarriers.id2name) == 0:
        load_carriers()
    return mediaCarriers.id2name.get(carr_id)

def carriers_name2id(carr_name):
    if len(mediaCarriers.name2id) == 0:
        load_carriers()
    return mediaCarriers.name2id.get(carr_name)

