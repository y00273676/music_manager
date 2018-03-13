#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_languages():
    ret = None
    res = _mysql.langs.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def update_languages(lang_id, lang_name, lang_des):
    return False

################## for import medias info:###########################

class mediaLanguages(object):
    '''
    actually a memcache inside of python class
    '''
    id2name = {}
    name2id = {}
    def __init__(self):
        pass

def load_languages():
    mediaLanguages.id2name = {}
    mediaLanguages.name2id = {}
    res = _mysql.langs.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        for carr in res:
            mediaLanguages.id2name[carr['lang_id']] = carr['lang_name']
            mediaLanguages.name2id[carr['lang_name']] = carr['lang_id']
    return True

def add_new_language(lang_name):
    res = _mysql.langs.add_new(lang_name)
    if res:
        mediaLanguages.id2name[res] = lang_name
        mediaLanguages.name2id[lang_name] = res
        return True
    else:
        return False

def languages_id2name(lang_id):
    if len(mediaLanguages.id2name) == 0:
        load_languages()
    return mediaLanguages.id2name.get(lang_id)

def lanaugages_name2id(lang_name):
    if len(mediaLanguages.name2id) == 0:
        load_languages()
    return mediaLanguages.name2id.get(lang_name)

