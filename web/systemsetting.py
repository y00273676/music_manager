#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-20 10:34:31
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


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int

from control.systemsetting import *
from control.servergroups import *

from control.fileservers import *

from control.readthunder import get_main_thunder_info

from control.serverutils import lsService
from control.serverutils import restartService
from control.serverutils import stopService

from control.theme import get_all_theme_info
from control.serverinfo import get_server_info

from control.postthunder import postHttp
from control.getlocalip import getLocalIp
from control.checkchange import check_change_version_code
from control.checkchange import read_thunder_ini_to_db
from control.checkchange import get_thunder_ini_db
from control.fileservers import sp_findthunder_ini
from control.theme import get_theme_package
from control.readthunder import read_all_info
from control.readthunder import set_other_ip_thunder
from control.karaokversion import *
from control.boxs import *
from tsjob.cloudlogin import CloudLoginTask
from orm.mm import deleteAllData




logger=logging.getLogger(__name__)


class SystemSetHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('systemset.html')

    @gen.coroutine
    def post(self):
        mtype=self.get_argument('type')

        _strcode="utf8"
        cf = ConfigParser.ConfigParser()
        cf.read('path.ini')
        str_val = cf.get("sec_a", "systemparh")
        _res = {}
        _res['code'] = 0
        _res['msg'] = "修改成功！"

        if  mtype=="1":
            #保存系统设置
            mdata = self.get_argument('mdata')
            mchangetype = self.get_argument('changetype')
            
            if(mchangetype == "sure"):
                mjsondata = json.loads(mdata)
                misc = mjsondata['misc']
#                 mainserver = mjsondata['mainserver']
                erpserver = mjsondata['erpserver']
#                 erp=mjsondata['erp']
#                 ktv=mjsondata['ktv']
                cloudset = mjsondata['cloudset']
                cloudmusic = mjsondata['cloudlogin']

                try:
                    set_erpserver(str_val,erpserver,_strcode)
                    set_misc(str_val,misc,_strcode)
#                     set_ktv(str_val,ktv,_strcode)
                    up_cloud_setting(cloudset)
                    up_cloudmusic_setting(cloudmusic)
                    allip=find_all_servers_ip()
                    print allip
                    jsondata={}
                    for ip in allip:
                        if ip==getLocalIp("eth0"):
                            pass
                        else:
                            state=postHttp(ip,mjsondata,"0")
                            if state!=0:
                                print ip+"修改失败"
                    
                    mresult=1
                    tminfo=read_all_info()
                    mainserver=tminfo['mainserver']
                    if getLocalIp("eth0")==mainserver['DataBaseServerIp']:
                        mresult=read_thunder_ini_to_db()
                    _res['result']=mresult
                    _res['msg'] = "设置成功！"
                    if 'loginpassword' in cloudmusic.keys() and cloudmusic['loginpassword']:
                        CloudLoginTask.get_auth_info()
                        _bres, _msg = CloudLoginTask.cloud_login_msg()
                        if _bres:
                            _res['msg'] += "云端帐号登录测试成功！"
                        else:
                            _res['msg'] += "云端帐号登录测试失败！云端消息：%s" % _msg
                except Exception as ex:
                    print traceback.format_exc()
                    _res['code'] = 1
                    _res['result']=1
                    _res['msg'] = "设置失败"
                
                #//分发数据
                
                #获取各个服务器ip
               

            self.send_json(_res)

        elif  mtype=="3":
            updatatype=self.get_argument('updatatype')
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)


            if updatatype=="addFristLevel":
                mid= add_server_groups(mjsondata)
                infojson={}
                infojson['result']="0"
                infojson['groupid']=mid
                infojson['groupservers']=find_file_servers()
                infojson['servergroups']=find_server_groups()
                self.send_json(infojson)
            elif updatatype=="updataFristLevel":
                result=updata_server_groups(mjsondata['ServerGroup_ID'],mjsondata)
                infojson={}
                infojson['result']=result
                self.send_json(infojson)
            elif updatatype== 'deleteFristLevel':
                result=delete_server_groups_id(mjsondata['ServerGroup_ID'])
                
                infojson={}
                infojson['result']=result
                self.send_json(infojson)
            elif updatatype=='addSecondLevel':
                mn = sp_addfileserver(name=mjsondata['name'],ipaddress=mjsondata['ipaddress'], os=mjsondata['os'], isvalid=mjsondata['isvalid'], group_id=mjsondata['group_id'], group_name=mjsondata['group_name'] ,ismain=mjsondata['ismain'])
