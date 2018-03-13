#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2017年4月6日
清除缓存
@author: yeyinlin
'''
import logging
import os.path
import time
import os
import logging
from config.appConfig import AppSet
from common.yfileutils import getlistfile
import codecs
import traceback

import logging
logger = logging.getLogger(__name__)

class clearcache(object):
    def __init__(self,name):
        self.A_DAY=86400
        self.A_MIN=60
        self.curclear=AppSet().ApachFileDownPath

    def start(self):
        return True
    
    def cleardir(self, dpath):
        try:
            if os.path.exists(dpath):
                logging.warn("删除目标文件夹下的过期文件：" + dpath)
                #获取目录下的文件
                fs = getlistfile(dpath)
                size = 0
                isfull = False
                time = (self.A_DAY) * 15
                self.deleteexpirefile(fs,time)
                fs = getlistfile(dpath)
                for f in fs:
                    try:
                        size += int(os.path.getsize(f))
                        #TODO
                        if size > self.apacheCacheSize():
                            isfull = True
                            break
                        pass
                    except Exception as e:
                        pass
                if isfull:
                    time = self.A_MIN * 30
                    self.deleteexpirefile(fs, self.A_MIN*30)
            else:
                logger.debug("清理目录（%s）不存在" % dpath)

        except Exception as e:
            logger.error(traceback.format_exc())
    
    def apacheCacheSize(self):
        app = AppSet()
        cf = app.cloudktvini
        cf.readfp(codecs.open(app.cloudktvsong_ini, "r", 'utf_8_sig'))
        size = cf.get('CloudKtvSong', "ApacheCacheSize")
        return size
    
    #删除失效的文件   
    def deleteexpirefile(self, fs, expire):
        for info in fs:
            logging.debug("准备删除文件" + info)
            mtime = os.path.getmtime(info)
            ctime = time.time()
            if int(ctime) - int(mtime) > expire:
                try:
                    os.remove(info)
                    logging.error("删除文件成功:" + info)
                except Exception as e:
                    logger.error(traceback.format_exc())

if __name__ == '__main__':
    cache=clearcache('name')
    cache.cleardir(cache.curclear)
