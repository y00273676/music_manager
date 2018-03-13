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
import tornado
import json
import re
import ConfigParser
import glob


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int

from control.skins import get_all_skins
from control.rooms import get_all_rooms_info, get_part_info_no,get_part_info_ip,\
        add_part_info,add_rooms_by_progress,upata_part_info,delete_room,\
        one_delete_room,one_motify_rooms,\
        get_rooms, flush_rooms
from control.rooms import get_room_bymac, get_dhcp_options, update_room, del_room
from control.servers import get_all_servers



from control.skin import get_all_skin_info, get_part_skin_info, add_new_skin,\
        updata_new_skin, delete_skin

from control.configs import get_all_config
from control.boxs import *
from control.modbc import comp_by_ip
from control.serverutils import *
logger=logging.getLogger(__name__)

class RoomsHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        _res = dict(code=0, msg='ok', result=None)
        if op == 'list':
            ret = get_rooms()
            if isinstance(ret, dict):
                _res['result'] = ret
            else:
                _res['code'] = 1
                _res['msg'] = "无法获得房台信息"

            self.send_json(_res)
            return
        elif op == 'get':
            room_mac = self.get_argument('room_mac', '')
            if room_mac == '':
                _res['code'] = 1
                _res['msg'] = '参数无效'
            _res['result'] = get_room_bymac(room_mac)
            self.send_json(_res)
            return
        elif op == 'setting':
            room_mac = self.get_argument('room_mac', '')
            if room_mac == '':
                _res['code'] = 1
                _res['msg'] = '参数无效'
            result = {}
            result['option'] = get_dhcp_options()
            roominfo = get_room_bymac(room_mac)
            if not roominfo:
                roominfo = {}
                roominfo['room_mac'] = room_mac
                roominfo['room_name'] = ''
                roominfo['room_no'] = ''
                roominfo['room_ip'] = ''
                roominfo['room_gw'] = ''
                roominfo['room_mask'] = ''
                roominfo['room_dns'] = ''
                roominfo['room_svr'] = ''
                roominfo['room_recordsvr'] = ''
                roominfo['room_skin'] = 0
                roominfo['room_theme'] = 0
            result['roominfo'] = roominfo
            result['config'] = get_all_config()
            skins = get_all_skins()
            if isinstance(skins, dict):
                result['skins'] = skins['matches']
            else:
                result['skins'] = []
            servers = get_all_servers()
            if isinstance(servers, dict):
                result['servers'] = servers['matches']
            else:
                result['servers'] = []
            _res['result'] = result
            self.send_json(_res)
            return
        else:
            raise tornado.web.HTTPError(405)
            #self.render('fangtaiset.html')

    @gen.coroutine
    def post(self, op):
        if op == 'update':
            '''
            保存单个Room信息
            {"boxip":{"ipaddress":"192.168.122.210","subnetmask":"255.255.255.0","serviceip":"192.168.122.201","name":"210","devicetype":"0","iprecond":"","skin_name":"90后V2","Room_MAC1":"","Room_ID":"","Room_Old_IpAddress":"192.168.122.210","Room_Old_SerialNo":"","Room_OrderType":1,"skin_theme_id":1},"option":[{"appvalue":"debugenable","optionvalue":""},{"appvalue":"use_tpanel","optionvalue":"elotouch"}],"name":["52540073585b"]}
            '''
            _res = dict(code=0, msg='保存成功！', result=None)
            roominfo = json.loads(self.request.body)
            starttime = int(time.time())
            ret = update_room(roominfo)
            if ret:
                pass
            else:
                _res['code'] = 1
                _res['msg'] = "保存失败,请确认信息填写完整并没有重复的IP地址!"

            self.send_json(_res)
            return
        elif op == 'del':
            _res = dict(code=0, msg='删除成功！', result=None)
            room_mac = self.get_argument('room_mac', '')
            if not room_mac:
                _res['code'] = 1
                _res['msg'] = '无效的参数!'
            ret = del_room(room_mac)
            if ret:
                pass
            else:
                _res['code'] = 1
                _res['msg'] = "删除失败!"

            self.send_json(_res)
            return
        elif op == 'flush':
            '''
            操作多个服务器
            同步数据库中的房台信息,到每台服务器上去.拟用于多服务器操作(要考虑Python的单线程问题)
            '''
            _res = dict(code=0, msg='同步房台配置信息成功！', result=None)
            _res['result'] = flush_rooms()
            self.send_json(_res)
            return
        elif op == 'sync':
            '''
            操作单个服务器
            同步数据库中的房台信息到本地.
            '''
            _res = dict(code=0, msg='刷新房台配置信息成功！', result=None)
            _res['msg'] = 'not implement yet'
            self.send_json(_res)
            return
        else:
            raise tornado.web.HTTPError(405)

