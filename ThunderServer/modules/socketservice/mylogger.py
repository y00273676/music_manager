#!/usr/bin/python
# -*- coding: UTF-8 -*-

import io
import os
import posixpath
import select
import shutil
import sys
import time
import threading
import traceback
import re
import datetime
import codecs

from time import ctime,sleep
from queue import Queue

class MyLogger(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.maxsize = 4096;
        self.logname = '';
        self.logpath = '';
        self.queque = Queue()
        self.stopped = False
        self.started = False

    def open(self, logpath, logname, maxsize):
        self.maxsize = maxsize;
        self.logname = logname;
        
        if self.started == False:
            self.start()
            self.started = True;
        
        if not os.path.exists(logpath[0:2]):
            logpath = 'c' + logpath[1:]
        
        if not os.path.exists(logpath):
            try:
                os.makedirs(logpath)
            except:
                print('create ', logpath, 'failed')
        self.logpath = logpath;
        print('logpath ', self.logpath)

    def close(self):
        self.stopped=True
    
    def dolog(self, info, track=False):
        if track:
            try:
                fp = io.StringIO()
                traceback.print_exc(file=fp)
                value = fp.getvalue()
                lines = value.splitlines()
                info = 'error ' + lines[1] + ' ' + lines[len(lines)-1]
            except:
                traceback.print_exc()
                info = 'track error'
        
        if self.started==False:
            print('!!!!!!! log thread ',  self.name, 'not open !!!!!!')
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + (".%04d" % int(time.time()*10000%10000))
            log={}
            log['now'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + (".%03d" % int(time.time()*1000%1000))
            log['info'] = info
            self.queque.put(log)
        
        print('log', info)
    
    def run(self):
        print('****** log thread', self.name, 'start ******')
        while not self.stopped:
            log = None
            try:
                log = self.queque.get(1, 1)
            except:
                log = None
                time.sleep(2)
            if log != None:
                try:
                    szpath = self.logpath + "/" + time.strftime("%Y%m", time.localtime())
                    if not os.path.exists(szpath):
                        os.mkdir(szpath)
                    filename = szpath + "/" + self.logname + ".txt"
                    if os.path.exists(filename) and os.path.getsize(filename)>self.maxsize:
                        try:
                            now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                            name2 = szpath + "/" + self.logname + "_" + now + ".txt"
                            os.rename(filename, name2)
                        except:
                            traceback.print_exc()
                            print("rename failed");

                    f = open(filename, 'a')
                    f.write(log['now'] + " ")
                    f.write(str(log['info']))
                    f.write("\r\n")
                    f.close()

                    
                except:
                    traceback.print_exc()
                finally:
                     f.close()

#if __name__ == '__main__':
#    logger = MyLogger('logger_test', '.', 40960)
#    logger.dolog('xxxx')