#                 mtjson={}
#                 mtjson['server_ip']=mjsondata['ipaddress']
#                 mtjson['server_type']="0"
#                 sp_add_systhunder(mtjson)
                infojson={}
                infojson['msg']='操作成功'
                try:
                    sp_roomktvservermapping()
                except:
                    infojson['msg']="设置服务器优先级出错！"
                if tongbu_file(mjsondata['ipaddress'])==1:
                    infojson['msg'] = ("添加成功，但"+mjsondata['ipaddress']+"网络异常，请查看是否配置或者是否连接")
                mresult=set_other_ip_thunder(mjsondata['ipaddress'])
                
#                 if mresult==1:
#                     infojson["msg"]="在同一个服务器下"
#                 elif mresult==0:
#                     infojson["msg"]="同步成功"
#                 else:
#                     infojson["msg"]="同步失败"
                
#                 infojson['msg']=is_allright_ip(mjsondata['ipaddress'])
                infojson['mtype']=str(mn)
                self.send_json(infojson)
            elif updatatype=="removeSecondLevel":
                ipaddress=mjsondata['ipaddress']
                print ipaddress
                if sp_check_by_address(ipaddress):
                    deleteAllData()
                infojson={}
                amn=sp_deletefileserver(rid='',ipaddress=ipaddress)
