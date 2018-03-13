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
import ConfigParser
import os

from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int


from control.boxsetting import add_new_setting
from control.boxset import update_setting
from control.boxset import update_set
from control.boxset import update_flag

from control.boxset import get_all_set_list
from control.boxipset import get_all_set_info
from control.boxipset import update_setip
from control.boxipset import updata_setip_ini,updata_setsome_ini
from control.boxset import get_all_set_list_ini
from control.boxset import get_all_config_ini
from control.boxset import add_config_ini
from control.boxset import updata_config_ini
from control.boxset import update_set_ini,remove_update_ini
from control.boxset import remove_set_ini
from control.boxset import delete_config_ini
from control.rooms import *

from control.skin import updata_new_skin
from control.skin import add_new_skin
from control.rooms import add_rooms_by_progress
from control.fileservers import sp_roomktvservermapping
from control.boxs import update_init_ini,find_stbip_name
from control.boxs import set_stb_syscn,set_stb_syscn_by_file
from control.boxs import is_a_nect,copyfile

from control.mboxini  import get_box_type_ini
from control.menpai import *

from control.fileservers import sp_AutoMac,find_room_by_ser_no,set_room_stbtype_no
logger=logging.getLogger(__name__)

class BoxHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('ktvbox.html')

    @gen.coroutine
    def post(self):
       img_url=self.get_argument('imgurl')
       logger.debug("有反应");
       _res = {}
       _res['code'] = 0
       _res['msg'] = "修改成功！"
       _res['data'] = img_url
       self.send_json(_res)

class SettingHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('boxset.html')
    @gen.coroutine
    def post(self):
        img_url=self.get_argument('imgurl')
        mtype=self.get_argument('type')
        if   mtype=="1":
            starttime=int(time.time())
            option=json.loads(img_url)['option']
            boxip=json.loads(img_url)['boxip']
            filename=json.loads(img_url)['name']
            
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            
            #需要去检查ip地址是否存在
            
            serial=boxip['ipaddress'].split('.')[3]
            if is_a_nect(boxip['ipaddress'])==1:
                _res['code'] = 1
                _res['msg'] = "机顶盒ip与服务器不是同一个网段！"
                self.send_json(_res)
                return
            #需要知道当前的是修改过还是添加
            starttime1=int(time.time())
            print('xxxxxxxxxxx',starttime1-starttime)
            for tname in filename:
                if boxip['Room_Old_SerialNo']!=serial and get_no_by_ini(boxip['ipaddress'],tname)==1:
                    _res['code'] = 1
                    _res['msg'] = "有相同的房台编号！"
                    self.send_json(_res)
                    return
                tname=str_val+tname+".ini"
#                 updata_setip_ini(tname,boxip['ipaddress'],boxip['subnetmask'],boxip['serviceip'],boxip['devicetype'],boxip['iprecond'],boxip['name'])
#                 remove_set_ini(tname,"PROSET")
#                 update_set_ini(tname,option)
                args={}
                args['ipaddress']=boxip['ipaddress']
                args['subnetmask']=boxip['subnetmask']
                args['serviceip']=boxip['serviceip']
                args['devicetype']=boxip['devicetype']
                args['iprecond']=boxip['iprecond']
                args['name']=boxip['name']
                
                remove_update_ini(tname,"PROSET",option,args)
                #如果没有房台，添加房台，如果有房台，就修改房台
                if boxip['Room_Old_SerialNo']=="":
                    jsondata={}
                    jsondata['Room_SerialNo']=serial
                    jsondata['Room_IpAddress']=boxip['ipaddress']
                    jsondata['Room_STBtype']=boxip['devicetype']
                    jsondata['Room_OrderType']=boxip['Room_OrderType']
                    jsondata['Room_MAC1']=boxip['Room_MAC1']
                    jsondata['Room_Name']=serial
                    mflag=add_rooms_by_progress(jsondata)
