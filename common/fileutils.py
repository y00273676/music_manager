#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import traceback
import logging
import hashlib

from ctypes import *

if sys.version_info < (3,):
    from urllib2 import urlopen
    from urllib2 import quote,unquote
else:
    from urllib.request import urlopen
    from urllib.parse import quote,unquote

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger(__name__)

class fileUtils():
    def __init__(self, name):
        self.name = name

    def save(self, filename, content, mylog=None):
        rt = False
        try:
            f = open(filename, 'wb')
            f.write(content)
            rt = True
        except:
            logger.error(traceback.format_exc())
            if mylog!=None:
                mylog.dolog('save', True)
            print('savefile',filename, content, 'failed')
        finally:
            f.close()

        return rt
    
    def read(self, filename, mylog=None):
        data = None
        f = None
        try:
            if filename.startswith('http://') or filename.startswith('https://'):
                #check python version
                req = urlopen(filename)
                data = req.read()
            else:
                if os.path.exists(filename):
                    f = open(filename, 'rb')
                    data = f.read()
        except:
            logging.error(traceback.format_exc())
            if mylog!=None:
                mylog.dolog('save', True)
            print('readfile', filename, 'failed')
        finally:
            if f!=None:
                f.close()
        return data
    
    def size(self, filename, mylog=None):
        size = -1
        if os.path.exists(filename):
            size = os.path.getsize(filename)
        else:
            if mylog!=None:
                mylog.dolog('not exist: ' + filename)

        return size

    def append(self, filename, content, mylog=None):
        try:
            f = open(filename, 'ab')
            f.write(content)
        except:
            logger.error(traceback.format_exc())
            if mylog!=None:
                mylog.dolog('save', True)
#             print('savefile',filename, info, 'failed')
        finally:
            f.close()

        return self.size(filename)

    def filename(self, filepath, mylog=None):
        fpath, fname = os.path.split(filepath)
        return fname
    
    def downfile(self, url, filename, md5sum=None, mylog=None):
        logger.info("request download file: %s -> %s" % (url, filename))
        if os.path.exists(filename) and (md5sum==None or self.md5sum(filename)==md5sum):
            logger.info("request download file: %s -> %s, skipped" % (url, filename))
            return True
        
        sztemp = filename + '.tmp';
        try:
            req = urlopen(url)
            with open(sztemp, "wb") as code:
                code.write(req.read())
                code.close()
            os.rename(sztemp, filename)
        except Exception as e:
            logger.error(traceback.format_exc())
            if mylog!=None:
                mylog.dolog('down', True);
        
        if os.path.exists(filename) and (md5sum==None or self.md5sum(filename)==md5sum):
            return True
        else:
            return False

    def md5sum(self, filename):
        m2 = hashlib.md5()
        data = self.read(filename)
        if data!=None:
            m2.update(data)
            return m2.hexdigest()
        else:
            return None

if __name__ == '__main__':
    fu = fileUtils('abc')
    aa=fu.downfile("https://ks3-cn-beijing.ksyun.com/sysres-bj/other/images/ef29122ae7600832c3d56b60fc134039.png", "e:\\log\\aaa.jpg", None,"shfjsdahkfhka")
    print (aa)  
