#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-22
# @Author  : yishunli@thunder.com.cn
# @Version : 01
# @Description: re-arch the old code, add specified api for server info

import commands
import traceback
import logging

from orm import orm as _mysql
from orm.mountdisk import list_all_disk

logger=logging.getLogger(__name__)

def get_all_servers():
    res = _mysql.servers.get_all()
    if isinstance(res, list):
        return dict(matches=res, total=len(res))
    return None

def get_server_ips():
    res = _mysql.servers.get_all_ip()
    servers = []
    if isinstance(res, list):
        for s in res:
            servers.append(s['server_ip'])
    return servers

def get_server(svrid):
    res = _mysql.servers.get_server()
    if isinstance(res, list):
        return dict(matches=res, total=len(res))
    return None

def add_server(svrinfo):
    return _mysql.servers.add(svrinfo)

def count_server():
    return _mysql.servers.count()

def del_server(svrid):
    return _mysql.servers.delete(svrid)

def update_server(svrinfo):
    return _mysql.servers.update(svrinfo)

def list_disk_all():
    return list_all_disk()

def list_dir(fpath):
    res = []
    try:
        resultText = commands.getoutput('ls -lh /video/' + fpath)
        resultList = resultText.split("\n")
        for line in resultList:
            flist = line.split()
            if flist[0]=="total" or flist[len(flist)-1]=="./" or flist[len(flist)-1]=="../":
                continue
            finfo = {}
            if flist[0][0] == "-":
                finfo['type'] = "f"
            if flist[0][0] == "d":
                finfo['type'] = "d"
            finfo["size"] = flist[4]
            finfo["name"] = flist[8]
            res.append(finfo)
    except:
        logger.error(traceback.format_exc())
        pass
    return res


