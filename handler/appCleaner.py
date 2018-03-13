#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import json
import shutil
import urllib
import logging
import datetime
import traceback
import threading

from setting import TMPDIR, DOWNLOADDIR
from common.yhttp import yhttp
from common.fileutils import fileUtils
from common.ZFile import extract
#from modules.bll.SettingBll import SettingBll
from lib.types import try_to_int
from control.configs import update_setconfig, get_all_config, get_config
from control.medias import medias_set_newsong, medias_update_fpath, medias_get_delete_list
#from modules.bll.MediaNewSongBLL import MediaNewSongBLL
from handler.tsTask import tsServiceTask,tsTask
from control.mediaimport import load_allowdel_medias
from control.cloudmusic import get_musicinfo_bylist

logger = logging.getLogger(__name__)

class _appCleaner(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    #_interval = 10
    _lastrun = 0

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('initialize cleaner singleton instance')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appCleaner, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self, name='appCleaner'):
        self.name = name
        self.fu = fileUtils(self.name)
        self.ktvid = None
        self.dogname = ''
        self.tempDir = os.path.join(TMPDIR, self.name)
        self.downDir = os.path.join(DOWNLOADDIR, self.name)
        if not os.path.exists(self.downDir):
            os.makedirs(self.downDir)

        self._common_init(self.name)

        self.setting = get_all_config()
        self.lasttime = 0
        
    def do_run(self):
        self.dogname = tsServiceTask.get_dogname()
        self.ktvid = tsServiceTask.get_ktvid()
        if not self.ktvid or not self.dogname:
            self._lastmsg = "Falied to get ktvinfo."
            logger.debug(self.lastmsg)
            return False
        self.get_allow_delete_list(self.lasttime)
        self.clean_mediafiles(self.lasttime)
        self.clean_tempfiles(self.lasttime)
        self.clean_themes(self.lasttime)
        self.clean_modules(self.lasttime)
        self.clean_modules(self.lasttime)

    def _is_today(self, timestemp):
        today = time.strftime('%Y-%m-%d', time.localtime() )
        theday = time.strftime('%Y-%m-%d', time.localtime(timestemp) )
        return today == theday

    def clean_mediafiles(self, lasttime):
        disks = os.listdir('/video')
        free = 0
        for disk in disks:
            vfsinfo = os.statvfs(os.path.join('/video', disk))
            space = vfsinfo.f_bavail * vfsinfo.f_bsize / 1024  / 1024 / 1024
            free += space
        logger.debug('total free disk : %s GB' % free)
        if free < 100:
            #call deleteing procedure when total disk space less than 100GB
            mlist = medias_get_delete_list()
            if len(mlist) == 0:
                return True
            i = 0
            for m in mlist.keys():
                logger.debug("Deleting- %s : %s " % (m, mlist[m]))
                if os.path.exists(mlist[m]):
                    os.remove(mlist[m])
            medias_update_fpath(mlist.keys())
        else:
            logger.debug(" have enough space")

    def clean_tempfiles(self, lasttime):
        pass

    def clean_themes(self, lasttime):
        #already delete in appTheme module
        return True
        pass

    def clean_modules(self, lasttime):
        if self._is_today(lasttime):
            return True
        pass

    def get_allow_delete_list(self, lasttime):
        if self._is_today(lasttime):
            return True
        #http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?op=getallmusicfile&depot=0&musictype=5&linkzip=1
        url = "%s/MusicService.aspx?op=getallmusicfile&depot=0&musictype=5&linkzip=1" % self.kcloud_v2
        res = yhttp().get_y(url)
        logger.debug("call url: %s, result: %s" % (url, res))
        resdata = json.loads(res)
        if resdata and int(resdata['code'])==1:
            if resdata['result']:
                fname = os.path.join(self.downDir, self.fu.filename(resdata['result']))
                if os.path.exists(fname):
                    #we think it has been loaded into db here
                    #only when cloud side publish new file, it will force to update
                    #also, delete the zip file will cause a force update!
                    return True
                else:
                    ret = self.fu.downfile(resdata['result'], fname, None, None)
                    if not ret:
                        logger.error("Failed to download cloud_musicinfo file")
                        return False

                #extra
                txtname, _ = os.path.splitext(fname)
                extra_fname = '%s.txt' % os.path.join(self.downDir, txtname)
                if extract(fname, self.downDir):
                    pass
                else:
                    #if failed to extra, delete the zip file to download again
                    if os.path.exists(extra_fname):
                        os.remove(extra_fname)
                logger.error("TODO: load music info into medias table......")

                if load_allowdel_medias(extra_fname):
                    if os.path.exists(extra_fname):
                        os.remove(extra_fname)
                    return True
                else:
                    if os.path.exists(fname):
                        os.remove(fname)
                    if os.path.exists(extra_fname):
                        os.remove(extra_fname)
                    logger.error("Failed to load allow delete medias from file")
                    return False
        else:
            logger.error("Failed to get allow delete info")
        return False

appCleaner = _appCleaner()

