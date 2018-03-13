#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-25 15:07:55
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
import ConfigParser
import glob


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int

from control.theme import get_all_theme_info
from control.rooms import get_all_rooms_info
from control.rooms import get_part_info_no
from control.rooms import get_part_info_ip
from control.rooms import add_part_info
from control.rooms import add_rooms_by_progress
from control.rooms import upata_part_info
from control.rooms import delete_room
from control.rooms import one_delete_room
from control.rooms import one_motify_rooms



from control.skin import get_all_skin_info
from control.skin import get_part_skin_info
from control.skin import add_new_skin
from control.skin import updata_new_skin
from control.skin import delete_skin


from control.configures import get_all_config_info
from control.fileservers import sp_roomktvservermapping
from control.fileservers import sp_AutoMac
from control.servergroups import find_file_servers


from control.boxs import *

from control.modbc import comp_by_ip

from control.serverutils import *



logger=logging.getLogger(__name__)



class FangTaiHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        print "mtype"
        self.render('fangtaiset.html')

    @gen.coroutine
    def post(self):
        mtype=self.get_argument('type')

        logger.debug("有反应")


        if  mtype=="1":
            _res = {}
            datachange=self.get_argument('datachange')
            mdata=self.get_argument('mdata')
            _res['msg'] = "修改成功"
            if datachange=="add":
                jsondata=json.loads(mdata)
                if jsondata['isbatch']=="1":
                    #循环添加
                    start=jsondata['startnum']
                    end=jsondata['endnum']
                    ip=jsondata['Room_IpAddress']
                    for i in range(int(start), int(end) + 1):
                        part=get_part_info_no(i)
                        if(part==None):
                        # mflag=add_part_info(jsondata)
                            jsondata['Room_SerialNo']=str(i)
                            jsondata['Room_IpAddress']=ip+str(i)
                            mflag=add_rooms_by_progress(jsondata)
                            if mflag>=0:
                                flag=add_new_skin(mflag,i,jsondata['skin_theme_id'],jsondata['skin_name'])
                            if mflag>=0:
                                _res['msg'] = str(i)+"房台添加"
                            else:
                                _res['msg'] = str(i)+"添加房台失败"
                        # if(flag):
                        #     _res['msg'] = num+"房台添加"
                        # else:
                        #     _res['msg'] = num+"添加皮肤失败"
                        else:
                            _res['msg'] = "当前房台已存在"
                        
                    
                    
                else:
                    num=jsondata['Room_SerialNo']
                    part=get_part_info_no(num)
                    if(part==None):
                        # mflag=add_part_info(jsondata)
                        mflag=add_rooms_by_progress(jsondata)
                        print "mnm"+str(mflag)
                        if mflag>=0:
                            flag=add_new_skin(mflag,jsondata['Room_SerialNo'],jsondata['skin_theme_id'],jsondata['skin_name'])
                            sp_roomktvservermapping()
                        if mflag>=0:
                            _res['msg'] = num+"房台添加"
                        else:
                            _res['msg'] = num+"添加房台失败"
                        # if(flag):
                        #     _res['msg'] = num+"房台添加"
                        # else:
                        #     _res['msg'] = num+"添加皮肤失败"
                    else:
                        _res['msg'] = "当前房台已存在"
            elif datachange=="updata":
                # upata_part_info(json.loads(mdata))
                one_motify_rooms(json.loads(mdata))
                updata_new_skin(json.loads(mdata))

            elif  datachange=="delete":
                jsondata= json.loads(mdata)
                try:
                    stopServiceOut('dhcp')
                # 删除文件
                    if delete_file_ini(jsondata['mac']):
                        _res['synsize'] = set_stb_syscn()
                        if jsondata['Room_SerialNo']!="":
                            part=get_part_info_no(jsondata['Room_SerialNo'])
                            if(part!=None):
                                one_delete_room(jsondata['Room_SerialNo'])
                                if get_all_rooms_info()!=None:
                                    sp_roomktvservermapping()
                        _res['msg'] = "删除成功"
                        _res['code'] = 0
                    else:
                        _res['msg'] = "删除失败"
                        _res['code'] = 1
                    
                    startServiceOut('dhcp')
                except:
                    _res['msg'] = "删除失败"
                    _res['code'] = 1

            self.send_json(_res)
        elif mtype=="3":
            sp_roomktvservermapping()
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            self.send_json(_res)
        elif mtype=="4":
            sp_AutoMac()
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            self.send_json(_res)
            
        elif mtype=="5":
            # 需要取出所有盒子的信息
            starttime=int(time.time())
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            files=[]
            files_one=[]
            files_two=[]
            #拿出所有的文件夹
            for filename in glob.glob(str_val+"*.ini"):
                conjson={}
                #检查是否含有标签
