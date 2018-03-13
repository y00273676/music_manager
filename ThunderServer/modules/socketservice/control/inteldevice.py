#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import json
import socket
import hashlib
import threading
import traceback
import datetime
import codecs
import struct
import urllib
import urllib.request
import urllib.parse
from functions import getSignedUrl
from common.KtvInfo import *

logger = logging.getLogger(__name__)

class inteldevice():
    def __init__(self):
        self.name = 'inteldevice';
        ktvInfo=KtvInfo()

    """
    /// <summary>
    /// 根据设备名称和型号获取设备信息
    /// </summary>
    /// <param name="name"></param>
    /// <param name="module"></param>
    /// <returns></returns>
    """
    def getinteldevicebyname(name,module):
        list=[]
        try:
            param={}
            param['op']='getdeviceinfo'
            param['name']=name
            param['module']=module
            def fn(dic,obj):
                dic['intel_desc'] = obj["intel_desc"]
                dic['intel_id'] = obj["intel_id"]
                dic['intel_logo'] = obj["intel_logo"]
                dic['intel_model'] = obj["intel_model"]
                dic['intel_name'] = obj["intel_name"]
            commonFn(list,param,fn)
        except:
            logger.error('inteldevice.getinteldevicebyname')
        return list
    
    def getroomdebuginfo(ip):
        list=[]
        try:
            param={}
            param['op']='getroomdebuginfo'
            param['roomip']=ip
            def fn(dic,obj):
                dic['ktv_id']=ktvInfo._info._ktvid
                dic['ktv_name']=ktvInfo._info._ktvname
                dic['room_debug']=obj['time_debug']
            commonFn(list,param,fn)
        except:
            logger.error('inteldevice.getroomdebuginfo')
        return list
    
    """
    /// <summary>
    /// 根据设备名称和型号以及包房IP获取本地方案
    /// </summary>
    /// <param name="ip"></param>
    /// <param name="name"></param>
    /// <param name="module"></param>
    /// <returns></returns>
    """
    def getprivateplanlist(ip, name, module):
        list=[]
        try:
            param={}
            param['op']='getprivateplanlist'
            param['name']=name
            param['module']=module
            param['roomip']=ip
            def fn(dic,obj):
                dic['plan_id'] = obj["plan_id"]
                dic['plan_name'] = obj["plan_name"]
                dic['plan_url'] = obj["plan_url"]
                dic['plan_time'] = obj["plan_time"]
                plist = getpubplanlistbyid(dic['plan_id'])
                if  plist != None and len(plist) > 0:
                    dic['plan_hot'] = plist[0]['plan_hot']
                    dic['plan_hotname'] = plist[0]['plan_hotname']
                    dic['plan_public'] = plist[0]['plan_public']
                    dic['plan_publicname'] = plist[0]['plan_publicname']
                    dic['plan_usecount'] = plist[0]['plan_usecount']
            commonFn(list,param,fn)
        except:
            logger.error('inteldevice.getprivateplanlist')
        return list
    
    
        
        
        
        
    """  
    /// <summary>
    /// 根据本地私有方案ID获取对应的公开方案信息
    /// </summary>
    /// <param name="id"></param>
    /// <returns></returns>
    """
    def getpubplanlistbyid(id):
        list=[]
        try:
            param={}
            param['op']='getpubplanlistbyid'
            param['id']=id
            def fn(dic,obj):
                dic['plan_id']=obj['plan_id']
                dic['plan_name']=obj['plan_name']
                dic['plan_url']=obj['plan_url']
                dic['city_name']=obj['plan_city']
                dic['plan_hot']=obj['plan_hot']
                dic['plan_hotname']=obj['plan_hotname']
                dic['plan_public']=obj['plan_public']
                dic['plan_publicname']=obj['plan_publicname']
                dic['plan_time']=obj['plan_time']
                dic['plan_url']=obj['plan_url']
                dic['plan_usecount']=obj['plan_usecount']
            commonFn(list,param,fn)
        except:
            logger.error('inteldevice.getpubplanlistbyid')
        return list;
        
    """
    /// <summary>
    /// 获取推荐方案列表
    /// </summary>
    /// <param name="name"></param>
    /// <param name="model"></param>
    /// <param name="rommtype"></param>
    /// <param name="city"></param>
    /// <returns></returns>
    """
    def getpubplanlist(name,model,roomtype,city):
        list=[]
        try:
            param={}
            param['op']='getpubplanlist'
            param['name']=name
            param['model']=model
            param['roomtype']=roomtype
            param['city']=city
            def fn(dic,obj):
                dic['plan_id']=obj['plan_id']
                dic['plan_name']=obj['plan_name']
                dic['plan_url']=obj['plan_url']
                dic['city_name']=obj['plan_city']
                dic['plan_hot']=obj['plan_hot']
                dic['plan_hotname']=obj['plan_hotname']
                dic['plan_public']=obj['plan_public']
                dic['plan_publicname']=obj['plan_publicname']
                dic['plan_time']=obj['plan_time']
                dic['plan_url']=obj['plan_url']
                dic['plan_usecount']=obj['plan_usecount']
                dic['ktv_name']=obj['ktv_name']
            commonFn(list,param,fn)
        except:
            logger.error('inteldevice.getpubplanlist')
        return list
        
        
        
    """
    /// <summary>
    /// 根据方案ID获取使用该方案的ktv列表
    /// </summary>
    /// <param name="planid"></param>
    /// <param name="islocal"></param>
    /// <returns></returns>
    """
    def getplanusektv(planid,islocal):
        list=[]
        try:
            param={}
            param['op']='getplanusektv'
            param['planid']=planid
            param['islocal']=islocal
            idList=[]
            def fn(dic,obj):
                if not obj["log_ktvid"] in idList:
                    dic['ktv_id']=obj['log_ktvid']
                    dic['ktv_name']=obj['log_ktvname']
                    idList.append(obj["log_ktvid"])
            commonFn(list,param,fn)
            idList=None
        except:
            logger.error('inteldevice.getplanusektv')
        return list

    def getroommodel():
        list=[]
        list.push({"room_id":0,"room_name":"全部"})
        try:
            param={}
            param['op']='getroommodel'
            def fn(dic,obj):
                dic['room_id']=obj['room_id']
                dic['room_name']=obj['room_name']
                dic['room_area']=obj['room_area']
            commonFn(list,param,fn)
        except:
            logger.error('inteldevice.getroommodel')
        return list        
        
        
    """
    /// <summary>
    /// 删除本地方案
    /// </summary>
    /// <returns></returns>
    """
    def delprivateplan(id):
        result = 0
        try:
            param = {}
            param['op'] = 'delprivateplan'
            param['planid'] = id
            def fn(obj):
                return result
            commonSingleFn(result,param,fn)
        except:
            logger.error('inteldevice.delprivateplan')
        return result


    """
    /// <summary>
    /// 更新设备更换次数
    /// </summary>
    /// <param name="ip"></param>
    /// <returns></returns>
    """
    def updatedevicetime(ip):
        result = 0
        try:
            param = {}
            param['op'] = 'updatedevicetime'
            param['roomip'] = ip
            def fn(obj):
                logger.error("inteldevice.addprivateplan", url+"?"+requeststr, obj["msg"])
                return result
            commonSingleFn(result,param,fn)
        except:
            logger.error('inteldevice.updatedevicetime')
        return result
        

    def addprivateplan(_localPlan):
        result = 0
        try:
            _localPlan['plan_ktvid'] = ktvInfo._info._ktvid
            param = {}
            param['op'] = 'delprivateplan'
            param['json'] = _localPlan
            def fn(obj):
                logger.error("inteldevice.addprivateplan", url+"?"+requeststr, obj["msg"])
                return result
            commonSingleFn(result,param,fn)
        except:
            logger.error('inteldevice.addprivateplan')
        return result
    
    
    def getcitylist():
        list=[]
        list.push({"city_id":0,"city_name":"全部"})
        try:
            param={}
            param['op']='getarealist'
            param['d']=2
            param['a']=0
            param['time']=time.time()
            key = "36b4442ce621c3ffe64a132b9a4b436c"
            url =  getSignedUrl('http://open.ktv.api.ktvdaren.com/AreaService.aspx?', param, key)
            req = urllib.request.urlopen(url)
            ret = req.read()
            data=urllib.parse.unquote(str(ret, "utf8", "strict"))
            jsonobj = json.loads(data)
            if jsonobj != None and len(jsonobj) > 0:
                if jsonobj["code"]!=1:
                    logger.error("inteldevice.getcitylist", url+"?"+requeststr, data)
                    return list
                result = jsonobj['result']
                if result != None and len(result) > 0:
                    matches = result['matches']
                    if matches != None and len(matches) > 0:
                        for obj in matches:
                            dic={}
                            dic['city_id']=obj['Areaid']
                            dic['city_name']=obj['Areaname']
                            list.append(dic)
        except:
            logger.error('inteldevice.getcitylist')
        return list    
    
    def commonFn(list,param,fn):
        param['ktvid']=ktvInfo._info._ktvid
        param['time']=time.time()
        url =  getSignedUrl('http://ktv.api.ktvdaren.com/ktv_intelService.aspx?', param)
        req = urllib.request.urlopen(url)
        ret = req.read()
        data=urllib.parse.unquote(str(ret, "utf8", "strict"))
        jsonobj = json.loads(data)
        if jsonobj != None and len(jsonobj) > 0:
            if jsonobj["code"] > 0:
                result = jsonobj["result"]
                if result != None and len(result) > 0:
                    matches = result["matches"]
                    if matches != None and len(matches) > 0:
                        for obj in matches:
                            dic={}
                            fn(dic,obj)
                            if not dic == {}:
                                list.append(dic)
                                
    def commonSingleFn(result,param,fn):
        param['ktvid']=ktvInfo._info._ktvid
        param['time']=time.time()
        url =  getSignedUrl('http://ktv.api.ktvdaren.com/ktv_intelService.aspx?', param)
        req = urllib.request.urlopen(url)
        ret = req.read()
        data=urllib.parse.unquote(str(ret, "utf8", "strict"))
        jsonobj = json.loads(data)
        if jsonobj != None and len(jsonobj) > 0:
            if jsonobj["code"] > 0:
                return fn(jsonobj)
            result = jsonobj["result"]

            