#                     print "mnm"+str(mflag)
                    if mflag>=0:
                        flag=add_new_skin(mflag,serial,boxip['skin_theme_id'],boxip['skin_name'])
                        sp_roomktvservermapping()
                else:
                    jsondata={}
                    jsondata['Room_ID']=boxip['Room_ID']
                    jsondata['Room_Old_SerialNo']=boxip['Room_Old_SerialNo']
                    jsondata['Room_Old_IpAddress']=boxip['Room_Old_IpAddress']
                    jsondata['Room_SerialNo']=serial
                    jsondata['Room_IpAddress']=boxip['ipaddress']
                    jsondata['Room_STBtype']=boxip['devicetype']
                    jsondata['Room_OrderType']=boxip['Room_OrderType']
                    jsondata['skin_theme_id']=boxip['skin_theme_id']
                    jsondata['skin_name']=boxip['skin_name']
                    jsondata['Room_MAC1']=boxip['Room_MAC1']
                    jsondata['Room_Name']=serial
                    one_motify_rooms(jsondata)
                    updata_new_skin(jsondata)
                    sp_roomktvservermapping()
#             sp_AutoMac()
            #盒子文件同步
#             set_stb_syscn()
            #同步单个文件
            starttime2=int(time.time())
            print('xxxxxxx2xxxx',starttime2-starttime)
            for tname in filename:
                set_stb_syscn_by_file(tname)
            starttime3=int(time.time())
            print('xxxxx3xxxxxx',starttime3-starttime)
            self.send_json(_res)
            
        #批量设置程序 
        elif mtype=="8":
            option=json.loads(img_url)['option']
            boxip=json.loads(img_url)['boxip']
            
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            if is_a_nect(boxip['ipaddress'])==1:
                _res['code'] = 1
                _res['msg'] = "机顶盒ip与服务器不是同一个网段！"
                self.send_json(_res)
                return
            try:
            #需要删除所有的房间
                if get_all_rooms_info()!=None:
                    for room in get_all_rooms_info():
                        one_delete_room(room['Room_SerialNo'])
                #删除menpai
                delete_menpaiall()
            except:
                pass
            
            #找到所有的配置文件
            stbstart=boxip['stbstart']
            for filename in glob.glob(str_val+"*.ini"):
                conjson={}
                #初始化 文件中加节点
#                 update_init_ini(filename)
                #删除的时候去添加
                remove_set_ini(filename,"PROSET")
                #设置信息
                updata_setip_ini(filename,boxip['ipaddress']+str(stbstart),boxip['subnetmask'],boxip['serviceip'],boxip['devicetype'],boxip['iprecond'],str(stbstart))
                
                update_set_ini(filename,option)
                
                if get_part_info_no(str(stbstart))==None:
                    jsondata={}
                    jsondata['Room_SerialNo']=str(stbstart)
                    jsondata['Room_IpAddress']=boxip['ipaddress']+str(stbstart)
                    jsondata['Room_STBtype']=boxip['devicetype']
                    jsondata['Room_OrderType']=boxip['Room_OrderType']
                    jsondata['Room_Name']=str(stbstart)
                    mflag=add_rooms_by_progress(jsondata)
                    print "mnm"+str(mflag)
                    if mflag>=0:
                        flag=add_new_skin(mflag,str(stbstart),boxip['skin_theme_id'],boxip['skin_name'])
                        
                else:
                    jsondata={}
                    jsondata['Room_ID']=str(stbstart)
                    jsondata['Room_Old_SerialNo']=stbstart
                    jsondata['Room_Old_IpAddress']=boxip['ipaddress']+str(stbstart)
                    jsondata['Room_SerialNo']=str(stbstart)
                    jsondata['Room_IpAddress']=boxip['ipaddress']+str(stbstart)
                    jsondata['Room_STBtype']=boxip['devicetype']
                    jsondata['Room_OrderType']=boxip['Room_OrderType']
                    jsondata['skin_theme_id']=boxip['skin_theme_id']
                    jsondata['skin_name']=boxip['skin_name']
                    jsondata['Room_MAC1']='0'
                    jsondata['Room_Name']=stbstart
                    print jsondata
                    one_motify_rooms(jsondata)
                    updata_new_skin(jsondata)
                    
                stbstart=int(stbstart)+1;
            sp_roomktvservermapping()
            sp_AutoMac()
            set_stb_syscn()
            self.send_json(_res)

        elif mtype=="3":
#             filename=json.loads(img_url)['name'].strip()
            infojson={}
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            config_val = cf.get("sec_a", "configpath")
            isfiles=self.get_argument('isfiles')
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            config_val = cf.get("sec_a", "configpath")
            fullname="orm/default.ini"
            #需要复制一份
