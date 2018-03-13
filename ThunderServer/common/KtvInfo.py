#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年4月7日

@author: yeyinlin
'''
import traceback
import logging
import time
import json
import threading
from config.appConfig import AppSet
from common.yhttp import yhttp
from modules.model.ktvinfo import ktv_info
import logging
logger = logging.getLogger(__name__)

class KtvInfo():
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('KtvInfo singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(KtvInfo, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('KtvInfo singleton is exists')
        return cls.__instance

    def __init__(self):
        self._info = None
        #for leike_x86
        #self.lk = 1
        #for leike_arm
        self.lk = 2

    def get_ktvinfo(self):
        if self._info:
            return self._info
        else:
            self.refresh_ktvinfo()
            return self._info

    def refresh_ktvinfo(self):
        try:
            DogName = AppSet()._dogname
            url = AppSet().GetCloudKtvIniValue("KtvInfoURL") + "/ktvservice.aspx?op=getktvbydog&dogname=" + yhttp().UrlEncode(DogName)
            print(url)
            result = yhttp().get_y(url,10)
            dic_res = json.loads(result)
            logger.debug("get ktvinfo: %s, result: %s" % (url, result))
            if dic_res and str(dic_res['code']) == '1':
                if isinstance(dic_res['result'], dict):
                    dic_ktv = dic_res['result']
                    ktv = dic_ktv['matches'][0]
                    self._info = ktv_info()
                    self._info.ktvid = int(ktv['StoreId'])
                    self._info.ktvname = ktv['StoreName']
                    self._info.jd = float(ktv['Jd'])
                    self._info.wd = float(ktv['Wd'])
                    self._info.city = ktv['City']
                    self._info.provincename = ktv['Province']
                    self._info.country = ktv['Country']
                    self._info.hostaddress = ktv['Hostaddress']
                    self._info.stbsystemboot = ktv['stbsystemboot']
                    #获取ktv省市id
                    try:
                        url = AppSet().GetCloudKtvIniValue("KtvInfoURL") + "/ktvservice.aspx?op=getktvcity&storeid=" + str(self._info.ktvid)
                        result = yhttp().get_y(url,10)
                        dic_res = json.loads(result)
                        if dic_res and str(dic_res['code']) == '1':
                            if isinstance(dic_res['data'], dict):
                                dic_city = dic_res['data']
                                self._info.province = str(dic_city['provincenum'])
                    except Exception as ex:
                        self._info = None
                        logging.error('KtvInfo init excepted')
                        logging.error(str(ex))
                        logging.error(traceback.format_exc())
#                         self.init_ktvmeta(self._info.ktvid)
            self.ktvconfig()
        except Exception as ex:
            self._info = None
            logging.error('KtvInfo init excepted')
            logging.error(str(ex))
            logging.error(traceback.format_exc())
            
    def ktvconfig(self):
        try:
            url = AppSet().GetCloudKtvIniValue("Alter90URL") + "/KtvAppService.aspx?op=getstorejson&dogname=" + yhttp().UrlEncode(AppSet()._dogname)+"&storeid=" + str(self._info.ktvid)
            result = yhttp().get_y(url,10)
            dic_res = json.loads(result)
            if dic_res and str(dic_res['code']) == '1':
                if isinstance(dic_res['result'], dict):
                    result = dic_res['result']['matches']
                    logger.debug("getstoreJson: result:%s" % result)
                    for item in result:
                        self._info.mtype = item['ModuleType']
                        self._info.projectver = item['ProjectVer']
                        self._info.updatetime = item['StoreUpdateTime']
                        work_update = item["StoreIsWorkingUpdate"]
        except Exception as e:
            logger.error(traceback.format_exc())
            pass

    #判断当前时间时候进行数据更新
    def MatchTime(self):
        #TODO需要 判断当前时间时候进行数据更新
        return True
    
hdl_ktvinfo = KtvInfo()

if __name__ == '__main__':
    info=KtvInfo()
    print (info._info._mtype)
