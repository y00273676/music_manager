#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月27日

@author: yeyinlin
'''
from config.appConfig import AppSet
from common.KtvInfo import KtvInfo
from common.yhttp import yhttp
import json
from modules.model.WallpaperInfo import WallpaperInfo
class wallpageapi(object):
    def __init__(self):
        ktvinfo=KtvInfo()
        self.ktvid=ktvinfo._info._ktvid
    #获取墙纸
    def GetWallPagersNew(self):
        iurl=AppSet.O2OAPI
        dicResult={}
        url="{0}/ad/policy/{1}".format(iurl, self.ktvid)
        print(url)
        result = yhttp().get_y(url,10)
        res_dict = json.loads(result)
        horizon_pos={}
        verticle_pos={}
        if res_dict:
            if 'errcode' in res_dict.keys():
                if int(res_dict['errcode'])==200:
                    hstr = []
                    vstr = []
                    if 'ad_pos' in res_dict.keys():
                        ad_pos=res_dict['ad_pos']
                        if ad_pos:
                            if 'horizon_lock_screen' in ad_pos.keys():
                                horizon_pos=ad_pos['horizon_lock_screen']
                                if horizon_pos:
                                    hstr=horizon_pos["ad"]
                            if 'verticle_lock_screen' in ad_pos.keys():
                                verticle_pos=ad_pos['verticle_lock_screen']
                                if verticle_pos:
                                    vstr=verticle_pos["ad"]
                    if 'ad_info' in res_dict.keys():               
                        array_obj=res_dict["ad_info"]
                        for adinfo in array_obj:
                            ad_dict=adinfo
                            if ad_dict["type"].lower()=="image" and ".bmp"in ad_dict["url"]:
                                type = 0
                                if len(hstr)>0:
                                    for arrayh in hstr:
                                        if str(arrayh)==str(ad_dict["ad"]):
                                            type = 0
                                            break
                                if len(vstr)>0:
                                    for arrayh in hstr:
                                        if str(arrayh)==str(ad_dict["ad"]):
                                            type = 1
                                            break
                                info=WallpaperInfo()
                                info.paper_name = ad_dict["md5"]
                                info.paper_id = ad_dict["ad"]
                                info.paper_sort = ad_dict["ad"]
                                info.paper_bagtype = type
                                info.paper_url = ad_dict["url"]
                                info.monitor_url = ad_dict["monitor_url"]
                                if not type in dicResult.keys():
                                    dicResult[type]=[]
                                dicResult[type].append(info)
        
        
        return dicResult            
if __name__ == '__main__':
    api=wallpageapi()
    print (api.GetWallPagersNew())
    
