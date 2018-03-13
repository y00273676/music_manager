#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年4月27日

@author: baizhiyu
'''
from modules.model.common import *

class ktv_tvadinfo(StructLayout):
    struct_layout = [('ad_id', 'i'),('ad_bigurl', '256s'),('ad_smallurl', '256s'),('ad_bigx', 'i'),('ad_bigy', 'i'),('ad_smallx', 'i'),('ad_smally', 'i'),('ad_playtime', 'i'),('ad_showtime', 'i')]
    def __init__(self):
        self.ad_id=0
        self.ad_bigurl=''
        self.ad_smallurl=''
        self.ad_bigx=0
        self.ad_bigy=0
        self.ad_smallx=0
        self.ad_smally=0
        self.ad_playtime=0
        self.ad_showtime=0
        
class ktv_tvad_log(Serializable):
    def __init__(self):
        self.ad_id=0
        self.ad_name=''
        self.roomstatus=0
        self.roomip=''
        self.time=0
        
class ktv_tvad_count(Serializable):
    def __init__(self):
        self.ad_id=0
        self.ad_name=''
        self.roomstatus=0
        
        
        
        
        