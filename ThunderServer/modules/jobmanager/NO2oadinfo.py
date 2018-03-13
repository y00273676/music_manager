#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月28日
更新广告信息
@author: yeyinlin
'''
from config.appConfig import AppSet
import os
import platform
from common.fileutils import fileUtils
from modules.socketservice.control.ktv_tvadinfoapi import ktv_tvadinfoapi
from modules.model.o2oad_action import o2oad_tvinfo
import traceback
from common.utils import md5
from modules.jobmanager.control.synchronousutils import synchronousutils

import logging
logger = logging.getLogger(__name__)

class no2oadinfo():
    _ins = None
    @staticmethod
    def Ins():
        if not no2oadinfo._ins:
            no2oadinfo._ins = no2oadinfo()
        return no2oadinfo._ins

    def __init__(self):
        #文件下载的地址
        self._localsavepath = os.path.join(AppSet()._trandownpath,'o2oad')
        if not os.path.exists(self._localsavepath):
            os.mkdir(self._localsavepath)
        #o2o 下载广告的地址
        self._localdatapath = os.path.join(AppSet().ApachPath, "data", "o2o")

        #验证文件夹是否存在
        if not os.path.exists(self._localdatapath):
            os.makedirs(self._localdatapath)
        #广告的地址
        self.ad_data = os.path.join(self._localdatapath, "ad.json")
        self.ad_del = os.path.join(self._localdatapath, "ad_del.json")

        self.fu = fileUtils('o2oadinfo')
        self._down_dict = {}

        if platform.system().lower() == 'windows':
            self.server_localpath="c:\\thunder\\ktvservice\\ktv_o2oadinfo"
            self.server_localpathlinux="/opt/thunder/www/ktvservice/ktv_o2oadinfo/"
        else:#for linux
            self.server_localpath="/opt/thunder/ktvservice/ktv_o2oadinfo"
            self.server_localpathlinux="/opt/thunder/www/ktvservice/ktv_o2oadinfo/"

        self.synutils = synchronousutils()
        self.res_adcaption = None
        self._ad = None
    
    def uploadadinfo(self):
        try:
            #获取o2o 里面的信息 所有的信息
            self.res_adcaption = ktv_tvadinfoapi().Ins().geto2oadcaption()

        except Exception as e:
            logger.error(traceback.format_exc())

        try:
            #获取o2o 里面的信息 所有的信息
            ad = ktv_tvadinfoapi().Ins().geto2oadinfolist()
            self._ad = ad
            if ad:
                for tv in ad.ad_dict:
                    mitem = o2oad_tvinfo()
                    mitem.url = tv.url                
                    mitem.url2 = tv.url2                
                    mitem.typestr = tv.typestr                
                    mitem.type = tv.type                
                    mitem.time = tv.time              
                    mitem.md5 = tv.md5              
                    mitem.trytime = 0          
                    mitem.last_exectime = 0
                    self._down_dict[tv.id] = mitem
                #此处需要下载操作
                #以及加工操作
                #需要进行下载的操作
                for adid in self._down_dict.keys():
                    _down_tv = self._down_dict[adid]
                    #每一个都同步
                    res = self.syncadinfo(_down_tv)
                    #根据同步结果 进行下一步操作
        except Exception as e:
            logger.error(traceback.format_exc())
            
    def syncadinfo(self, tv, check=True):
        if check:
            url_suc = False
            _server_localpath = self.server_localpath if tv.type==0 else os.path.join(AppSet().ApachPath,'gif')
            if tv.url:
                ext = os.path.splitext(tv.url)[1]
                localpath = os.path.join(self._localsavepath, md5(tv.url)+str(ext))
                logger.debug("download url:%s to file %s" % (tv.url, localpath))
                #同步并下载文件
                if self.fu.downfile(tv.url, localpath, None, None):
                    if int(AppSet().DBtype)==1:
                        self.synutils.synfiletoserver(localpath,self.server_localpath,1)
                    else:
                        self.synutils.synfiletoserver(localpath,self.server_localpathlinux,1)
                else:
                    #没有下载成功时的操作
                    pass

            if tv.url2:
                ext=os.path.splitext(tv.url2)[1]
                localpath = os.path.join(self._localsavepath, md5(tv.url2)+str(ext))
                logger.debug("download url2:%s to file %s" % (tv.url2, localpath))
                #同步并下载文件
                if self.fu.downfile(tv.url2, localpath, None, None):
                    if int(AppSet().DBtype)==1:
                        self.synutils.synfiletoserver(localpath,self.server_localpath,1)
                    else:
                        self.synutils.synfiletoserver(localpath,self.server_localpathlinux,1)
                else:
                    #没有下载成功时的操作
                    pass
        return 1

    def addplaylog(self):
        pass

    #删除广告文件 
    def deladinfo(self):
        if self.del_dict and len(self.del_dict.keys()) > 0:
            for adid in self.del_dict.keys():
                try:
                    tv = self.del_dict[adid]
                    sb = ''
                    res_suc = False
                    if not tv.localpath:
                        linux_res = os.remove(tv.localpath)
                        logger.debug("o2o_adinfo.deladinfo() " + tv.localpath + ("删除成功" if res_suc else "删除失败"));

                    if tv.localpath2:
                        linux_res = os.remove(tv.localpath2)
                        logger.debug("o2o_adinfo.deladinfo() url2 " + tv.localpath2 + ("删除成功" if res_suc else "删除失败"));
                        if res_suc:
                            self.del_dict.pop(adid);
                except Exception as ex:
                    logger.error(traceback.format_exc())

if __name__ == '__main__':
    pass