class moduleonline(object):
    def __init(self):
        self.name = 'moduleonline'
        self.hmodules = []
        self.vmodules = []
        print(self.name, 'init')
        self.x = 0
    
    def setX(self, x):
        self.x = x
    
    def getX(self):
        return self.x

    def Ins(self):
        hmodules = []
        vmodules = []
        
        #param = 'dogname=' + ktvinfo.dogname + '&op=getktv_moduleonlinelist&storeid=' + ktvinfo.ktvid;
        
        param = 'dogname=' + urllib.parse.quote('张兵帅测试1') + '&op=getktv_moduleonlinelist&storeid=12'
        url =  getSignedUrl('http://ktv.api.ktvdaren.com/module_verservice.aspx?', param)
        print('url', url)
        req = urllib.request.urlopen(url)
        ret = req.read()
        data=urllib.parse.unquote(str(ret, "utf8", "strict"))
        jsonobj = json.loads(data)
        if jsonobj['code']==1:
            for dic in jsonobj['result']['matches']:
                bagtype = int(dic["module_bagtype"])
                info = {}
                info['module_bgpic'] = dic['module_bgpic']
                info['module_dataid'] = int(dic['module_dataid'])
                info['module_datatype'] = int(dic['module_datatype'])
                info['module_id'] = int(dic['module_id'])
                info['module_name'] = dic['module_name']
                info['module_pic'] = dic['module_pic']
                info['module_type'] = int(dic['module_type'])
                info['module_position'] = int(dic['module_position'])
                info['module_movietype'] = int(dic['module_movietype'])
                #DownUtil.Ins.Down(info.module_pic, 0, 0, true);
                #DownUtil.Ins.Down(info.module_bgpic, 0, 0, true);
                print('\a FIXME DownUtil.Ins.Down')
                if bagtype==0:
                    hmodules.append(info)
                else:
                    vmodules.append(info)
        
        self.hmodules = hmodules
        self.vmodules = vmodules
        
        print(self.hmodules)