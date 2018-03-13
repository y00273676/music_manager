#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-03 13:51:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
import ConfigParser
from lib.iniconfig import IniConfig
import os
import os.path
from orm import orm as _mysql

def find_karaok_version():
    res = _mysql.karaokversion.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def find_last_karaok_version():
    maxid=0
    ktvversion=''
    ver_list = find_karaok_version()
    if ver_list == None:
        return ktvversion
    for i in ver_list:
        if i['KaraokVersion_ID']!=None:
            if int(i['KaraokVersion_ID'])>maxid:
                maxid=int(i['KaraokVersion_ID'])
                ktvversion=i['KaraokVersion_ver']
                
    return ktvversion
        

