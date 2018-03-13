#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib import http
from orm import orm as _mysql

def get_all_mediatype():
    ret = None
    res = _mysql.mediatype.get_by_all()
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def update_mediatype(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds, MediaType_NewTypeID):
    params = {}
    params['MediaType_ID'] = MediaType_ID
    params['MediaType_Name'] = MediaType_Name
    params['MediaType_Description'] = MediaType_Description
    params['MediaType_IsMovie'] = MediaType_IsMovie
    params['MediaType_IsKaraok'] = MediaType_IsKaraok
    params['MediaType_IsAds'] = MediaType_IsAds
    params['MediaType_NewTypeID'] = MediaType_NewTypeID
    
    return _mysql.mediatype.update(MediaType_ID, params)


def add_mediatype(**mediaType):
    return sp_addmediatype(**mediaType)
    