#             copyfile(config_val,fullname)
            
            infojson['boxip']=get_all_set_list_ini(fullname)
            infojson['option']=get_all_config_ini(config_val)
            infojson['boxtype']=get_box_type_ini()
            self.send_json(infojson)

        elif mtype=="4":
            infojson={}
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            config_val = cf.get("sec_a", "configpath")
            infojson['option']=get_all_config_ini(config_val)
            self.send_json(infojson)

        elif mtype=="5":
            option=json.loads(img_url)
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            config_val = cf.get("sec_a", "configpath")
            updata_config_ini(config_val,option)
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            self.send_json(_res)

        elif mtype=="6":
            option=json.loads(img_url)
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            config_val = cf.get("sec_a", "configpath")
            add_config_ini(config_val,option)
            _res = {}
            _res['code'] = 0
            _res['msg'] = "添加成功！"
            self.send_json(_res)

        elif mtype=="7":
            option=json.loads(img_url)
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            config_val = cf.get("sec_a", "configpath")
            delete_config_ini(config_val,option)
            _res = {}
            _res['code'] = 0
            _res['msg'] = "删除成功！"
            self.send_json(_res)
            
        #批量可选设置 就是对公共的一些配置进行设置
        elif mtype=="9":
            option=json.loads(img_url)['option']
            boxip=json.loads(img_url)['boxip']
            filenamearr=self.get_argument('filename')
            filename=json.loads(filenamearr)
            #需要单独的去
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            if is_a_nect(boxip['ipaddress'])==1:
                _res['code'] = 1
                _res['msg'] = "机顶盒ip与服务器不是同一个网段！"
                self.send_json(_res)
                return
            arrlocalip=[]
            stbstart=boxip['stbstart']
            #不如取修补更改
            arrmac=[]
            for item in filename:
                macname=item['mac']
                arrmac.append(macname)
            print arrmac
            for loaclfilename in glob.glob(str_val+"*.ini"):
                #需要机顶盒里面有这个ip地址的，这是盒子里面
                #这个地方错了
                aafilename=os.path.basename(loaclfilename).split('.ini')[0]
                if not aafilename in arrmac:
                    localip=find_stbip_name(loaclfilename)
                    if localip:
                        try:
                            myno=localip.split('.')[3]
                        except:
                            myno=0
                        if myno:
                            print myno
                            arrlocalip.append(str(myno))
                    
            #当本地盒子的ip地址和上传时候含有的时候      这个时候就可以按这些去设置   
            locali=0
            canroombuilt=[]
            for item in filename:
                #第一步需要拿出filename
                macname=item['mac']
                #在数据库里面的编号
                no=item['no']
                #首先需要知道在
                
                if not str(int(stbstart)+locali) in arrlocalip:
                    #如果里面没有就可以进行正常的添加
                    #1,删除数据里房台的信息
                    print 'xsxx',int(stbstart)+locali
                    one_delete_room(str(int(stbstart)+locali))
                    canroombuilt.append(int(stbstart)+locali)
                    locali=locali+1
                else:
                    while True:
                        locali=int(locali)+1
                        print 'xxx',int(stbstart)+locali
                        if not str(int(stbstart)+locali) in arrlocalip:
                            one_delete_room(str(int(stbstart)+locali))
                            canroombuilt.append(int(stbstart)+locali)
                            locali=int(locali)+1
                            break
            #找到所有的配置文件
            
#             for filename in glob.glob(str_val+"*.ini"):
            for afilename in arrmac:
                filename=str_val+afilename+".ini"
                #取出一个参数

                stbstart=canroombuilt.pop()
                if not stbstart:
                    break
                print "stbstart",stbstart
                conjson={}
                #初始化 文件中加节点
