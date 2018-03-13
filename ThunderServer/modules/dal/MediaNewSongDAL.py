#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月14日

@author: yeyinlin
'''
from common.Thunder import * 
from time import strftime, localtime
import time
import datetime
from common.dateutils import get_today_month
from config.appConfig import AppSet
import logging
logger = logging.getLogger(__name__)

class MediaNewSongDAL(object):
    def __init__(self):
        ins = Thunder().Ins()
        self.helper = ins.Karaokdbhelper

    def ResetSort(self):
        try:
            sql = "update medianewsong set media_Sort=99999 "
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
    
    def GetMediaIdbySerialNo(self,no):
        try:
            sql = "select Media_ID from medias where Media_SerialNo='" + str(no)+"'"
            data=self.helper.Query(sql)
            if data and len(data)>0:
                return data[0]
            else:
                return 0
        except Exception as e:
            logger.error(traceback.format_exc())
            return 0

    def InsertMediaNewsong(self, mediaId, utime, sort):
        try:
            intime=time.strftime('%Y-%m-%d %H-%M',time.localtime(time.time()))
        #获取几个月后的日期
            validtime=get_today_month(int(utime))
            sqlone="select 1 from medianewsong where Media_ID='"+ str(mediaId)+"'"
            data=self.helper.Query(sqlone)
            if data and len(data)>0:
                sql="update medianewsong set Media_InTime='"+str(intime)+"',Media_ValidUntil='"+str(validtime)+"' ,Media_Sort='"+str(sort)+"' where Media_ID='"+str(mediaId)+"'"
            else:
                sql+="insert into medianewsong( Media_ID, Media_InTime, Media_ValidUntil, Media_Sort) values ('"+str(mediaId)+"', '"+str(intime)+"','"+str(validtime)+"', '"+str(sort)+"' )"
            logger.debug('InsertMediaNewsong():  sql = %s' % sql)
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
        
    def GetMediaNewSongTime(self):
        try:
            dbtype=AppSet().DBtype
            if str(dbtype)=="1":
                sql="select top 1 Media_InTime from MediaNewSong order by Media_Sort"
            else:
                sql="select Media_InTime from MediaNewSong order by Media_Sort limit 1"
    #         sql="select {0} Media_InTime from MediaNewSong order by Media_Sort {1}"
            data=self.helper.ExecuteSql(sql)['Media_InTime']
            if not data:
                return '1990-01-01'
            return data
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
        
    def GetSongValidtime(self):
        try:
            sql = "select config_value from config where config_name=CloudMusic_ValidTime"
            data=self.helper.Query(sql)
            if data and len(data)>0:
                return data[0]['config_value']
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
    
if __name__ == '__main__':
    pass
