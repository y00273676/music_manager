#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月27日
墙纸更新
@author: yeyinlin
'''
import os
import json
import logging
import platform
import traceback

from lib.http import request_json

from common.fileutils import fileUtils
from common.utils import md5

from control.configs import get_config, update_setconfig
from handler.tsTask import tsServiceTask,tsTask
from setting import TMPDIR, DOWNLOADDIR, HTDOCDIR

logger = logging.getLogger(__name__)

class _appWallpaper(tsTask):
    def __init__(self, name='appWallpaper'):
        self.name = name
        self.fu = fileUtils(self.name)
        self._common_init(self.name)
        self.wallpaperpath = os.path.join(DOWNLOADDIR, self.name)
        if not os.path.exists(self.wallpaperpath):
            os.makedirs(self.wallpaperpath)
        self.paper_dict = {}
            
        if platform.system().lower == 'windows':
            self._filesavepath = "C:\\thunder\\Apache\\htdocs\\looppics\\picfile\\"
            self._filesavepath_turn = "C:\\thunder\\Apache\\htdocs\\looppics\\picfile_turn\\"
        else:
            self._filesavepath = "/opt/thunder/www/looppics/picfile/"
            self._filesavepath_turn = "/opt/thunder/www/looppics/picfile_turn/"
        self.localfilelist = list()
        self.tagfilelist = list()
        #self.radias = radisutils()

    def WallpaperInfo(self):
        wp = {}
        wp['paper_id'] = None
        wp['paper_name'] = None
        wp['paper_url'] = None
        #1横板,2竖版
        wp['paper_bagtype'] = None
        wp['paper_time'] = None
        wp['paper_state'] = None
        wp['paper_sort'] = None
        wp['paper_invalidtime'] = None
        wp['monitor_url'] = []
        return wp
 


    #获取墙纸
    def getWallPagersNew(self):
        dicResult={}
        url="{0}/ad/policy/{1}".format(self.O2OAPI, tsServiceTask.get_ktvid())

        logger.debug(url)
        res_dict = request_json(url, timeout=10, method='GET')
        horizon_pos={}
        verticle_pos={}
        if res_dict:
            if 'errcode' in res_dict.keys():
                if int(res_dict['errcode'])==200:
                    hstr = []
                    vstr = []
                    if 'ad_pos' in res_dict.keys():
                        ad_pos = res_dict['ad_pos']
                        if ad_pos:
                            if 'horizon_lock_screen' in ad_pos.keys():
                                horizon_pos = ad_pos['horizon_lock_screen']
                                if horizon_pos:
                                    hstr = horizon_pos["ad"]
                            if 'verticle_lock_screen' in ad_pos.keys():
                                verticle_pos = ad_pos['verticle_lock_screen']
                                if verticle_pos:
                                    vstr = verticle_pos["ad"]
                    if 'ad_info' in res_dict.keys():               
                        array_obj = res_dict["ad_info"]
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
                                info = self.WallpaperInfo()
                                info['paper_name'] = ad_dict["md5"]
                                info['paper_id'] = ad_dict["ad"]
                                info['paper_sort'] = ad_dict["ad"]
                                info['paper_bagtype'] = type
                                info['paper_url'] = ad_dict["url"]
                                info['monitor_url'] = ad_dict["monitor_url"]
                                if not type in dicResult.keys():
                                    dicResult[type]=[]
                                dicResult[type].append(info)
        return dicResult            

    def do_run(self):
        self.updateWallpaper()
        self.syncDataToServer()
        self.clearLastFile()

    #更新墙纸
    def updateWallpaper(self):
        RequestDic = self.getWallPagersNew()
        if RequestDic:
            for item in list(RequestDic.keys()):
                #需要知道什么时候同步的屏保 第二个参数是同步的类型 是竖屏还是横屏
                self.SyncData(RequestDic[item], item, True)
        else:
            logger.info("wallpaper/updatewallpage", "未获取到数据")   
    
    #判断是否需要同步        
    def SyncData(self,wall_list,type,issync):
        try:
            dicData = {}
            if issync:
                dicData = None
            dic = {}
            namelist = list()
            dic['name'] = namelist
            if not dicData:
                for item in wall_list:
                    name = os.path.join(self.wallpaperpath,os.path.basename(item['paper_url']))
                    #同步墙纸
                    self.fu.downfile(item['paper_url'], name, None, None)
                    self.localfilelist.append(name)
                    #需要存入redis
                    walldic = {}
                    walldic['path'] = name
                    walldic['wall'] = item
                    namelist.append(walldic)
            self.paper_dict['type'] = dic
            
        except Exception as e:
            logger.error(traceback.format_exc())
        
    def syncDataToServer(self):
        #拿到了墙纸的地址，需要同步
        return True
        '''
        fileDicPath = self.wallpaperpath
        try:
            
            for mkey in self.paper_dict.keys():
                if int(mkey) == 0:
                    wall_dic = self.paper_dict[0]
                    for item in wall_dic['name']:
                    #linux
                        logger.info('同步到',item['path'],self._filesavepath)
                        self.synch.synfiletoserver(item['path'],self._filesavepath,0)
                        tagpath = os.path.join(self._filesavepath,os.path.basename(item['path']))
                        self.tagfilelist.append(tagpath)
                        
                else:
                    wall_dic = self.paper_dict[1]
                    #linux
                    for item in wall_dic['name']:
                        logger.info('同步到',item['path'],self._filesavepath_turn)
                        self.synch.synfiletoserver(item['path'],self._filesavepath_turn,0)
                        tagpath = os.path.join(self._filesavepath_turn,os.path.basename(item['path']))
                        self.tagfilelist.append(tagpath)
                    #竖版
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e)
        '''
    
    def clearLastFile(self):
        return True
        #dellocalfile() #删除本地文件还有问题，待修改
        #self.radias.updatadownrecode(self.name,self.tagfilelist)
        #self.radias.delalldeletefile(self.name)

appWallpaper = _appWallpaper()
    
if __name__ == '__main__':
    wall=Wallpapers()
    wall.updatewallpage()
    wall.syncdatatoserver()
    wall.clearlastfile()

