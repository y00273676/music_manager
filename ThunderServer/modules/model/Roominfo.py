#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年4月6日

@author: yeyinlin
'''
from modules.model.common import *

class Roominfo(Serializable):
    def __init__(self):
        #房间的id
        self.roomid=0
        #房间的名称
        self.roomName=''
        #房间的ip地址
        self.ip=''
        #房间分类名
        self.room_className=''


'''
Created on 2017年4月10日

@author: baizhiyu
'''
class Intel_Device(StructLayout):
    struct_layout = [('intel_id', 'i'),('intel_name', '64s'),('intel_model', '16s'),('intel_desc', '512s'),('intel_logo', '256s')]
    def __init__(self):
        self.intel_id = 0
        self.intel_name = ''
        self.intel_model = ''
        self.intel_desc = ''
        self.intel_logo = ''
        
class Intel_DebugInfo(StructLayout):
    struct_layout = [('ktv_id', 'i'),('ktv_name', '64s'),('room_name', '16s'),('room_model', '16s'),('room_debug', 'i'),('room_update', 'i')]
    def __init__(self):
        self.ktv_id = 0
        self.ktv_name = ''
        self.room_name = ''
        self.room_model = ''
        self.room_debug = 0
        self.room_update = 0
        
class Intel_PlanList(StructLayout):
    struct_layout = [('plan_id', 'i'),('plan_name', '32s'),('plan_url', '256s'),('plan_public', 'i'),('plan_hot', 'i'),('plan_time', '32s'),('plan_usecount', 'i'),('plan_publicname', '32s'),('plan_hotname', '32s')]
    def __init__(self):
        self.plan_id = 0
        self.plan_name = ''
        self.plan_url = ''
        self.plan_public = 0
        self.plan_hot = 0
        self.plan_time = ''
        self.plan_usecount = 0
        self.plan_publicname = ''
        self.plan_hotname = ''
        
class Intel_PubPlanList(StructLayout):
    struct_layout = [('plan_id', 'i'),('plan_name', '32s'),('plan_url', '256s'),('plan_public', 'i'),('plan_hot', 'i'),('plan_time', '32s'),('plan_usecount', 'i'),('plan_publicname', '32s'),('plan_hotname', '32s'),('ktv_name', '64s'),('city_name', '16s')]
    def __init__(self):
        self.plan_id = 0
        self.plan_name = ''
        self.plan_url = ''
        self.plan_public = 0
        self.plan_hot = 0
        self.plan_time = ''
        self.plan_usecount = 0
        self.plan_publicname = ''
        self.plan_hotname = ''
        self.ktv_name = ''
        self.city_name = ''
        
class Intel_PlanKTV(StructLayout):
    struct_layout = [('ktv_id', 'i'),('ktv_name', '64s')]
    def __init__(self):
        self.ktv_id = 0
        self.ktv_name = ''
        
class Intel_RoomModel(StructLayout):
    struct_layout = [('room_id', 'i'),('room_name', '16s'),('room_area', '32s')]
    def __init__(self):
        self.room_id = 0
        self.room_name = ''
        self.room_area = ''
        
class Intel_City(StructLayout):
    struct_layout = [('city_id', 'i'),('city_name', '32s')]
    def __init__(self):
        self.city_id = 0
        self.city_name = ''
        
        
        
        
    
    
    
    