#                 update_init_ini(filename)
                name=filename.replace(str_val,"")
                mname=name.replace(".ini","")
                #文件名称
                mystbinfo=find_stb_info_defult(filename)
                conjson['filename']=mname
                conjson['isuse']=mystbinfo[0]
                conjson['Stbtype']=mystbinfo[2]
                conjson['Room_ID']=''
                conjson['Room_SerialNo']=""
                conjson['Room_IpAddress']=mystbinfo[1]
                conjson['Room_OrderType']=""
                conjson['Room_STBtype']=""
                conjson['Room_MAC1']=""
                conjson['skin_name']=""
                conjson['skin_id']=""
                conjson['Room_Name']=mystbinfo[3]
                #用名称去取房台信息
                
                if conjson['Room_IpAddress']!='':
                    partinfos=get_part_info_ip(conjson['Room_IpAddress'])
                    if partinfos!=None:
                        partinfo=partinfos[0]
                        skins=get_part_skin_info(conjson['Room_IpAddress'].split('.')[3])
                        skin_name=""
                        skin_id=0
                        if(skins!=None):
                            skin=skins[0]
                            skin_name=skin["skin_theme_name"]
                            skin_id=skin["skin_theme_id"]
                        conjson['Room_ID']=partinfo['Room_ID']
                        conjson['Room_SerialNo']=partinfo['Room_SerialNo']
                        conjson['Room_IpAddress']=partinfo['Room_IpAddress']
                        conjson['Room_OrderType']=partinfo['Room_OrderType']
                        conjson['Room_STBtype']=partinfo['Room_STBtype']
                        if partinfo['Room_STBtype']==0:
                            conjson['Room_STBtype_Name']="包房机顶盒"
                        else:
                            conjson['Room_STBtype_Name']="门牌机"
                        conjson['Room_MAC1']=partinfo['Room_MAC1']
                        conjson['skin_name']=skin_name
                        conjson['skin_id']=skin_id
                        
                if conjson['Room_SerialNo']=="":
                    files_one.append(conjson)
                else:
                    files_two.append(conjson)       
            
            files_two.sort(comp_by_ip)
         
            infojson={}
            infojson['rooms']=files_one+files_two
            infojson['theme']=get_all_theme_info()
            infojson['configures']=get_all_config_info()
            infojson['server']=find_file_servers()
            endtime=int(time.time())
            print ("time cha:",endtime-starttime)
            self.send_json(infojson)
           

        else:
            mjson={}
            roomscontent=get_all_rooms_info()
            
            if roomscontent==None:
                roomscontent=[]

            select_value=[]
            #需要组装数据
            for item in roomscontent:
                skins=get_part_skin_info(item['Room_SerialNo'])
                skin_name=""
                skin_id=0
                if(skins!=None):
                    skin=skins[0]
                    skin_name=skin["skin_theme_name"]
                    skin_id=skin["skin_theme_id"]
                mselect={}

                mselect['Room_ID']=item['Room_ID']
                mselect['Room_SerialNo']=item['Room_SerialNo']
                mselect['Room_Name']=item['Room_Name']
                mselect['Room_IpAddress']=item['Room_IpAddress']
                mselect['Room_OrderType']=item['Room_OrderType']
                mselect['Room_STBtype']=item['Room_STBtype']
                mselect['Room_MAC1']=item['Room_MAC1']
                mselect['skin_name']=skin_name
                mselect['skin_id']=skin_id
                select_value.append(mselect)


            infojson={}
            infojson['rooms']=select_value
            infojson['theme']=get_all_theme_info()
            infojson['configures']=get_all_config_info()
            

            self.send_json(infojson)

