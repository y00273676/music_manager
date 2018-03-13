#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ConfigParser import ConfigParser
ini = '/opt/thunder/thunder.ini'


def read_all_setting():
    datajson={}
    cf = ConfigParser()
    # cf.read(filename)
    cf.read(ini)
    sections = cf.sections()
    mainserver=cf.items("MainServer")
    erpserver=cf.items("ErpServer")
    misc=cf.items("Misc")
    ktv=cf.items("KTV")
    erp=cf.items("ERP")

    _mjson={}
    _mprjson={}
    _mmijson={}
    _mktvjson={}
    _merpjson={}

    for colum in mainserver:
        _mjson[colum[0]]=colum[1]
    for columone in erpserver:
        _mprjson[columone[0]]=columone[1]

    for columtwo in misc:
        _mmijson[columtwo[0]]=columtwo[1]
    for columtwo in ktv:
        _mktvjson[columtwo[0]]=columtwo[1]
    for columtwo in erp:
        _merpjson[columtwo[0]]=columtwo[1]


    datajson['mainserver']=_mjson
    datajson['erpserver']=_mprjson
    datajson['misc']=_mmijson
    datajson['erp']=_merpjson
    datajson['ktv']=_mktvjson
    print datajson
    return datajson

data =  read_all_setting()
DB = {
    'host':data["mainserver"]["databaseserverip"],
    'user':data["mainserver"]["username"],
    'pass':data["mainserver"]["password"],
    'dbname':'karaok',
    'charset':'utf8',
    'port':3306
}
