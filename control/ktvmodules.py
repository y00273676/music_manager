#!/usr/bin/env python
# -*- coding: utf-8 -*-

from orm import orm as _mysql

def get_all_ktvmodules(bagtype=0):
    res = _mysql.ktvmodules.get_all(bagtype)
    if isinstance(res, list) and len(res) > 0:
        return dict(matches=res, total=len(res))
    return None

def get_ktvmodule(mid):
    res = _mysql.ktvmodules.get_by(mid)
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    return None

def get_latest_ktvmodules(bagtype=0):
    res = _mysql.ktvmodules.get_latest(bagtype)
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    return None

def delete_ktvmodule(mid):
    return _mysql.ktvmodules.delete(mid)

def add_ktvmodule(info):
    '''
    更新模板信息
    '''
    return _mysql.ktvmodules.add_module(info)


def update_ktvmodule(info):
    '''
    更新模板信息
    '''
    return _mysql.ktvmodules.update(info)

