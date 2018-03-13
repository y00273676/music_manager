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
import md5
from modules.model.ktv_tvadinfo import *
import logging

logger = logging.getLogger(__name__)

class localCachManage():
    ktv_IntelCach = {}
    
    Ktv_tvadinfoCach = {}
    
    tvadinintervalCach = 0
    
    def GetKtv_tvadinfoByID(id):
        if id in Ktv_tvadinfoCach:
            return Ktv_tvadinfoCach[id]
        return ktv_tvadinfos()
    
    def GetKtv_tvadinfo():
        list=[]
        for i in ktv_IntelCach:
            list.append(ktv_IntelCach[i])
        return list
    
    def getINTEL_GETROOMDEBUGINFO_Key():
        return "INTEL_GETROOMDEBUGINFO"
    
    def getINTEL_GETDEVICEPUBLICPLAN_File_Key():
        return "INTEL_GETDEVICEPUBLICPLAN_File_"+str(type)
    
    def getINTEL_GETCITYLIST_Data_Key():
        return "INTEL_GETCITYLIST_Data"
    
    def getINTEL_GETCITYLIST_Count_Key():
        return "INTEL_GETCITYLIST_Count"
    
    def getINTEL_GETCITYLIST_Key():
        return "INTEL_GETCITYLIST"
    
    def getINTEL_GETROOMPLANLIST_Key():
        return "INTEL_GETROOMPLANLIST"
    
    def getINTEL_GETROOMMODEL_Data_Key():
        return "INTEL_GETROOMMODEL_Data"
    
    def getINTEL_GETROOMMODEL_Count_Key():
        return "INTEL_GETROOMMODEL_Count"
    
    def getINTEL_GETROOMMODEL_Key():
        return "INTEL_GETROOMMODEL"
    
    def getINTEL_GETPLANUSEKTVLIST_Data_Key(id,islocal):
        m1 = md5.new()
        m1.update("INTEL_GETPLANUSEKTVLIST_Data/" + str(id) + "|" + str(islocal))
        md5Text = m1.hexdigest()
        return md5Text
    
    def getINTEL_GETPLANUSEKTVLIST_Count_Key(id,islocal):
        m1 = md5.new()
        m1.update("INTEL_GETPLANUSEKTVLIST_Count/" + str(id) + "|" + str(islocal))
        md5Text = m1.hexdigest()
        return md5Text
    
    def getINTEL_GETPLANUSEKTVLIST_Key():
        return "INTEL_GETPLANUSEKTVLIST"
    
    def getINTEL_GETDEVICEPUBLICPLAN_File_Key(type):
        return "INTEL_GETDEVICEPUBLICPLAN_File_" + str(type)
    
    def getINTEL_GETDEVICEPUBLICPLAN_Data_Key(name, module, roomtype, city):
        m1 = md5.new()
        m1.update("INTEL_GETDEVICEPUBLICPLAN_Data/" + str(name) + "|" + str(module) + "|" + str(roomtype) + "|" + str(city))
        md5Text = m1.hexdigest()
        return md5Text
    
    def getINTEL_GETDEVICEPUBLICPLAN_Data_Key(name, module, roomtype, city):
        m1 = md5.new()
        m1.update("INTEL_GETDEVICEPUBLICPLAN_Data/" + str(name) + "|" + str(module) + "|" + str(roomtype) + "|" + str(city))
        md5Text = m1.hexdigest()
        return md5Text
    
    def getINTEL_GETDEVICEPUBLICPLAN_Count_Key(name, module, roomtype, city):
        m1 = md5.new()
        m1.update("INTEL_GETDEVICEPUBLICPLAN_Count/" + str(name) + "|" + str(module) + "|" + str(roomtype) + "|" + str(city))
        md5Text = m1.hexdigest()
        return md5Text
    
    def getINTEL_GETDEVICEPUBLICPLAN_Key():
        return "INTEL_GETDEVICEPUBLICPLAN"
    
    def getINTEL_GETDEVICEINFO_Key():
        return "INTEL_GETDEVICEINFO"
                
    def getINTEL_GETDEVICEINFO_Count_Key(name,module):
        text="INTEL_GETDEVICEINFO_Count/"+str(name)+"/"+str(module)
        m1 = md5.new()
        m1.update(text)
        md5Text = m1.hexdigest()
        return md5Text
    
    def getINTEL_GETDEVICEINFO_Data_Key(name,module):
        text="INTEL_GETDEVICEINFO/"+str(name)+"/"+str(module)
        m1 = md5.new()
        m1.update(text)
        md5Text = m1.hexdigest()
        return md5Text
    
    def SendCash(_socketClient,key,count_key,data_key):
        flag = False
        if key in ktv_IntelCach:
            obj = ktv_IntelCach[key]
            if obj != None and type(obj) == "<class 'dict'>":
                i = int(obj[count_key])
                dataobj = obj[data_key]
                if i > 0 and dataobj != None and type(dataobj)=="<class 'list'>":
                    data=dataobj.tolist()
                    _socketClient.request.sendall(i)
                    _socketClient.request.sendall(data)
                    flag = True
        return flag
    
    def AddCash(key,count_key,data_key,count,datas):
        if key in ktv_IntelCach:
            ht = {}
            ktv_IntelCach[key]=ht
        if count_key in ktv_IntelCach[key]:
            ktv_IntelCach[key].pop(count_key)
        if data_key in ktv_IntelCach[key]:
            ktv_IntelCach[key].pop(data_key)
        ktv_IntelCach[key][count_key]=count
        ktv_IntelCach[key][data_key]=datas
    
    