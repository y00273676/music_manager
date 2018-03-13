#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import logging
import datetime
import traceback
import threading

from common.fileutils import fileUtils
from common.ZFile import extract
from common.yhttp import yhttp
from lib.http import request_json

#from modules.model.Ktvmodule_theme import Ktvmodule_theme
#from modules.bll.KtvModuleVerBLL import KtvModuleVerBll

from control.themes import add_theme, get_all_themes, delete_theme
from control.configs import get_config
from handler.tsTask import tsServiceTask,tsTask
from setting import TMPDIR, DOWNLOADDIR, HTDOCDIR

logger = logging.getLogger(__name__)

#下载任务和更新任务不同时进行
class _appTheme(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()
    #_interval = 3600
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('_appTheme singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appTheme, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('_appTheme singleton is exists')
        return cls.__instance

    def __init__(self, name='appTheme'):
        self.name = name

        self.fu = fileUtils(self.name)

        self.theme_savepath = self.name
        self.store_path = os.path.join(DOWNLOADDIR, self.theme_savepath)
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)

        self.topath = os.path.join(HTDOCDIR, self.name)
        
        self._common_init(self.name)
        self.lk = 2

    def do_run(self):
        print('Updating themes **************')
        self.updateNewTheme()
        
    #需要定时的执行更新theme的任务
    def updateNewTheme(self):
        try:
            #需要从数据库中查询出来 主题来  按在线的主题来
            #themeList = self._bll.GetAllKtvModule_Theme(1)
            themeList = get_all_themes()
            if themeList:
                themeList = themeList['matches']
            #如果含有参数
            lasttime = datetime.datetime(2017, 1, 1, 9, 0, 0, 0)
            if themeList:
                for theme in themeList:
                    #获取转化的时间戳 
                    mytime = theme['theme_date']
                    if theme['theme_state'] == 1 and mytime > lasttime:
                        lasttime = theme['theme_date']
            logger.debug("[%s] last update time: %s" % (self.name, str(lasttime)))
            #获取最新的 主题列表
            themes = self.getNewThemes(lasttime)
            logger.debug('get Themes: %s' % themes)
            if isinstance(themes, list) and len(themes) > 0:
                for theme in themes:
                    fname = os.path.basename(theme['theme_path'])
                    theme_file = os.path.join(self.store_path, fname)
                    if not os.path.exists(theme_file):
                        downres = self.fu.downfile(theme['theme_path'], theme_file, None, None)
                    else:
                        downres = True

                    if downres:
                        #如果下载完成
                        theme['theme_path'] = theme_file
                        theme['theme_unpath'] = os.path.join(self.topath, "htheme_" + os.path.splitext(fname)[0])
                        self.install_theme(theme)
            else:
                logger.info('线上未获取主题')

            logger.info("check for clean outdate themes")
            for theme in themeList:
                res = self.checkThemeStatus(theme['theme_id'])
                logger.info("checkThemeStatus: Theme_id: %d , res: %s" % (theme['theme_id'], res))
                if res > 0:
                    delete_theme(theme['theme_id'])
                    if os.path.exists(theme['theme_path']):
                        os.remove(theme['theme_path'])
                    if os.path.exists(theme['theme_unpath']):
                        shutil.rmtree(theme['theme_unpath'])
        except Exception as e:
            logger.error(traceback.format_exc())

    def cleanOldThemes(self, localTheme, onlineThemes):
        pass
   
    def install_theme(self, theme):
        if theme == None:
            return False
        print(theme['theme_path'], theme['theme_unpath'])
        if not theme['theme_path'] or not theme['theme_unpath']:
            return False

        if extract(theme['theme_path'], theme['theme_unpath']):
            theme['theme_state'] = 1
            #print(theme.theme_unpath)
            #ret = self._bll.AddModule_Theme(theme)
            ret = add_theme(theme)
            logger.debug("add_theme (%s) returns: %s" % (theme['theme_unpath'], ret))
            return True
        else:
            logger.error("Failed to install themes to server")
            return False

    def getNewThemes(self, lasttime="1990-01-01 00:00:00"):
        self.dogname = tsServiceTask.get_dogname()
        self.ktvid = tsServiceTask.get_ktvid()
        if not self.dogname or not self.ktvid:
            logger.error("Failed to get dogname or ktvinfo")
            return False
 
        themeList=[]
        try:
            baseurl = "%s/ModuleService.aspx?" % self.KtvApi
            param={}
            param['op'] = 'getmoduletheme'
            param['lasttime'] = str(lasttime)
            param['storeid'] = str(self.ktvid)
            param['dogname'] = self.dogname
            param['time'] = str(int(time.time()))
            #print (param)
            paramurl = yhttp().ParamSign(param)
            url = baseurl + paramurl
            if self.lk == 1 or self.lk == 2:
                url += '&lk=1'
            logger.debug(url)
            result = yhttp().get_y(url, 10)
            dic_res = json.loads(result)
            logger.debug(dic_res )
            if dic_res and str(dic_res['code']) == '1':
                if isinstance(dic_res['result'], dict):
                    mresult = dic_res['result']['matches']
                    if len(mresult) > 0:
                        for obj in mresult:
                            theme = {}
                            theme['theme_id'] = obj["theme_id"]
                            theme['theme_name'] = obj["theme_name"]
                            theme['theme_desc'] = obj["theme_desc"]
                            theme['theme_path'] = obj["theme_path"]
                            theme['theme_unpath'] = ''
                            theme['theme_type'] = obj["theme_type"]
                            theme['theme_date'] = obj["theme_date"]
                            theme['theme_author'] = obj["theme_author"]
                            theme['theme_authorize'] = obj["theme_authorize"]
                            theme['theme_bagtype'] = obj["theme_bagtype"]
                            theme['theme_exptime'] = obj["theme_exptime"]
                            theme['theme_state'] = obj["theme_state"]
                            themeList.append(theme)
            else:
                return themeList
            return themeList
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    #获取自由切换主题的状态是否已经失效/过期
    def checkThemeStatus(self, tid):
        result = 0
        try:
            param = {}
            param['id'] = str(tid)
            param['time'] = str(int(time.time()))
            param['op'] = "checkinvalidtheme"
            paramurl = yhttp().ParamSign(param)
            url = "%s/ModuleService.aspx?%s" % (self.KtvApi, paramurl)
            logger.debug(url)
            result = yhttp().get_y(url, 10)
            dic_res = json.loads(result)
            if dic_res and str(dic_res['code']) == '1':
                result = dic_res['result']
                return result
        except Exception as ex:
            logger.error(traceback.format_exc())
        return result

appTheme = _appTheme()

if __name__ == '__main__':
    pass
