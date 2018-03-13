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


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int
from control.configures import get_all_config_info
from control.configures import update_setconfig
from control.theme import get_all_theme_info
from control.rooms import get_all_rooms_info
from control.systemsetting import find_data_setting
from control.systemsetting import update_systemset

logger=logging.getLogger(__name__)

class AndBoxHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('boxhome.html')


    @gen.coroutine
    def post(self):
        mtype=self.get_argument('type')

        logger.debug("有反应")
        print mtype

        if  mtype=="1":

            mdata=self.get_argument('mdata')
            mjsondata=json.loads(mdata)
            print mjsondata['Configure_Set17']
            set17=int(mjsondata['Configure_Set17'])
#             mark=int(mjsondata['Configure_IsMark'])
#             leadsong=int(mjsondata['Configure_IsLeadSong'])

            
            set23=int(mjsondata['Configure_Set23'])
            ordercontrol=int(mjsondata['Configure_OrderControl'])
            isspecial=int(mjsondata['Configure_IsSpecialEffect'])

            set51=mjsondata['Configure_Set51']
            set52=mjsondata['Configure_Set52']
            
            set58=mjsondata['Configure_Set58']
            set59=mjsondata['Configure_Set59']
            set60=mjsondata['Configure_Set60']
            splitinfo=set51.split(".",3)
            split51=splitinfo[0]+"."+splitinfo[1]+"."+splitinfo[2]+"."
            update_setconfig(1,set17,split51,set23,set52,ordercontrol,isspecial,set58,set59,set60)

            mdisco=mjsondata['DiscoControl']
#             usetime=mjsondata['UseTimePrompt']
            update_systemset("DiscoControl",mdisco)
            update_systemset("CanSong",ordercontrol)
#             update_systemset("UseTimePrompt",usetime)

            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            self.send_json(_res)

        else:
            infojson={}
            infojson['configures']=get_all_config_info()
            infojson['theme']=get_all_theme_info()
            mtdata=[]
            for disco in find_data_setting():
                if disco['SettingInfo_Name']=="DiscoControl":
                    mtdata.append(disco)
                elif disco['SettingInfo_Name']=="UseTimePrompt":
                    mtdata.append(disco)
            infojson['systemset']=mtdata


            print infojson
            self.send_json(infojson)




class FangTaiHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        print "mtype"
        self.render('fangtaiset.html')

    @gen.coroutine
    def post(self):
        mtype=self.get_argument('type')

        logger.debug("有反应")
        print mtype

        if  mtype=="1":
            _res = {}
            _res['code'] = 0
            _res['msg'] = "修改成功！"
            self.send_json(_res)

        else:
            infojson={}
            infojson['configures']=get_all_rooms_info()
            print infojson
            self.send_json(infojson)


