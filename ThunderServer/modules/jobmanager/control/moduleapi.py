#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月13日

@author: yeyinlin
'''
import json
import time
import urllib
import traceback
import logging

from config.appConfig import AppSet
from common.yhttp import yhttp
from common.KtvInfo import hdl_ktvinfo
from modules.model.Ktvmodule_theme import Ktvmodule_theme
from common.functions import getSignedUrl
from modules.model.KtvModule_Ver import KtvModule_Ver

logger = logging.getLogger(__name__)

class moduleapi():
    def __init__(self):
        self.ktvid = None
        self.lk = hdl_ktvinfo.lk
        #till now, only module service only recognize "lk=1' flag for Leike product.
        # yishunli@thunder.com.cn    2017-11-01
        self.lk = 1
        
    def getnewmodule(self,m_ver,bagtype,appver):
        logger.debug("getnewmodule")
        self.ktvinfo = hdl_ktvinfo.get_ktvinfo()
        if not self.ktvinfo:
            return False
        self.ktvid = self.ktvinfo.ktvid
        #获取模板信息
        if self.lk == 1 or self.lk == 2:
            url="%s/module_verservice.aspx?op=getmoduleverjson&version=%s&dogname=%s&bagtype=%s&storeId=%s&type=v2&appver=%s&lk=%d" % (AppSet.songlist, m_ver, yhttp().UrlEncode(AppSet()._dogname), bagtype, self.ktvid, appver, self.lk)
        else:
            url="%s/module_verservice.aspx?op=getmoduleverjson&version=%s&dogname=%s&bagtype=%s&storeId=%s&type=v2&appver=%s" % (AppSet.songlist, m_ver, yhttp().UrlEncode(AppSet()._dogname), bagtype, self.ktvid, appver)
        logger.debug(url)
        result = yhttp().get_y(url,10)
        dic_res = json.loads(result)
        arrver=[]
        if dic_res and str(dic_res['code']) == '1':
            if isinstance(dic_res['result'], dict):
                mresult=dic_res['result']['matches']
                var=KtvModule_Ver()
                if len(mresult)>0:
                    for item in mresult:
                        var.msgtime=item['MsgTime']
                        var.version=item['Version']
                        var.fileurl=item['FileUrl']
                        var.desc=item['Desc']
                        var.addtime=str(int(time.time()))
                        var.needun=0
                        var.revision=item['ReVision']
                        var.bagtype=item['BagType']
                        var.unpath=""
                        var.name=item['Name']
                        var.isshow=item['IsShow']
                        var.id=item['Id']
                        var.isuse=1
                        var.vertype=item['VerType']
                        var.isdefault=item['IsDefault']
                        arrver.append(var)
                return arrver
        return arrver

    def getnewthemes(self, lasttime="1990-01-01 00:00:00"):
        themeList=[]
        try:
            self.ktvinfo = hdl_ktvinfo.get_ktvinfo()
            if not self.ktvinfo:
                return False
            self.ktvid = self.ktvinfo.ktvid
            baseurl="{0}/ModuleService.aspx?".format(AppSet().KtvApi)
            #param="op=getmoduletheme&lasttime=%s&storeid=%s&dogname=%s" % (str(lasttime),str(self.ktvid),urllib.parse.quote(AppSet()._dogname))
            param={}
            param['op'] = 'getmoduletheme'
            param['lasttime'] = str(lasttime)
            param['storeid'] = str(self.ktvid)
            param['dogname'] = AppSet()._dogname
            param['time'] = str(int (time.time()))
            #print (param)
            paramurl = yhttp().ParamSign(param)
            url = baseurl + paramurl
            if self.lk == 1:
                url += '&lk=1'
            #url=getSignedUrl(str(baseurl),str(param))
            print(url)
            result = yhttp().get_y(url,10)
            dic_res = json.loads(result)
            #print(dic_res )
            if dic_res and str(dic_res['code']) == '1':
                if isinstance(dic_res['result'], dict):
                    mresult=dic_res['result']['matches']
                    if len(mresult)>0:
                        for obj in mresult:
                            theme=Ktvmodule_theme()
                            theme.theme_id = obj["theme_id"]
                            theme.theme_author = obj["theme_author"]
                            theme.theme_authorize = obj["theme_authorize"]
                            theme.theme_bagtype = obj["theme_bagtype"]
                            theme.theme_date = obj["theme_date"]
                            theme.theme_desc = obj["theme_desc"]
                            theme.theme_exptime = obj["theme_exptime"]
                            theme.theme_name = obj["theme_name"]
                            theme.theme_path = obj["theme_path"]
                            theme.theme_state = obj["theme_state"]
                            theme.theme_type = obj["theme_type"]
                            themeList.append(theme)
            else:
                return themeList
            return themeList
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    #获取自由切换主题的状态是否已经失效/过期
    def checkthemestatus(self,id):
        result=0
        try:
            param={}
            param['id']=id
            param['time']=str(int(time.time()))
            param['op']="checkinvalidtheme"
            paramurl=yhttp().ParamSign(param)
            baseurl="{0}/ModuleService.aspx?".format(AppSet().KtvApi)
            url=baseurl+paramurl
            print(url)
            result = yhttp().get_y(url,10)
            dic_res = json.loads(result)
            if dic_res and str(dic_res['code']) == '1':
                result=dic_res['result']
                return result
        except Exception as e:
            print(e)
        return result
if __name__ == '__main__':
    api=moduleapi()
    print(api.getnewthemes())
