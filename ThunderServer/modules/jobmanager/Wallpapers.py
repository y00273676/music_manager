#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月27日
墙纸更新
@author: yeyinlin
'''
from modules.jobmanager.control.wallpageapi import wallpageapi
import traceback
import os
from common.fileutils import fileUtils
from config.appConfig import AppSet
from common.utils import md5
from modules.jobmanager.control.synchronousutils import synchronousutils
from modules.jobmanager.control.radisutils import radisutils

import platform
import logging
logger = logging.getLogger(__name__)

class Wallpapers(object):
    def __init__(self):
        self.myname="wallpapers"
        self._wpapi=wallpageapi()
        self._trandownpath = AppSet()._trandownpath
        self.fu = fileUtils('Wallpapers')
        self.savepath=os.path.join(AppSet()._trandownpath, "ktvservice")
        self.paper_dict={}
        self.wallpaperpath=os.path.join(self.savepath,'wallpaper')
        print(self.wallpaperpath)
        if not os.path.exists(self.wallpaperpath):
            os.makedirs(self.wallpaperpath)
            
        if platform.system().lower == 'windows':
            self._filesavepath = "C:\\thunder\\Apache\\htdocs\\looppics\\picfile\\"
            self._filesavepath_turn = "C:\\thunder\\Apache\\htdocs\\looppics\\picfile_turn\\"
        else:
            self._filesavepath = "/opt/thunder/www/looppics/picfile/"
            self._filesavepath_turn = "/opt/thunder/www/looppics/picfile_turn/"
        self.synch=synchronousutils()
        self.localfilelist=list()
        self.tagfilelist=list()
        self.radias=radisutils()
        
    #更新墙纸
    def updatewallpage(self):
        RequestDic=self._wpapi.GetWallPagersNew()
        if RequestDic:
            for item in list(RequestDic.keys()):
                #需要知道什么时候同步的屏保 第二个参数是同步的类型 是竖屏还是横屏
                self.SyncData(RequestDic[item], item, True)
        else:
            print("wallpaper/updatewallpage", "未获取到数据")   
    
    #判断是否需要同步        
    def SyncData(self,wall_list,type,issync):
        try:
            if not os.path.exists(self._trandownpath):
                os.makedirs(self._trandownpath)
            dicData={}
            if issync:
                dicData=None
            dic={}
            namelist=list()
            dic['name']=namelist
            if not dicData:
                for item in wall_list:
                    name=os.path.join(self.wallpaperpath,os.path.basename(item.paper_url))
                    #同步墙纸
                    self.fu.downfile(item.paper_url, name, None, None)
                    self.localfilelist.append(name)
                    #需要存入redis
                    walldic={}
                    walldic['path']=name
                    walldic['wall']=item
                    namelist.append(walldic)
            self.paper_dict[type]=dic
            
        except Exception as e:
            print("traceback.format_exc()",traceback.format_exc())
        
    def syncdatatoserver(self):
        #拿到了墙纸的地址，需要同步
        fileDicPath=self.wallpaperpath
        try:
            
            for mkey in list(self.paper_dict.keys()):
                if int(mkey)==0:
                    wall_dic=self.paper_dict[0]
                    for item in wall_dic['name']:
                    #linux
                        print('同步到',item['path'],self._filesavepath)
                        self.synch.synfiletoserver(item['path'],self._filesavepath,0)
                        tagpath=os.path.join(self._filesavepath,os.path.basename(item['path']))
                        self.tagfilelist.append(tagpath)
                        
                else:
                    wall_dic=self.paper_dict[1]
                    #linux
                    for item in wall_dic['name']:
                        print('同步到',item['path'],self._filesavepath_turn)
                        self.synch.synfiletoserver(item['path'],self._filesavepath_turn,0)
                        tagpath=os.path.join(self._filesavepath_turn,os.path.basename(item['path']))
                        self.tagfilelist.append(tagpath)
                    #竖版
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e)
    
    def clearlastfile(self):
#         dellocalfile() #删除本地文件还有问题，待修改
        self.radias.updatadownrecode(self.myname,self.tagfilelist)
        self.radias.delalldeletefile(self.myname)
    
if __name__ == '__main__':
    wall=Wallpapers()
    wall.updatewallpage()
    wall.syncdatatoserver()
    wall.clearlastfile()

