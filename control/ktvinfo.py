#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import hashlib
from ctypes import *
import logging
import traceback
import threading

from lib.mc import _defaultredis as redis_cli
from control.cloudapi import CloudAPI
from lib.http import request_json
import urllib

logger = logging.getLogger(__name__)

class _KTVInfo(object):

    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_KTVInfo, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance


    def __init__(self):
        self.ktvinfo = None
        pass

    def get_ktvinfo_key(self):
        key = hashlib.md5("cache_ktvinfo_123456789").hexdigest().upper()
        return key

    def hw_dogname(self):
        logger.error("Get doanem from hardware")
        class ss(Structure):
            _fields_=[("name", c_byte*32),]
        filename = "/opt/thunder/lib/libGetDogInfo.so"
        lib = cdll.LoadLibrary(filename)
        t = ss()
        dog= lib.GetDogName(pointer(t))
        tt = create_string_buffer(33)
        memmove(tt, byref(t), 32)
        dname = tt.value.__str__()
        dname = dname.strip().decode('gbk').encode('utf8')
        return dname

    def get_ktvinfo_bydog(self):
        try:
            ktvinfo = None
            dname = self.hw_dogname()
            #print("dogname: %s" % dname)
            if dname == '':
                return None

            url = CloudAPI().KtvInfoURL + "/ktvservice.aspx?op=getktvbydog&dogname=" + urllib.quote(dname)
            result = request_json(url, timeout=10, method='GET')
            #print ('result=%s' % result)
            logger.debug("get ktvinfo: %s, result: %s" % (url, result))
            if result and str(result['code']) == '1':
                if isinstance(result['result'], dict):
                    ktvinfo = result['result']['matches'][0]
                    ktvinfo['dogname'] = dname
        except Exception as ex:
            logging.error(traceback.format_exc())
            return None

        try:
            url = CloudAPI().Alter90URL + "/KtvAppService.aspx?op=getstorejson&dogname=" + urllib.quote(dname)+"&storeid=" + str(ktvinfo['StoreId'])
            dic_res = request_json(url, timeout=10, method='GET')
            if dic_res and str(dic_res['code']) == '1':
                if isinstance(dic_res['result'], dict):
                    result = dic_res['result']['matches']
                    logger.debug("getstoreJson: result:%s" % result)
                    for item in result:
                        ktvinfo['mtype'] = item['ModuleType']
                        ktvinfo['projectver'] = item['ProjectVer']
                        ktvinfo['updatetime'] = item['StoreUpdateTime']
                        ktvinfo['allow_del_song'] = item['IsAllowDelSong']
                        ktvinfo['work_update'] = item["StoreIsWorkingUpdate"]
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

        return ktvinfo
       
    def ktvconfig(self, ktvid, dogname):
        try:
            url = CloudAPI().Alter90URL + "/KtvAppService.aspx?op=getstorejson&dogname=" + yhttp().UrlEncode(AppSet()._dogname)+"&storeid=" + str(self._info.ktvid)
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



    def set_ktvinfo(self, ktvinfo):
        key = self.get_ktvinfo_key()
        ret = redis_cli.set(key, json.dumps(ktvinfo))
        redis_cli.expire(key, 3600 * 24)

    def get_ktvinfo(self):
        key = self.get_ktvinfo_key()
        ret = redis_cli.get(key)
        try:
            if not ret:
                ret = json.loads(ret)
            if isinstance(ret, dict):
                logger.debug("read ktvinfo from cache")
                return ret
        except Exception as ex:
            logger.debug("don't have ktvinfo")
            pass
        
        ret = self.get_ktvinfo_bydog()
        if isinstance(ret, dict):
            self.set_ktvinfo(ret)
        return ret

KTVInfo = _KTVInfo()
