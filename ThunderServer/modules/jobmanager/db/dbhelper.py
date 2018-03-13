#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月6日

@author: yeyinlin
'''
import codecs
import MySQLdb
import logging
import configparser
from MySQLdb import cursors

from common.iniconfig import IniConfig
from common.dateutils import get_today_month
from config.appConfig import AppSet

logger = logging.getLogger(__name__)

def getMediaIdbySerialNo(no):
    sql = "select Media_ID from medias where Media_SerialNo=" + no
    res =doexesqldit([],sql,'karaok')
    dit=[]
    for item in res:
        dic={}
        dic['Media_ID']=item[0]
        dit.append(dic)
    if len(dit)>0:
        return  dit[0]['Media_ID']
    else:
        return  0

def resetsort():
    sql = "update medianewsong set media_Sort=99999 "
    return doexesqldit([],sql,'karaok')

def getSongValidtime():
    sql = "select Configure_SongValidtime from configures"
    res=doexesqldit([],sql,'karaok')
    myres=[]
    dic={}
    dic['Configure_SongValidtime']=res[0]['Configure_SongValidtime']
    myres.append(dic)
    return myres

def insertMediaNewsong(mediaId, time,sort):
    intime = time.strftime('%Y-%m-%D %H-%m',time.localtime(time.time()))
    #获取几个月后的日期
    validtime = get_today_month(time)
    
    sql = "if exists(select 1 from medianewsong where Media_ID='"+ str(mediaId)+"')"
    sql += "Begin update medianewsong set Media_InTime='"+str(intime)+"',Media_ValidUntil='"+str(validtime)+"' ,Media_Sort='"+str(sort)+"' where Media_ID='"+str(mediaId)+"' "
    sql += "ENd else Begin  insert into medianewsong( Media_ID, Media_InTime, Media_ValidUntil, Media_Sort) values ('"+str(mediaId)+"', '"+str(intime)+"','"+str(validtime)+"', '"+str(sort)+"' ) End"
    return doexesqldit([],sql,'karaok')

class dbhelper():
    def __init__(self):
        pass
    #查询
    def Query(self,sql):
        return []
    def ExecuteSql(self,sql):
        return 0

    def getconnect(self,dbname):
        tpath=AppSet().thunder_ini
        cf = IniConfig()
        cf.readfp(codecs.open(tpath, "r", 'utf-8'))
        host = cf.get('MainServer', 'DataBaseServerIp')
        username = cf.get('MainServer', 'UserName')
        password = cf.get('MainServer', 'Password')
        try:
            conn = MySQLdb.connect(host=host, port=3306, user=username, passwd=password, db='karaok', charset='utf8', cursorclass=cursors.DictCursor)
            return conn
        except Exception as e:
            logger.error(traceback.format_exc())

def doexesqldit(a,b,c):
    return ""

if __name__ == '__main__':
    pass
