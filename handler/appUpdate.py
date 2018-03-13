#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import platform
import json
import logging

import sys
if sys.version_info < (3,):
    from urllib2 import urlopen
    from urllib2 import quote,unquote
    import commands as subprocess
else:
    from urllib.request import urlopen
    from urllib.parse import quote,unquote
    import subprocess

import traceback
import threading
from zipfile import BadZipfile


from lib.http import request_json
#from common.Thunder import Thunder
#from common.KtvInfo import KtvInfo
from common.fileutils import fileUtils
from common.utils import VersionConvert
from common.ZFile import extract
#from config.appConfig import AppSet
#from modules.bll.SettingBll import SettingBll
from setting import TMPDIR, DOWNLOADDIR
from handler.tsTask import tsServiceTask,tsTask
from control.configs import get_config

#from modules.jobmanager.db.dbhelper import dbhelper

logger = logging.getLogger(__name__)

class _appUpgrade(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    #_interval = 10
    #_lastrun = 0

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('KtvInfo singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appUpgrade, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('KtvInfo singleton is exists')
        return cls.__instance

    def __init__(self, name='appUpdate'):
        #self.setbll = SettingBll()
        #self.iswork=False
        self.name = name
        self.patchDir = os.path.join(DOWNLOADDIR, self.name)
        self.tempDir = os.path.join(TMPDIR, self.name)
        #self.transip = self.getTransIP()
        self.fu = fileUtils(self.name)
        self.lk = 1

        self._common_init(self.name)

        #这两个是上下文执行用的，如果有重入，要清除掉
        self.fileName = None
        self.maxver = None

    def get_cur_version(self):
        cfg = get_config("karaok_ver")
        if cfg:
            self.version = cfg['config_value']
            return True

    def searchTUP(self):
        for f in os.listdir(self.tempDir):
            if f.endswith(".tup"):
                return os.path.join(self.tempDir, f)
        return ''

    def run(self):
        logger.error('[%s] run in, time: %.2f' % (self.name, time.time()))
        if self.running:
            logger.error('[%s] already running, cannot run two instance at the same time' % self.name)
            return

        self.running = True
        try:
            #处理用户确认状态及行为：
            if self._confirm and self.status == 'confirmed':
                logger.info('[%s] run callback with confirmed action' % self.name)
                self.do_callback()
                return
            if self._confirm:
                logger.info('[%s] waiting user confirm action' % self.name)
                return 

            #再走正常的程序
            self.do_run()
        except Exception as ex:
            logger.error(traceback.format_exc())
        finally:
            self.running = False
            logger.error('[%s] run out, time: %.2f' % (self.name, time.time()))

    def do_run(self):

        #这两个是上下文执行用的，如果有重入，要清除掉
        self.fileName = None
        self.maxver = None

        self._lastrun = time.time()
        if not self.get_cur_version():
            logger.error('[%s] Failed to get software version, aborting' % self.name)
            self._lastmsg = "Failed to get current version"
            return False

        if os.path.exists(self.patchDir) == False:
            os.makedirs(self.patchDir)
        if not tsServiceTask.get_dogname():
            logger.error('[%s] Failed to get DogName, aborting' % self.name)
            self._lastmsg = "Failed to get dogname"
            return False

        #这里需要打印加密狗，然后调用接口需要解密狗名称进行验证
        logger.debug('DogName:' + tsServiceTask.get_dogname())
        self._lastmsg = "calling home"
        if self.lk == 1 or self.lk == 2:
            url = '%s/ProgramPatchService.aspx?op=getcloudappupdatelist' \
                    '&apptype=2&version=%s&minversion=0.0.0.0&os=linux&time=%d' \
                    '&dogname=%s&lk=%d' % (self.KtvApi, self.version, 
                            int(time.time()), quote(tsServiceTask.get_dogname()), self.lk)
        else:
            url = '%s/ProgramPatchService.aspx?op=getcloudappupdatelist' \
                    '&apptype=2&version=%s&minversion=0.0.0.0&os=linux&time=%d' \
                    '&dogname=%s' % (self.KtvApi, self.version, 
                            int(time.time()), quote(tsServiceTask.get_dogname()))
        logger.debug(url)
        maxver = None
        try:
            jsonobj = request_json(url, timeout=10, method='GET')
            logger.debug("read ProgramPatchService info: url:%s, result:%s" % (url, jsonobj))

            self.ver_val = VersionConvert(self.version)

            if jsonobj['result'] and jsonobj['result']['matches']:
                for upver in jsonobj['result']['matches']:
                    if (upver['app_maxver'] > 0 and self.ver_val > upver['app_maxver']) \
                            or (self.ver_val < upver['app_minver'] and self.ver_val != upver['app_curver']):
                        logger.debug("Ignore:  local:%d, min:%d, max:%d, upto:%d" \
                                % (self.ver_val, upver['app_minver'], upver['app_maxver'], upver['app_curver']))
                        continue
                    if not maxver:
                        maxver = upver
                    else:
                        if maxver['app_curver'] < upver['app_curver']:
                            maxver = upver
                        logger.debug("would upgrade to %s" % maxver['curver'])
                if not maxver:
                    logger.debug("no app update version found")
                    self._lastmsg = "Already on latest version"
                    return True
                self._lastmsg = "Downloading: %s" % maxver['app_url']
                fname = self.fu.filename(maxver['app_url'])
                self._lastmsg = "Download complete: %s" % fname
                
                tempfileName = "tmp_%s" % fname.split('.')[0]
                #下载并解压缩erp
                fileName = os.path.join(self.patchDir, fname)
                #检测文件是否存在，然后下载
                if os.path.exists(fileName) == False:
                    ret = self.fu.downfile(maxver['app_url'], fileName, None, None)
                    if not ret:
                        logger.error("Failed to download file %s->%s, will remove local file" % (maxver['app_url'], fileName))
                        os.remove(fileName)
                    self._lastmsg = "Downloaded upgrade file:%s" % fileName

                #检测文件夹是否存在，如果存在，删除重新解压缩
                if os.path.exists(self.tempDir) == True:
                    subprocess.getstatusoutput("rm -rf %s" % self.tempDir)

                if os.path.exists(self.tempDir) == False:
                    os.makedirs(self.tempDir)
                #很久之前解压缩后前要通过md5sum.txt将所有文件进行MD5值验证，现在没有这个文件就不需要验证了
                logger.debug("extrating file %s to folder %s" % (fileName, os.path.join(self.patchDir, tempfileName)))
                res = extract(fileName, self.tempDir)
                self._lastmsg = "extracted file %s to folder %s" % (fileName, self.tempDir)
                if res:
                    pkpath = self.searchTUP()
                    if not pkpath:
                        self._lastmsg = "extracted file failed(no tup file)"
                        logger.debug("cannot fine *.tup files")
                        return False

                    #not allow interactive mode till now
                    if maxver['app_isshow'] == 1 and self._interactive:
                        self._confirm = True
                        self._status = 'waiting'
                        self._lastmsg = maxver['app_desc']

                        #保存文件路径，留着确认之后再执行
                        self.fileName = fileName
                        self.maxver = maxver

                    else:
                        self._confirm = False
                        self.do_callback()
                else:
                    self._lastmsg = "Failed to extracted file %s to folder %s" % (fileName, self.tempDir)
                    #possible bad file, just remove it to wait download again.
                    if os.path.exists(fileName):
                        os.remove(fileName)
        except BadZipfile as ex:
            if os.path.exists(fileName):
                os.remove(fileName)
            self._lastmsg = str(ex)
        except Exception as ex:
            self._lastmsg = str(ex)
            print('upgrade failed %s(%s)' % (str(ex), tsServiceTask.get_dogname()));
            logger.error(traceback.format_exc())

        '''
        #查找一下，不在下载文件列表中的文件删除掉
        DownLoadFlag=False
        if len(Ulists)>0:
            for file in os.listdir(self.patchDir):
                DownLoadFlag=False
                file_path = os.path.join(self.patchDir, file)
                if os.path.splitext(file_path)[1]=='.zip':
                    print('file_path-', file_path);
                    for item in Ulists:
                        if item == self.fu.filename(file_path):
                            DownLoadFlag=True
                            break
                    if DownLoadFlag==False:
                        os.remove(file_path)
        '''
    def do_callback(self):
        if not self.fileName or not self.maxver:
            logger.debug("Illegal callback call")
            self._lastmsg = "Illegal callback call"
            return False
        #防止文件意外被改变，重新解压文件再执行升级
        #检测文件夹是否存在，如果存在，删除重新解压缩
        if os.path.exists(self.tempDir) == True:
            subprocess.getstatusoutput("rm -rf %s" % self.tempDir)

        if os.path.exists(self.tempDir) == False:
            os.makedirs(self.tempDir)
        #很久之前解压缩后前要通过md5sum.txt将所有文件进行MD5值验证，现在没有这个文件就不需要验证了
 
        res = extract(self.fileName, self.tempDir)
        self._lastmsg = "extracted file %s to folder %s" % (self.fileName, self.tempDir)
        if res:
            pkpath = self.searchTUP()
            if not pkpath:
                self._lastmsg = "extracted file failed(no tup file)"
                logger.debug("cannot fine *.tup files")
                return False
        #end: --防止文件意外被改变，重新解压文件再执行升级

        #TODO launch the upgrade service client side, from Shaolin
        #cmd = "LD_PRELOAD=/opt/lib/preloadable_libiconv.so LD_LIBRARY_PATH=/opt/lib /opt/thunder/bin/update/ThunderUpdateTools "\
        #         "-f '%s' -v '%s'" % (pkpath, maxver['curver'])
        cmd = "/opt/thunder/bin/update/ThunderUpdateTools -f '%s' -v '%s'" % (pkpath, self.maxver['curver'])
        logger.debug("Upgrade command:\n%s\n" % cmd)
        return True
        out = ''
        ret, out = subprocess.getstatusoutput(cmd)
        if ret == 0:
            logger.debug("Upgrade success")
            self._lastmsg = "Upgrade success"
        else:
            logger.error("Upgrade Failed")
            self._lastmsg = "Upgrade Failed"
        logger.debug("upgrade output:\n%s\n" % out.decode('utf-8'))
        self._lastrun = time.time()
        self._confirm = False
        self._status = ''


appUpgrade = _appUpgrade("upgrade")

if __name__ == "__main__":
    Upgrade = Upgrade("Upgrade")
