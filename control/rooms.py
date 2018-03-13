#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-25 14:37:28
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import ConfigParser
import glob
import chardet
import codecs
import logging
import json

from lib import http
from orm import orm as _mysql
from lib.iniconfig import IniConfig

from control.fileservers import sp_addroom
from control.fileservers import sp_delete_room
from control.fileservers import sp_modifyroom
from control.boxs import find_stb_name
from setting import DHCP_CONFIG_PATH

logger=logging.getLogger(__name__)

def get_all_rooms_info():
    res = _mysql.rooms.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def get_men_pai_info():
    res = _mysql.rooms.get_menpai_room('1')
    if isinstance(res, list) and len(res) > 0:
        return res
    return []

def find_id_info():
    res = _mysql.rooms.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def get_part_info_no(serialno):
    res = _mysql.rooms.get_part_room(serialno)
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def get_part_info_ip(ip):
    res = _mysql.rooms.get_part_room_ip(ip)
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def add_part_info(jsondata):
    params = {}
    num=0
    for mid in find_id_info():
        if num<mid['Room_ID']:
            num=mid['Room_ID']
    print "num======"+str(num)
    params['Room_SerialNo'] =  int(jsondata['Room_SerialNo'])
    params['Room_ID'] =  int(num+1)
    params['Room_IpAddress'] =  jsondata['Room_IpAddress']
    params['Room_OrderType'] =  int(jsondata['Room_OrderType'])
    params['Room_Name'] =  jsondata['Room_Name']
    params['Room_Class_ID'] = 1

    skin_id = _mysql.rooms.add(params)
    if skin_id and skin_id > 0:
        return num
    else:
        return -1

def add_rooms_by_progress(jsondata):
    # @IsOrNo_SaveBill int=0,--房台的机顶盒是否存单标志（0不存单，1存单）
    # @FullNum int=0 ,    --额定人数
    # @strFloor varchar(20)='',   --所属楼成
    # @Room_MAC1 int = 0,     --麦克风频道1
    # @Room_STBtype int = 0   --机顶盒类型 0 包房机顶盒； 1 门牌机
    params = {}
    num=1
    if find_id_info()!=None:
        for mid in find_id_info():
            if num<mid['Room_ID']:
                num=mid['Room_ID']

    params['room_serialno'] =  int(jsondata['Room_SerialNo'])
    params['room_id'] =  int(num+1)
    params['room_ipaddress'] =  jsondata['Room_IpAddress']
    params['mediaordertype'] =  int(jsondata['Room_OrderType'])
    params['room_name'] =  jsondata['Room_Name']
    params['room_class'] = 1
    params['room_description'] = ""

    params['IsOrNo_SaveBill'] = 0
    params['FullNum'] = 0
    params['strFloor'] = ""
    params['Room_STBtype'] = jsondata['Room_STBtype']
    params['Room_MAC1'] = 0


    params['room_class_name'] = "KTV"
    params['manufactory_id'] = 1
    params['manufactory_name'] = "一楼"


    params['room_PriceGroup_Name'] = ""
    params['discount'] = ""


    return sp_addroom(params)

def upata_part_info(jsondata):
    params = {}
    params['Room_SerialNo'] =  int(jsondata['Room_SerialNo'])
    params['Room_IpAddress'] =  jsondata['Room_IpAddress']
    params['Room_OrderType'] =  int(jsondata['Room_OrderType'])
    params['Room_Name'] =  jsondata['Room_Name']

    ret=_mysql.rooms.updata(int(jsondata['Room_SerialNo']),params)

    return ret

def delete_room(room_num):
    ret=_mysql.rooms.delete(room_num)
    return ret

def one_delete_room(room_num):
    params = {}
    params['room_id']=""
    params['room_serialno']=room_num
    params['room_ipaddress']=""
    return sp_delete_room(params)

def one_motify_rooms(jsondata):

    params = {}
    params['room_id'] =  jsondata['Room_ID']
    params['room_serialno'] =  int(jsondata['Room_Old_SerialNo'])
    params['room_newserialno'] =  int(jsondata['Room_SerialNo'])
    params['room_ipaddress'] =  jsondata['Room_Old_IpAddress']
    params['room_newipaddress'] =  jsondata['Room_IpAddress']
    params['mediaordertype'] =  int(jsondata['Room_OrderType'])
    params['room_name'] =  jsondata['Room_Name']
    params['Room_Old_SerialNo'] =  jsondata['Room_Old_SerialNo']


    params['room_class'] = 1
    params['room_description'] = ""

    params['IsOrNo_SaveBill'] = 0
    params['FullNum'] = 0
    params['strFloor'] = ""
    params['Room_STBtype'] = jsondata['Room_STBtype']
    params['Room_MAC1'] = jsondata['Room_MAC1']


    params['room_class_name'] = "KTV"
    params['manufactory_id'] = 1
    params['manufactory_name'] = "一楼"

    params['discount'] = "一楼"
    params['room_PriceGroup_Name'] = ""
    params['discount'] = ""
    params['RoomClassBranchName'] = ""

    return sp_modifyroom(params)
#查询是否有相同的ip地址

def get_no_by_ini(seilno,macname):
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_val = cf.get("sec_a", "boxpath")
    for filename in glob.glob(str_val+"*.ini"):
        if not macname in filename:
            if seilno==find_stb_name(filename):
                return 1
    return 0

def add_room(rinfo):
    '''
    更新房台信息
    '''
    return _mysql.rooms.add(rinfo)


