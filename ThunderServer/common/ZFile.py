#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年4月26日

@author: yeyinlin
'''
import zipfile
import os.path
import os
import logging
import traceback
import platform
logger = logging.getLogger(__name__)
   
class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)
          
    def addfile(self, path, arcname=None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        self.zfile.write(path, arcname)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)
              
    def close(self):
        self.zfile.close()
          
    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)
              
    def extract(self, filename, path):
        path = path.decode('gbk').encode('utf-8')
        if not filename.endswith('/'):
            #buildname = filename.encode("cp437").decode('gbk')
            buildname = filename.decode('gbk').encode('utf-8')
            if platform.system().lower() == 'linux':
                buildname = buildname.replace('\\', '/')
            f = os.path.join(path, buildname)
            _dname, _fname = os.path.split(f)
            if not os.path.exists(_dname):
                os.makedirs(_dname)
            open(f, 'wb').write(self.zfile.read(filename))   

def create(zfile, files):   
    z = ZFile(zfile, 'w')   
    z.addfiles(files)   
    z.close()   
      
def extract(zfile, path):
    z = ZFile(zfile)   
    try:
        z.extract_to(path.decode('utf-8'))   
        z.close()
        return True
    except:
        logger.error(traceback.format_exc())
        return False
if __name__ == '__main__':
    #extract('c:\\thunder\\apache\\htdocs\\modules\\16224d35abff90fbfc3123de29048917.zip','c:\\thunder\\apache\\htdocs\\modules\\16224d35abff90fbfc3123de29048917')
    extract('/opt/thunder/ktvservice/d19f400647e4194c5bb5aabb7e626ec7.tsres','/opt/thunder/ktvservice/tmp_d19f400647e4194c5bb5aabb7e626ec7')
   
