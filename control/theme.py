#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-25 10:54:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql
import glob


def get_all_theme_info():
    res = _mysql.theme.get_all(1)
    if isinstance(res, list) and len(res) > 0:
        themearr=[]
        for mtheme in res:
            if mtheme['theme_name']=='骄阳':
                continue
            themearr.append(mtheme)
        return themearr
    return None

def get_theme_package():
    alltheme=[]
    str_val='/opt/thunder/www/Skin/'
    for filename in glob.glob(str_val+"*.img"):
        name=filename.replace(str_val,"")
        mname=name.replace(".img","")
        alltheme.append(mname)
    return alltheme
    
    