#                 update_init_ini(filename)
                #删除的时候去添加
                remove_set_ini(filename,"PROSET")
                #设置信息
                updata_setip_ini(filename,boxip['ipaddress']+str(stbstart),boxip['subnetmask'],boxip['serviceip'],boxip['devicetype'],boxip['iprecond'],str(stbstart))
                
                update_set_ini(filename,option)
                
                if get_part_info_no(str(stbstart))==None:
                    jsondata={}
                    jsondata['Room_SerialNo']=str(stbstart)
                    jsondata['Room_IpAddress']=boxip['ipaddress']+str(stbstart)
                    jsondata['Room_STBtype']=boxip['devicetype']
                    jsondata['Room_OrderType']=boxip['Room_OrderType']
                    jsondata['Room_Name']=str(stbstart)
                    mflag=add_rooms_by_progress(jsondata)
                    print "mnm"+str(mflag)
                    if mflag>=0:
                        flag=add_new_skin(mflag,str(stbstart),boxip['skin_theme_id'],boxip['skin_name'])
                        
                else:
                    jsondata={}
                    jsondata['Room_ID']=str(stbstart)
                    jsondata['Room_Old_SerialNo']=stbstart
                    jsondata['Room_Old_IpAddress']=boxip['ipaddress']+str(stbstart)
                    jsondata['Room_SerialNo']=str(stbstart)
                    jsondata['Room_IpAddress']=boxip['ipaddress']+str(stbstart)
                    jsondata['Room_STBtype']=boxip['devicetype']
                    jsondata['Room_OrderType']=boxip['Room_OrderType']
                    jsondata['skin_theme_id']=boxip['skin_theme_id']
                    jsondata['skin_name']=boxip['skin_name']
                    jsondata['Room_MAC1']='0'
                    jsondata['Room_Name']=stbstart
                    print jsondata
                    one_motify_rooms(jsondata)
                    updata_new_skin(jsondata)
                    
#                 stbstart=int(stbstart)+1;
            sp_roomktvservermapping()
            sp_AutoMac()
            for tname in arrmac:
                set_stb_syscn_by_file(tname)
                print ("amac",tname)            
#             set_stb_syscn()
            self.send_json(_res)
            #需要更新数据库和ini文件
        elif mtype=="10":
            option=json.loads(img_url)['option']
            boxip=json.loads(img_url)['boxip']
            filenamearr=self.get_argument('filename')
            filename=json.loads(filenamearr)
            #需要单独的去
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"

            #不如取修补更改
#             arrmac=[]
#             for item in filename:
#                 macname=item['mac']
#                 arrmac.append(macname)
#             print arrmac
            #当本地盒子的ip地址和上传时候含有的时候      这个时候就可以按这些去设置
            print 'filename',filename   
            for item in filename:
                amac=item['mac']
                tempfilename=str_val+amac+".ini"
                #删除的时候去添加
                remove_set_ini(tempfilename,"PROSET")
                #设置信息 更新ini文件的设置
                updata_setsome_ini(tempfilename,boxip['subnetmask'],boxip['serviceip'],boxip['devicetype'],boxip['iprecond'])
                update_set_ini(tempfilename,option)
                #需要设置含有皮肤的 需要知道含有皮肤的房台
                #需要查询是否含有该皮肤  boxip['skin_theme_id'] boxip['skin_name']
#                 updata_new_skin(jsondata) #查询出room_id号
                room_no=item['no'] #查出是否有房台编号
                if find_room_by_ser_no(room_no):
                    obj={}
                    obj['Room_SerialNo']=room_no
                    obj['Room_Old_SerialNo']=room_no
                    obj['skin_theme_id']=boxip['skin_theme_id']
                    obj['skin_name']=boxip['skin_name']
                    updata_new_skin(obj)
                    set_room_stbtype_no(room_no,boxip['devicetype'])
                set_stb_syscn_by_file(amac)
                print ("xxxxxxxxxxxxxxxxxxamacxxxxxxxxxxxxxxxx",amac)
#             set_stb_syscn()
            self.send_json(_res)


        else:
            starttime=int(time.time())
            filename=json.loads(img_url)['name'].strip()
            print filename
            infojson={}
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            sections = cf.sections()
            options = cf.options("sec_a")
            str_val = cf.get("sec_a", "boxpath")
            config_val = cf.get("sec_a", "configpath")
            fullname=str_val+filename+".ini"
            print "fullname",fullname
            infojson['boxip']=get_all_set_list_ini(fullname)
            print infojson['boxip']
            infojson['option']=get_all_config_ini(config_val)
            infojson['boxtype']=get_box_type_ini()
            endtime=int(time.time())
            print ("time cha",endtime-starttime)
            self.send_json(infojson)










