#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月17日

@author: yeyinlin
'''
from common.KtvInfo import KtvInfo
from config.appConfig import AppSet
from common.yhttp import yhttp
import json
import time
from modules.model.o2oad_action import *

import logging
logger = logging.getLogger(__name__)

class ktv_tvadinfoapi(object):
    _ins = None
    @staticmethod
    def Ins():
        if not ktv_tvadinfoapi._ins:
            ktv_tvadinfoapi._ins = ktv_tvadinfoapi()
        return ktv_tvadinfoapi._ins

    def __init__(self):
        self.ktvinfo = KtvInfo()._info

    #获取字幕
    def geto2oadcaption(self):
        url = '{0}/ad/caption/{1}'.format(AppSet().O2OAPI,self.ktvinfo.ktvid)
        #url = "http://api.stage.ktvsky.com/ad/caption/1";
        data = yhttp().get_y(url, 10)
        jsonres = json.loads(data)
        logger.debug("get o2o ad caption, url:%s result: %s" % ( url, jsonres))
        if "errcode" in jsonres and jsonres['errcode'] == 200:
            return jsonres
        return None
    
    def GetKtv_TvadinfoList(self):
        try:
            param = {}
            param['op'] = 'getktv_tvadinfolist'
            param['dogname'] = self.ktvinfo.ktvname
            param['time'] = str(int(time.time()))
            
            endurl = yhttp().ParamSign(param)
            
            url = "{0}/Ktv_tvadinfoService.aspx?".format(AppSet().songlist);
            url += endurl
            data = yhttp().get_y(url, 10)
            jsonres = json.loads(data)
            logger.debug("GetKtv_TvadinfoList: url:%s \nresult:%s\n" % (url, jsonres))
            if jsonres:
                if jsonres['code'] < 0:
                    return []
                if jsonres['result'] and len(jsonres['result']) > 0:
                    matches = jsonres['result']['matches']
                    return matches
        except Exception as e:
            logger.error(traceback.format_exc())
        return None
                  
    def GetKtv_tvadininterval(self):
        try:
            tvadininterval = 0
            param = {}
            param['op'] = 'getktv_tvadconf'
            param['ktvid'] = str(self.ktvinfo.ktvid)
            param['time'] = str(int(time.time()))
            endurl = yhttp().ParamSign(param)
            url = "{0}/Ktv_tvadinfoService.aspx?".format(AppSet().songlist);
            url += endurl
            data = yhttp().get_y(url, 10)
            jsonres = json.loads(data)
            logger.debug("GetKtv_tvadininterval: url:%s \nresult:%s\n" % (url, jsonres))
            if jsonres:
                if jsonres['code']<0:
                    return tvadininterval
                if jsonres['result'] and len(jsonres['result'])>0:
                    matches = jsonres['result']['matches']
                    return matches[0]['tvadininterval']
        except Exception as e:
            logger.error(traceback.format_exc())
        return None
            
    def GetOverdueKtv_tvadList(self):
        try:
            param = {}
            param['op'] = 'getoverduektv_tvadlist'
            param['dogname'] = self.ktvinfo.ktvname
            param['time'] = str(int(time.time()))
            endurl = yhttp().ParamSign(param)
            url = "{0}/Ktv_tvadinfoService.aspx?".format(AppSet().songlist);
            url += endurl
            data = yhttp().get_y(url, 10)
            jsonres = json.loads(data)
            logger.debug("GetOverdueKtv_tvadList: url:%s \nresult:%s\n" % (url, jsonres))
            if jsonres:
                if jsonres['code']<0:
                    return []
                if jsonres['result'] and len(jsonres['result'])>0:
                    matches = jsonres['result']['matches']
                    return matches
        except Exception as e:
            logger.error(traceback.format_exc())
            pass 
        return None
    
    def geto2oadinfolist(self):
        iurl = AppSet().O2OAPI1
        url = "{0}/ad/policy/{1}".format(iurl,str(self.ktvinfo.ktvid))
        data = yhttp().get_y(url, 10)
        jsonres = json.loads(data)
        logger.debug("geto2oadinfolist: url:%s \nresult:%s\n" % (url, jsonres))
        ad = o2oad()
        if jsonres and 'errcode' in jsonres and jsonres['errcode']==200:
            if "ad_pos" in jsonres.keys():
                ad_pos = jsonres['ad_pos']
                if "start" in ad_pos.keys():
                    ad.start_action = self.parseo2oaction(ad_pos["start"])
                if "mv" in ad_pos.keys():
                    ad.mv_action = self.parseo2oaction(ad_pos["mv"])
                if "end" in ad_pos.keys():
                    ad.end_action = self.parseo2oaction(ad_pos["end"])
                if "no_song" in ad_pos.keys():
                    ad.nosong_action = self.parseo2oaction(ad_pos["no_song"])
                if "horizon_lock_screen" in ad_pos.keys():
                    ad.horizon_action = self.parseo2oaction(ad_pos["horizon_lock_screen"])
                if "verticle_lock_screen" in ad_pos.keys():
                    ad.verticle_action = self.parseo2oaction(ad_pos["verticle_lock_screen"])
                if "redpack" in ad_pos.keys():
                    ad.redpack_action = self.parseo2oaction(ad_pos["redpack"])
                if "7000plus" in ad_pos.keys():
                    ad.redpack_action = self.parseo2oaction(ad_pos["7000plus"])
            if  "ad_info" in jsonres.keys():
                ad_info = jsonres["ad_info"]
                if ad_info:
                    for  item in ad_info:
                        mo2oad = o2oad_tvinfo()
                        mo2oad.id = item['ad']
                        mo2oad.url = item['url']
                        mo2oad.url2 = item['url2']
                        mo2oad.url2 = item['url2']
                        if item["type"].lower() == 'video':
                            mo2oad.type = 0
                        elif item["type"].lower() == 'gif':
                            mo2oad.type = 1
                        else:
                            mo2oad.type = 2
                        mo2oad.typestr = item["type"]
                        mo2oad.time = item['time']
                        mo2oad.monitor_url = []
                        mo2oad.md5 = item['md5']
                        for mstr in item["monitor_url"]:
                            mo2oad.monitor_url.append(mstr)
                        ad.ad_dict.append(mo2oad)
            return ad

    def parseo2oaction(self,action_dict):
        _action = None
        if action_dict:
            _action=o2oad_action()
            _action.action = action_dict["action"]
            _action.adlist = action_dict["ad"]
            _action.fullplay = action_dict["fullplay"]
            if 'pos' in action_dict.keys():
                _action.pos = action_dict['pos']
            if 'interval' in action_dict.keys():
                mtime=action_dict['interval'].split(",")
                if len(mtime):
                    _action.offset=mtime[0]
                    _action.interval=mtime[1]
                    _action.listinterval=mtime[2]
        return _action
    
    def o2oplaystat(self,adid,roomid,roominfo,cnt,playtime,stime,etime,adp,mac):
        iurl = AppSet().O2OAPI1
        url = "{0}/ad/policy".format(iurl)
        endurl="?ad_id={0}&ktv_id={1}&room_id={2}&room_info={3}&cnt={4}&time={5}&stt={6}&edt={7}&adp={8}&mac={9}".format(adid,roomid,roominfo,cnt,playtime,stime,etime,adp,mac)
        data=yhttp().get_y(url+endurl, 10)
        jsonres=json.loads(data)
        if "errcode" in jsonres:
            return jsonres
        return None       

if __name__ == '__main__':
    api=ktv_tvadinfoapi()
    api.o2oplaystat()
