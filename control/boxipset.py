#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-19 16:04:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql
import ConfigParser
from lib.iniconfig import IniConfig


def get_all_set_info():
    res = _mysql.boxipset.get_all(1)
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def update_setip(flag,ipaddress,subnetmask, serviceip,devicetype, devicegraphics, iprecond):
    params = {}
    params['ipaddress'] = ipaddress
    params['subnetmask'] = subnetmask
    params['serviceip'] = serviceip
    params['devicetype'] = devicetype
    params['devicegraphics'] = devicegraphics
    params['iprecond'] = iprecond

    return _mysql.boxipset.update(flag, params)

def updata_setip_ini(filename,ipaddress,subnetmask, serviceip,devicetype, iprecond,name):
    cf = IniConfig()
    cf.read(filename)
    cf.set("STB", "IP", ipaddress)
    cf.set("STB", "NMASK", subnetmask)
    cf.set("STB", "SERVER", serviceip)
    cf.set("STB", "STBType", devicetype)
    cf.set("STB", "RecordSvr", iprecond)
    cf.set("STB", "Name", name)
    cf.write(open(filename, "w"))
    
def updata_setsome_ini(filename,subnetmask, serviceip,devicetype, iprecond):
    cf = IniConfig()
    cf.read(filename)
    cf.set("STB", "NMASK", subnetmask)
    cf.set("STB", "SERVER", serviceip)
    cf.set("STB", "STBType", devicetype)
    cf.set("STB", "RecordSvr", iprecond)
    cf.write(open(filename, "w"))



