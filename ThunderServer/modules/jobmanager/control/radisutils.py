#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月28日

@author: yeyinlin
'''
import redis
import traceback
import json
from modules.model.SynFileStatus import SynFileStatus
from modules.jobmanager.control.synchronousutils import synchronousutils
import logging

logger = logging.getLogger(__name__)
class radisutils(object):
    
    def __init__(self):
        self.redis = '127.0.0.1'
        self.syn=synchronousutils()

    #连接redis db=1 时为长存在 db=5时为短存在
    def connectradis(self,num):
        r=None
        try:
            r = redis.Redis(host=self.redis, port=6379, db=int(num))
            #r = redis.Redis(host=self.redis, port=6379, db=int(num))
        except Exception as e:
            logger.error(traceback.format_exc())
        return r

    #需要传入 名称 值 和存储的类型（1 为长时间保存 5为短时间保存）
    def savedatabyshort(self,name,data):
        result=0
        try:
            rediaclient=self.connectradis(5)
            rediaclient.set(name,data)
            result=1
        except Exception as e:
            logger.error(traceback.format_exc())
        return 0
    
    def delshortinfobyname(self,name):
        result=0
        try:
            rediaclient=self.connectradis(5)
            rediaclient.delete(name)
            result=1
        except Exception as e:
            logger.error(traceback.format_exc())
        return result
    
    def getshortinfobyname(self,name):
        data=None
        try:
            rediaclient=self.connectradis(5)
            data=rediaclient.get(name)
        except Exception as e:
            logger.error(traceback.format_exc())
        return data

    #分类的名称  目标的路径list集合
    def updatadownrecode(self,name,filepath):
        data=self.getshortinfobyname(name)
        #如果能够查询到数据 
        redisdata=[]

        if data:
            redisdata = json.loads(data)
            for item in redisdata:
                item['status']=1
                if item['tagpath'] in filepath:
                    del redisdata[item]

        for item in  filepath:
            syn = SynFileStatus()
            syn.tagpath=filepath
            syn.status=0       
            redisdata.append(json.loads(str(syn)))
        self.savedatabyshort(name, redisdata)
    
    def delalldeletefile(self,name):
        data=self.getshortinfobyname(name)
        redisdata=[]
        try:
            if data:
                redisdata=json.loads(data)
                for item in redisdata:
                    if item['status']==1:
                        if self.syn.deletefilefromserver(item['tagpath'])==1:
                            del redisdata[item]
        except Exception as e:
            logger.error(traceback.format_exc())
        
if __name__ == '__main__':
    pass
