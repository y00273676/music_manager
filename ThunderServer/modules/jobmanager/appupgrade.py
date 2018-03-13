#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import platform
import json

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


from common.Thunder import Thunder
from common.KtvInfo import KtvInfo
from common.fileutils import fileUtils
from common.utils import VersionConvert
from common.ZFile import extract
from config.appConfig import AppSet
from modules.bll.SettingBll import SettingBll
from zipfile import BadZipfile

import platform
import logging
#from modules.jobmanager.db.dbhelper import dbhelper

logger = logging.getLogger(__name__)

class appUpgrade():
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('KtvInfo singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(appUpgrade, cls).__new__(cls, *args, **kwargs)
                    cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('KtvInfo singleton is exists')
        return cls.__instance


    def __init__(self):
        self.setbll = SettingBll()
        self.ktvid = 0
        self.dogname = None
        #self.iswork=False
        self.patchDir = os.path.join(AppSet()._trandownpath, 'appUpdate')
        self.tempDir = os.path.join(AppSet().tempDir, 'Upgrade')
        self.helper = Thunder().Ins().Karaokdbhelper
        self.ktvinfo = self.getKtvInfo()
        self.dogname = self.getDogname()
        self.transip = self.getTransIP()
        self.version = self.setbll.getKaraokVer()
        self.fu = fileUtils('appupgrade')
        self.lk = KtvInfo().lk


        print(self.dogname, self.transip, self.version)

        #从网卡上找到所有transferIPStr是否存在，如果存在才可以额调用
        #if self.transferIPStr!=""：
        #self.iswork=True

        #if self.iswork==True:
        #    self.tsfStart()
    def searchTUP(self):
        for f in os.listdir(self.tempDir):
            if f.endswith(".tup"):
                return os.path.join(self.tempDir, f)
        return ''

    def getDogname(self):
        return AppSet().get_DogName()

    def getKtvInfo(self):
        return KtvInfo()._info

    def getTransIP(self):
        try:
            sql = "select config_value from config where config_name='中转服务器IP'"
            data = self.helper.Query(sql)
            if data and len(data)>0:
                return data[0]['SettingInfo_Value']
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def UpdateApp(self):
        if os.path.exists(self.patchDir)==False:
            os.makedirs(self.patchDir)
        if self.dogname == None:
            time.sleep(113)
        #这里需要打印加密狗，然后调用接口需要解密狗名称进行验证
        logger.debug('DogName:' + self.dogname)
        if self.lk == 1 or self.lk == 2:
            self.url = '%s/ProgramPatchService.aspx?op=getcloudappupdatelist' \
                    '&apptype=2&version=%s&minversion=0.0.0.0&os=linux&time=%d' \
                    '&dogname=%s&lk=%d' % (AppSet().KtvApi, self.version, 
                            int(time.time()), quote(self.dogname), self.lk)
        else:
            self.url = '%s/ProgramPatchService.aspx?op=getcloudappupdatelist' \
                    '&apptype=2&version=%s&minversion=0.0.0.0&os=linux&time=%d' \
                    '&dogname=%s' % (AppSet().KtvApi, self.version, 
                            int(time.time()), quote(self.dogname))
        maxver = None
        try:
            req = urlopen(self.url)
            retstr = req.read()
            data = unquote(retstr)
            jsonobj = json.loads(data)
            logger.debug("read ProgramPatchService info: url:%s, result:%s" % (self.url, jsonobj))

            self.ver_val = VersionConvert(self.version)

            print(self.version, self.ver_val)
            if jsonobj['result'] and jsonobj['result']['matches']:
                for upver in jsonobj['result']['matches']:
                    if (upver['app_maxver'] > 0 and self.ver_val > upver['app_maxver']) \
                            or (self.ver_val < upver['app_minver'] and self.ver_val != upver['app_curver']):
                        logger.debug("local:%d, min:%d, max:%d, upto:%d" \
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
                    return True
                fname = self.fu.filename(maxver['app_url'])
                
                tempfileName = "tmp_%s" % fname.split('.')[0]
                #下载并解压缩erp
                fileName = os.path.join(self.patchDir, fname)
                #检测文件是否存在，然后下载
                if os.path.exists(fileName) == False:
                    ret = self.fu.downfile(maxver['app_url'], fileName, None, None)
                    if not ret:
                        logger.error("Failed to download file %s->%s, will remove local file" % (maxver['app_url'], fileName))
                        os.remove(fileName)

                #检测文件夹是否存在，如果存在，删除重新解压缩
                if os.path.exists(self.tempDir) == True:
                    subprocess.getstatusoutput("rm -rf %s" % self.tempDir)

                if os.path.exists(self.tempDir) == False:
                    os.makedirs(self.tempDir)
                #很久之前解压缩后前要通过md5sum.txt将所有文件进行MD5值验证，现在没有这个文件就不需要验证了
                logger.debug("extrating file %s to folder %s" % (fileName, os.path.join(self.patchDir, tempfileName)))
                res = extract(fileName, self.tempDir)
                if res:
                    pkpath = self.searchTUP()
                    if not pkpath:
                        return False
                    #TODO launch the upgrade service client side, from Shaolin
                    cmd = "LD_PRELOAD=/opt/lib/preloadable_libiconv.so LD_LIBRARY_PATH=/opt/lib /opt/thunder/bin/update/ThunderUpdateTools "\
                             "-f '%s' -v '%s'" % (pkpath, maxver['curver'])
                    logger.debug("Upgrade command:\n%s\n" % cmd)
                    out = ''
                    ret, out = subprocess.getstatusoutput(cmd)
                    if ret == 0:
                        logger.debug("Upgrade success")
                    else:
                        logger.error("Upgrade Failed")
                    logger.debug("upgrade output:\n%s\n" % out.decode('utf-8'))
        except BadZipfile as ex:
            if os.path.exists(fileName):
                os.remove(fileName)
        except Exception as ex:
            print('upgrade failed %s(%s)' % (str(ex), self.dogname));
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

if __name__ == "__main__":
    Upgrade = Upgrade("Upgrade")
