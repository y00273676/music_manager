#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月18日

@author: yeyinlin
'''

from common.Thunder import Thunder
from common.yhttp import yhttp
import traceback
import logging
logger = logging.getLogger(__name__)

class SettingDAL(object):
    def __init__(self):
        #self.erphelper=Thunder().Ins().erpdbhelper
        self.dbhelper=Thunder().Ins().Karaokdbhelper

    #获得本地的IP
    def GetSettingValue(self, name):
        try:
            sql = "select config_value from config where config_name='"+str(name)+"'"
            data = self.dbhelper.Query(sql)
            if data:
                return data[0]['config_value']
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def SetSettingInfo(self,name,value):
        try:
            #value=value.decode('utf8').replace('\\','\\\\')
            sql1=""
            sql1="update config set config_value ='"+str(value)+"' where config_name ='"+str(name)+"'"
            logger.debug(sql1)
            data=self.dbhelper.ExecuteSql(sql1)
            return data
        except Exception as e:
            logger.error(traceback.format_exc())
            return None       
   
    def GetSongValidtime(self):
        try:
            sql = "select Configure_SongValidtime from configures"
            data=self.dbhelper.Query(sql)
            if data and len(data)>0:
                return data
            else:
                return None
            
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
        
    #获取所有视频服务器信息
    def GetMainServer(self):
        try:
            sql = "select 1 as id, server_ip from  servers order by server_ip"
            data = self.dbhelper.Query(sql)
            if data and len(data)>0:
                return data
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def GetRooms(self):
        try:
            sql = "select rooms.*,cl.RoomClass_Name from rooms  left join roomclasses cl on cl.RoomClass_ID = rooms.Room_ClassID" 
            data = self.erphelper.Query(sql)
            if data and len(data)>0:
                return data[0]
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def GetServer(self):
        try:
            sql = "select server_ip from  servers order by server_ip"
            data = self.dbhelper.Query(sql)
            if data and len(data)>0:
                return data
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    #获取karaok软件版本号
    def GetKaraokVersion(self):
        try:
            sql = "select config_value as KaraokVersion from config where config_name='karaok_ver'"
            data = self.dbhelper.Query(sql)
            if data and len(data)>0:
                return data[0]['KaraokVersion']
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

if __name__ == '__main__':
    dal=SettingDAL()
    print(dal.GetRooms())
    
