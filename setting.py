#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import codecs

from lib.iniconfig import IniConfig

def _get_dbinfo():
    cf = IniConfig()
    cf.readfp(codecs.open('/opt/thunder/thunder.ini', "r", 'utf8'))
    ini_master = cf.items("MainServer")
    dbinfo = {}
    dbinfo['host'] = '127.0.0.1'
    dbinfo['passwd'] = 'Thunder#123'
    dbinfo['user'] = 'root'
    dbinfo['port'] = 3306
    dbinfo['db'] = 'karaok'
    for item in ini_master:
        if item[0] == 'UserName':
            dbinfo['user'] = item[1]
        elif item[0] == 'Password':
            dbinfo['passwd'] = item[1]
        elif item[0] == 'DataBaseServerIp':
            dbinfo['host'] = item[1]

    return dbinfo

dbinfo = _get_dbinfo()

# Mysql config used by sqlachemy(ORM) code
MYSQL = {
    'master': dbinfo,
    'slaves': [],
    'dbs': ['karaok']
}

REDIS = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0
}

#Session configuration(implemented on REDIS)
session_conf = {
    'cookie_secret': "e346977943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
    'session_secret': "4cdcb9f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
    'session_timeout': 1200,
    'store_options': REDIS,
    }

app_conf = {
    'allowips': [],
    'appkey': 'e6f9c625e6b9c11e3bb1b94de806d865',
    'template_path': os.path.join(os.path.dirname(__file__), "tpl"),
    'static_path': os.path.join(os.path.dirname(__file__), "static")
    }

#use to get song name from songno
KCLOUD_SERVER_URL = "http://kcloud.v2.service.ktvdaren.com"

#use for login authentication
OpenApiURL = "http://open.ktv.api.ktvdaren.com"
DHCP_CONFIG_PATH = '/opt/thunder/bin/dhcp'
TMPDIR = "/data/tmp"
DOWNLOADDIR = "/data/download"
HTDOCDIR = "/opt/thunder/www"

