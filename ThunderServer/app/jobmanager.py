#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年5月2日

@author: yeyinlin
'''
from modules.jobmanager.NModuleinfo import Moduleinfo
from modules.jobmanager.NO2oadinfo import no2oadinfo
from modules.jobmanager.NUpmoduletheme import nupmoduletheme
from modules.jobmanager.roomclassinfo import roomclassinfo
from modules.jobmanager.Wallpapers import Wallpapers
from modules.jobmanager.clearcache import clearcache
from modules.jobmanager.codeexec import codeexec
from modules.jobmanager.newsong import newsong
from modules.jobmanager.resDeploy import ResDeploy
# from modules.socketservice.ktv_tvadinfoService import tvadinfo
from modules.jobmanager.control.moduleapi import moduleapi
from modules.jobmanager.appupgrade import appUpgrade
class Mjobmanager():
    def __init__(self,name):
        pass
    
    def start(self):
        #升级包下载
        appup = appUpgrade()
        appup.UpdateApp()
        print('NewSong:' + '*' * 80)
        mysong = newsong()
        #mysong.updatenewsong()
        mysong.getCloudSong()
        #模版下载模块
        print('\nModule:' + '*' * 80)
        module = Moduleinfo()
        module.loadonlinemodule(1)
        module.loadonlinemodule(2)
        module.startimport()
        #themes
        ####皮肤包下载***************************##
        ins = nupmoduletheme().Ins()
        ins.updatanewtheme()
        #下载资源包
        #各种资源下载（ktvTasks)***************************##
        hdl_res = ResDeploy()
        hdl_res.getCloudRes()
        return True
        #o2o广告模块
        print('O2OAd:' + '*' * 80)
        no2oad = no2oadinfo().Ins()
        no2oad.uploadadinfo()

        #壁纸模块
        print('Wallpaoers:' + '*' * 80)
        wall = Wallpapers()
        wall.updatewallpage()
        wall.syncdatatoserver()
        wall.clearlastfile()
        
        #清理Cache?
        print('clearcache:' + '*' * 80)
        cache = clearcache('clearcache')
        cache.cleardir(cache.curclear)
        
        '''
        #线上推下SQL脚本，线下执行
        print('execcode:' + '*' * 80)
        mexec = codeexec()
        mexec.runexec()
        '''
        ####***************************##
        #adinfo=tvadinfo().get_instance()

        
class UpdataModule():
    #需要知道
    def __init__(self,name):
        pass
    
    def start(self):
        module=Moduleinfo().Ins()
        
    def restart(self):
        pass
    
    def stop(self):
        pass
        

if __name__ == '__main__':
    pass