#                 sp_delete_synthunder(ipaddress)
                try:
                    sp_roomktvservermapping()
                except:
                    infojson['msg']="设置服务器优先级出错！"
                infojson['msg'] = "修改成功！"
                print "result:"+str(amn)
                infojson['mtype']=str(amn)
                infojson['result']="删除成功"
                self.send_json(infojson)
            elif updatatype=="updataSecondLevel":
                amn=sp_modifyfileserver(mjsondata)
                sp_roomktvservermapping()
                infojson={}
                print "result:"+str(amn)
                infojson['mtype']=str(amn)
                self.send_json(infojson)
            elif updatatype=="setmianlevel":
                amn=set_mian_group(mjsondata['ServerGroup_ID'])
                infojson={}
                infojson['mtype']=str(amn)
                infojson['result']="0"
                infojson['groupservers']=find_file_servers()
                infojson['servergroups']=find_server_groups()
                self.send_json(infojson)
            elif updatatype=="checkisonly":
                #检查是否为最后一台
                count=sp_check_only_fileserver(mjsondata['ServerGroup_ID'])
                infojson={}
                if count==1:
                    if sp_check_is_have_media(mjsondata['ServerGroup_ID']):
                        infojson['count']=count
                    else:
                        infojson['count']="2"
                else:
                    infojson['count']=count
                infojson['result']="0"
                self.send_json(infojson)
                

        elif mtype=="4":
            updatatype=self.get_argument('updatatype')
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            if updatatype=="find":
                infojson={}
                infojson['theme']=get_all_theme_info()
                infojson['localtheme']=get_theme_package()
                self.send_json(infojson)
            elif updatatype=="addtheme":
                mdata=self.get_argument('mdata')
                _res = {}
                if sp_find_theme_by_name(mjsondata['theme_name'])==0:
                    _res['code']="1"
                    _res['msg'] = "有重复皮肤！"
                else:
                    _res['code'] = sp_add_theme_con(mjsondata)
                    _res['msg'] = "添加成功！"
                
                self.send_json(_res)
            elif updatatype=="updatatheme":
                mdata=self.get_argument('mdata')
                _res = {}
                _res['code'] = sp_modify_theme_con(mjsondata)
                _res['msg'] = "修改成功！"
                self.send_json(_res)
            elif updatatype=="deletetheme":
                _res = {}
                _res['code'] = sp_delete_theme_con(mjsondata)
                _res['msg'] = "删除成功！"
                self.send_json(_res)
                pass
        elif mtype=="5":
            #获取服务器信息
            updatatype=self.get_argument('updatatype')
            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            #需要去调用获取服务的信息
            if updatatype=="ls":
                mjson={}
                mjson['server']=lsService()
                result=get_server_info(mjsondata['ip'])
                mjson['sbtinfo']={}
                if result!=1:
                    mjson['sbtinfo']=result
                _res = {}
                _res['msg']="获取成功"
                _res['code']=0
                _res['data']=mjson
                self.send_json(_res)
            
            elif updatatype=="restart":
                servierarr=['dbass','dhcp','recog','record','broadcast','video','stbmodule']
                serverjson={}
                serverjson['dbass']='KTV数据服务'
                serverjson['dhcp']='DHCP服务'
                serverjson['recog']='手写服务'
                serverjson['record']='录音服务'
                serverjson['broadcast']='广播服务'
                serverjson['video']='视频服务'
                serverjson['stbmodule']='模板同步服务'
                serverjson['mainktv']='加密狗服务'
                serverjson['twm']='数据管理服务'
                serverjson['search']='搜索服务'
                serverjson['transfer_vod']='微信点歌服务'
                serverjson['wx_ngrok']='微信点歌连接'
                
                _res = {}
                _res['msg']=''
                try:
                    for sign in mjsondata['name']:
                        if  restartService(sign)==0:
                            if _res['msg']=='':
                                _res['msg'] =serverjson[sign]+"操作成功！"
                            else:
                                _res['msg'] =_res['msg']+","+ serverjson[sign]+"操作成功！"
                        else:
                            
                            if _res['msg']=='':
                                _res['msg'] =serverjson[sign]+"操作失败！"
                            else:
                                _res['msg'] = _res['msg']+","+serverjson[sign]+"操作失败！"
                    
                   
                    
                except:
                    _res['msg'] = "启动失败！"
                _res['code'] = 0
                
                self.send_json(_res)
                
            elif updatatype=="stopserver":
                servierarr=['TD_DBAss','TD_DHCP','TD_RecogServer','TD_RecordServer','TD_Broadcast','TD_VideoServer']
                _res = {}
                _res['msg']=''
                for sign in mjsondata['name']:
                    if sign=="twm":
                        continue
                    if   stopService(sign)==0:
                        if _res['msg']=='':
                            _res['msg'] =sign+"停止服务成功！"
                        else:
                            _res['msg'] =_res['msg']+","+ sign+"停止服务成功！"
                    else:
                        
                        if _res['msg']=='':
                            _res['msg'] =sign+"停止失败！"
                        else:
                            _res['msg'] = _res['msg']+","+sign+"停止失败！"
                   
                _res['code'] = 0
                
                self.send_json(_res)
        elif mtype=="6":
            _res = {}
            _res['msg']="获取成功"
            _res['code']=check_change_version_code()
            self.send_json(_res)
            pass
        elif mtype=="7":
            #同步服务器
            _res = {}
            _res['code']="0"
            mmsg=tong_all_inianddata()
            if len(mmsg)==0:
                _res['msg']='只有一台服务器'
            else:
                _res['msg']=mmsg
            self.send_json(_res)
            pass

        else:
            print mtype
            #get systemset info
            cf = ConfigParser.ConfigParser()
            cf.read('path.ini')
            str_val = cf.get("sec_a", "systemparh")
            infojson={}
            add_defult_groups()
            
            infojson['systemsetting']=read_all_setting(str_val,_strcode)
            infojson['groupservers']=find_file_servers()
            infojson['servergroups']=find_server_groups()

            mtemp={}
            cloudmusic = {}
            try:
                for disco in find_data_setting():
                    if disco['SettingInfo_Name']=="中转服务器IP":
                        mtemp["centerinip"]=disco['SettingInfo_Value']
                    elif disco['SettingInfo_Name']=="中转服务器外网IP":
                        mtemp["centeroutip"]=disco['SettingInfo_Value']
                    elif disco['SettingInfo_Name']=="本地VPN域名":
                        mtemp["localname"]=disco['SettingInfo_Value']
                    elif disco['SettingInfo_Name']=="SSID":
                        mtemp["ssid"]=disco['SettingInfo_Value']
                    elif disco['SettingInfo_Name']=="SSID_Pwd":
                        mtemp["ssidpw"]=disco['SettingInfo_Value']
                    #for cloud music login info:
                    elif disco['SettingInfo_Name'] == "CloudMusic_uname":
                        cloudmusic["loginname"] = disco['SettingInfo_Value']
                    elif disco['SettingInfo_Name'] == "CloudMusic_passwd":
                        cloudmusic["loginpassword"] = disco['SettingInfo_Value']
                    elif disco['SettingInfo_Name'] == "CloudMusic_realdown":
                        cloudmusic["realdown"] = disco['SettingInfo_Value']
            except:
                pass
            


            infojson['cloudset']=mtemp
            infojson['karaokversion']=find_last_karaok_version()
            infojson['cloudlogin'] = cloudmusic
            print mtemp
            # sp_lookupktvservers(id='',ipaddress='')
            # sp_lookupfileservers(id='', ipaddress='', group_id='', group_name='')
#             get_thunder_ini_db()
            self.send_json(infojson)