def update_room(rinfo):
    '''
    更新房台信息
    '''

    room_mac = rinfo['room_mac']
    exists = _mysql.rooms.room_exists(room_mac)
    if exists:
        ret = _mysql.rooms.update(rinfo)
    else:
        ret = _mysql.rooms.add(rinfo)
    sync_room_config(room_mac)
    return ret

def del_room(mac):
    '''
    更新房台信息
    '''
    ret = _mysql.rooms.delete(mac)
    try:
        ini_path = os.path.join(DHCP_CONFIG_PATH,'STBs/%s.ini' % mac)
        if os.path.exists(ini_path):
            os.remove(ini_path)
    except Exception as ex:
        logger.error(str(ex))
    #TODO: still need to delete ini file
    return ret

def get_rooms():
    local_list = get_local_rooms()
    ret = _mysql.rooms.get_all()
    if isinstance(ret, list):
        for room in ret:
            if room['room_mac'] in local_list.keys():
                local_list.pop(room['room_mac'])
        for room in local_list.keys():
            ret.insert(0, local_list[room])

    else:
        ret = []
        for room in local_list.keys():
            ret.insert(0, local_list[room])
    return dict(matches=ret, total=len(ret))

def get_room_bymac(mac):
    ret = _mysql.rooms.get_by_mac(mac)
    if isinstance(ret, list) and len(ret) > 0:
        return ret[0]
    else:
        return None

def get_dhcp_options():
    item=[]
    configini = os.path.join(DHCP_CONFIG_PATH, 'Config.ini')
    cf = open(configini, "r")
    data = cf.read()
    f = codecs.open(configini, "r", chardet.detect(data)['encoding'])
    while True:
        line = f.readline()
        if line:
            line=line.strip()
            if(line.strip() == '[ITEM]'):
                datajson={}
                item.append(datajson)
            else:
                key_val = line.split("=")
                if(len(key_val)>1):
                    datajson[key_val[0]]=key_val[1]
                else:
                    datajson["select"]=key_val[0]
        else:
            break
    f.close()
    return item

def get_local_rooms(filters=[]):
    local_list = {}
    for filename in glob.glob(os.path.join(DHCP_CONFIG_PATH, "STBs/*.ini")):
        _, fname = os.path.split(filename)
        fname, _ = os.path.splitext(fname)
        match = False
        if len(filters) > 0:
            for itm in filters:
                if filename.startswith(item):
                    match = True
        else:
            match = True

        if match:
            roominfo = {}
            roominfo['room_mac'] = fname 
            roominfo['room_no'] = ''
            roominfo['room_name'] = ''
            roominfo['room_ip'] = ''
            roominfo['room_dns'] = ''
            roominfo['room_gw'] = ''
            roominfo['room_mask'] = ''
            roominfo['room_svr'] = ''
            roominfo['room_recordsvr'] = ''
            roominfo['room_recordsvr'] = ''
            roominfo['room_skin'] = 0
            roominfo['room_theme'] = 0
            roominfo['room_profile'] = ''
        local_list[fname] = roominfo
    return local_list

def sync_room_config(room_mac):
    ret = _mysql.rooms.get_by_mac(room_mac)
    if isinstance(ret, list) and len(ret) > 0:
        roominfo = ret[0]
    else:
        roominfo = None

    if not roominfo:
        return False
    return update_dhcp_ini(room_mac, roominfo)
 
def flush_rooms():
    '''
    从数据库中重新Flush出房台信息.
    操作分两步:
    1. 删除所有房台的Ini文件
    2. 查询数据库,把查询到的房台写入各自的Ini文件中.

    长期考虑,推荐废除Ini文件,只采用数据库信息为准(DHCP服务器)
    '''
    os.system("rm -f %s" % os.path.join(DHCP_CONFIG_PATH,'STBs/*.ini'))
    flush_list = []
    ret = _mysql.rooms.get_all()
    if isinstance(ret, list):
        for roominfo in ret:
            room_mac = roominfo['room_mac']
            update_dhcp_ini(room_mac, roominfo)
            flush_list.append(room_mac)
    return flush_list

def update_dhcp_ini(room_mac, roominfo):
    ini_path = os.path.join(DHCP_CONFIG_PATH,'STBs/%s.ini' % room_mac)
    if os.path.exists(ini_path):
        os.remove(ini_path)
    cf = IniConfig()
    #默认信息:
    if not cf.has_section('STB'):
        cf.add_section('STB')
    cf.set("STB", "CLIENTTYPE", 0)
    cf.set("STB", "DYNCONFIG",0)
    cf.set("STB", "SCREENMODE",1)
    cf.set("STB", "VGARES",1)
    cf.set("STB", "TVMODE",1)
    cf.set("STB", "OtherSettings","")
    cf.set("STB", "BootFile","pxelinux.0")
    cf.set("STB", "DefaultRouter","")
    cf.set("STB", "DomainName","")
    cf.set("STB", "STBType",0)
    cf.set("STB", "VGATYPE", "")

    #基本信息
    cf.set("STB", "IP", roominfo['room_ip'])
    cf.set("STB", "MAC", room_mac)
    cf.set("STB", "NMASK", roominfo['room_mask'])
    cf.set("STB", "SERVER", roominfo['room_svr'])
    cf.set("STB", "STBType", 1)
    cf.set("STB", "RecordSvr",  roominfo['room_recordsvr'])
    cf.set("STB", "Name", roominfo['room_name'])

    if not cf.has_section('PROSET'):
        cf.add_section('PROSET')
    try:
        options = json.loads(roominfo['room_profile'])
    except Exception as ex:
        logger.error(str(ex))
        options = []
    for op in options:
        cf.set("PROSET", op['appvalue'], op['optionvalue'])

    cf.write(open(ini_path, "w"))
    return True

