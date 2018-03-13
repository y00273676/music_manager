#!/usr/bin/env python
# -*- coding: utf-8 -*-

from orm import orm as _mysql
import glob

def get_all_themes():
    res = _mysql.themes.get_all()
    if isinstance(res, list) and len(res) > 0:
        return dict(matches=res, total=len(res))
    return None

def get_theme_list():
    res = _mysql.themes.get_all()
    themes = []
    if isinstance(res, list) and len(res) > 0:
        for t in res:
            themes.append(dict(theme_name=t['theme_name'],theme_id=t['theme_id']))
        return themes
    return None



def get_theme(themeid):
    res = _mysql.themes.get_by_id()
    if isinstance(res, list) and len(res) > 0:
        return res[0]
    return None


def delete_theme(tid):
    return _mysql.themes.delete(tid)

def add_theme(info):
    '''
    更新模板信息
    '''
    return _mysql.themes.add(info)


def update_theme(info):
    '''
    更新模板信息
    '''
    return _mysql.themes.update(info)

