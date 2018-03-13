#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:25:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import time
import setting
import logging
import hashlib
import traceback
import json
import re
import glob
import string


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int
from control.menpai import *
import ConfigParser
from control.rooms import *

logger=logging.getLogger(__name__)

class MenpaiHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('boxs.html')

    @gen.coroutine
    def post(self):

        mtype=self.get_argument('type')

        logger.debug("有反应")
        print mtype

        _res = {}
        _res['code'] = 0
        #添加
        if  mtype=="1":
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            result=add_menpai(mjsondata)
            if result =='0':
                _res['msg'] = '操作成功'
            else:
                _res['code'] = 1
                _res['msg'] ='操作失败'

            self.send_json(_res)
        elif mtype=="2":
            _res['data'] = get_all_set_info()
            _res['mediaad'] = get_all_mediadetails(1,100,'','3')
            _res['fangtai'] = get_men_pai_info()
            self.send_json(_res)    
            
        elif mtype=="3":
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            if updata_menpai(mjsondata):
                _res['code'] = 0
                _res['msg']='操作成功'
            else:
                _res['code'] = 1
                _res['msg']='操作失败'
           
            self.send_json(_res)    
        elif mtype=="4":
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            deleter=delete_menpai_roomid(mjsondata['MenPaiAdSetting_Id'])
            if deleter:
                _res['code'] = 0
                _res['msg']='操作成功'
            else:
                _res['code'] = 1
                _res['msg']='操作失败'
           
            self.send_json(_res)    
        
        elif mtype=="5":
            menpaizh=[]
            
            
            for room in get_men_pai_info():
                roomzh={}
                roomzh['Room_ID']=room['Room_ID']
                roomzh['Room_SerialNo']=room['Room_SerialNo']
                roomzh['Room_IpAddress']=room['Room_IpAddress']
                roomzh['Room_Name']=room['Room_Name']
                roomzh['MenPaiType_ID']=""
                menpaiarr=[]
                tempad=""
                tempadno=""
                
                if get_all_set_info()!=None:
                    for menpai in get_all_set_info():
                        if str(room['Room_ID']) == str(menpai['MenPaiAdSettings_RoomID']):
                            roomzh['MenPaiType_ID']=menpai['MenPaiType_ID']
                            if menpai['MenPaiType_ID']==0:
                                roomzh['MenPaiType_Name']="横版"
                            else :
                                roomzh['MenPaiType_Name']="竖版"
                            menpaipart={}
                            menpaipart['MenPaiAdSetting_SerialNo']=menpai['MenPaiAdSetting_SerialNo']
                            menpaipart['MenPaiAdSetting_Id']=menpai['MenPaiAdSetting_Id']
                            tempadno+=str(menpai['MenPaiAdSetting_SerialNo'])
                            tempadno+='/'
                            for ad in get_all_mediadetails(1,100,'','3')['matches']:
                                if str(ad['Media_SerialNo'])==str(menpai['MenPaiAdSetting_SerialNo']):
                                    menpaipart['Media_Name']=ad['Media_Name']
                                    tempad+=ad['Media_Name']
                                    tempad+='/'
                            menpaiarr.append(menpaipart)
                roomzh['tempad']=tempad
                roomzh['tempadno']=tempadno
                roomzh['menpaiarr']=menpaiarr
                menpaizh.append(roomzh)                
            _res['data'] = get_all_set_info()
            _res['mediaad'] = get_all_mediadetails(1,100,'','3')
#             _res['fangtai'] = get_men_pai_info()
            _res['menpaizh'] = menpaizh
            self.send_json(_res)    
        elif mtype=="6":
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            roomidarr=mjsondata['roomid']
            adtype=mjsondata['adtype']
            adinfoarr=mjsondata['adinfo']
            isall=mjsondata['isall']
            
            if isall=='Y':
                roomidarr=[]
                delete_menpaiall()
                for room in get_men_pai_info():
                    roomidarr.append(room['Room_ID'])
            for roomid in roomidarr:
                delete_menpai_roomid(roomid)
                for adinfo in adinfoarr:
                    menpaiinfo={}
                    menpaiinfo['MenPaiAdSetting_SerialNo']=adinfo
                    menpaiinfo['MenPaiAdSetting_PlayCount']=5
                    menpaiinfo['MenPaiType_ID']=adtype
                    menpaiinfo['MenPaiAdSettings_RoomID']=roomid
                    add_menpai(menpaiinfo)
            self.send_json(_res)    
        else:
            pass
