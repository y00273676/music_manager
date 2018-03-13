#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月28日
更新模板主题
@author: yeyinlin
'''

import os
import time
import logging
import datetime
import traceback

from common.fileutils import fileUtils
from common.ZFile import extract

from config.appConfig import AppSet
from modules.model.Ktvmodule_theme import Ktvmodule_theme
from modules.bll.KtvModuleVerBLL import KtvModuleVerBll
from modules.jobmanager.control.moduleapi import moduleapi

logger = logging.getLogger(__name__)

#下载任务和更新任务不同时进行
class nupmoduletheme(object):
    _ins = None
    @staticmethod
    def Ins():
        if not nupmoduletheme._ins:
            nupmoduletheme._ins = nupmoduletheme()
        return nupmoduletheme._ins
    
    def __init__(self):
        self._bll = KtvModuleVerBll()
        self._mapi = moduleapi()
        self.theme_savepath = "themes"
        self.fu = fileUtils('ktvtheme')
        self.store_path = os.path.join(AppSet()._trandownpath, self.theme_savepath)
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)
        self.topath = os.path.join(AppSet().ApachPath, 'themes')
        
        #本地的主题
        self.local_themes={}
        #全局的主题
        self.ver_themes={}
        #执行出错的主题
        self.err_themes={}
        
    #需要定时的执行更新theme的任务
    def updatanewtheme(self):
        try:
            #需要从数据库中查询出来 主题来  按在线的主题来
            themeList = self._bll.GetAllKtvModule_Theme(1)
            #如果含有参数
            lasttime = datetime.datetime(2017, 1, 1, 9, 0, 0, 0)
            if themeList:
                for key in themeList:
                    #获取转化的时间戳 
                    mytime = key.theme_date
                    if key.theme_state == 1 and mytime > lasttime:
                        lasttime = key.theme_date
            print(str(lasttime))
            #获取最新的 主题列表
            themes = self._mapi.getnewthemes(lasttime)
            print('get %s themes' % themes)
            if isinstance(themes, list) and len(themes) > 0:
                for theme in themes:
                    self.ver_themes[theme.theme_id] = theme
                    fname = os.path.basename(theme.theme_path)
                    theme_file = os.path.join(self.store_path, fname)
                    if not os.path.exists(theme_file):
                        downres = self.fu.downfile(theme.theme_path, theme_file, None, None)
                    else:
                        downres = True
                    if downres:
                        #如果下载完成
                        theme.theme_path = theme_file
                        theme.theme_unpath = os.path.join(self.topath, "htheme_" + os.path.splitext(fname)[0])
                        self.install_theme(theme)
                        #添加进全局的字典
                        self.ver_themes[theme.theme_id] = theme
                    else:
                        #没有下载的处理 未下载
                        self.module_dict[theme.theme_id] = res_ver
            else:
                logger.info('线上未获取主题')

        except Exception as e:
            logger.error(traceback.format_exc())
   
    def install_theme(self, theme):
        print(theme.theme_path, theme.theme_unpath)
        if theme == None:
            return False
        if not theme.theme_path or not theme.theme_unpath:
            return False

        if extract(theme.theme_path, theme.theme_unpath):
            theme.theme_state = 1
            #theme.theme_unpath = theme.theme_unpath[len('/opt/thunder/www'):]
            #print(theme.theme_unpath)
            ret = self._bll.AddModule_Theme(theme)
            print(str(ret))
        else:
            logger.error("Failed to install themes to server")

 
    #需要定时的执行同步的任务
    def syndata(self):
        try:
            if self.ver_themes:
                if len(list(self.ver_themes.keys()))>0:
                    self.syncthemetoserver(self.ver_themes.values())
        except Exception as e :
            print("traceback.format_exc()",traceback.format_exc())


    def syncthemetoserver(self, themelist):
        if themelist:
            for theme in themelist:
                #本地存储的地址
                local_theme_path=os.path.join(AppSet()._trandownpath,self.theme_savepath,os.path.basename(theme.theme_path))
                #下载主题列表
                if self.fileutil.downfile(theme.theme_path, local_theme_path, None, None):
                    #
                    tlocalname=os.path.basename(theme.theme_path)
                    name=os.path.splitext(tlocalname)[0]
                    theme.theme_unpath = os.path.join(self.topath, self.theme_savepath, "htheme_" + name)
                    '''
                    #win
                    if int(AppSet().DBtype)==1:
                        theme.theme_unpath=os.path.join(self.towinpath, self.theme_savepath,"htheme_" + name)
                    #linux
                    else:
                        theme.theme_unpath=os.path.join(self.tolinuxpath,self.theme_savepath,"htheme_" + name)
                    '''
                    unpath = os.path.join(AppSet()._trandownpath, self.theme_savepath)
                    #开始解压
                    if extract(local_theme_path, unpath):
                        #开始同步文件 到服务端
                        suc_status = self.synutil.synfiletoserver(local_theme_path, theme.unpath, 1)
                        #同步成功
                        if suc_status==1:
                            #需要将已经同步的主题插入数据库
                            theme.theme_path = local_theme_path
                            theme.theme_state = 1
                            self._bll.AddModule_Theme(theme)
                        else:
                            logger.error("Failed to sync themes to server")
                            #同步失败
                            pass
if __name__ == '__main__':
    ins=nupmoduletheme().Ins()
    ins.updatanewtheme()
