#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''

@author: yeyinlin
'''
from config.appConfig import AppSet
from modules.jobmanager.control.scp import writefile, deletefile
from ctypes import CDLL, create_string_buffer
import os
import sys
from _ctypes import pointer
import time
from modules.bll.SettingBll import SettingBll

class synchronousutils(object):
    def __init__(self):
        self.dbtype=AppSet().DBtype
        self.setbll=SettingBll()
        basename = "lib/modulesyn.dll"
        cwd = os.path.dirname(os.getcwd())
        start=cwd.split("ThunderServer")[0]
        self.syfilename = os.path.join(start+"ThunderServer", basename)
        
    #同步文件还文件夹 1为文件 2 为文件夹
    def synfiletoserver(self,localpath,filepath,filetype):
        return True
        if int(self.dbtype)==1:
            self.synfiletoWin(localpath,filepath,filetype)
        elif int(self.dbtype)==2:
            self.synfiletolinux(localpath,filepath,filetype)
        return 1

    #删除文件       
    def deletefilefromserver(self,filepath,filetype=1):
        return True
        if int(self.dbtype)==1:
            self.deletefilefromwin(filepath,filetype)
        elif int(self.dbtype)==2:
            self.deletefilefromlinux(filepath,filetype)
        return 1

    #向linux 同步        
    def synfiletolinux(self,localpath,filepath,filetype):
        return True
        username ='root'
        password ='Thunder'
        execpath = os.path.join(AppSet().ApachPath, str(int(time.time()))+'.txt')
        #self.servers 需要获取所有视频服务器的ip地址
        servers = list()
        for item in  self.setbll.GetServer():
            servers.append(item['FileServer_IpAddress'])
        writefile(execpath,username,password,servers,(localpath.rstrip("/")).replace('/', '\\'),filepath.rstrip("/"))

    #向win 同步        
    def synfiletoWin(self,localpath,filepath,filetype):
        return True
        dllpath = self.syfilename
        dll = CDLL(dllpath)
        fileserver = create_string_buffer(1024)
        rt3 = dll.syncdirectorydata(localpath.replace('/', '\\').encode(),filepath.replace('/', '\\').encode() , pointer(fileserver))
        
    #删除win
    def deletefilefromwin(self,filepath,filetype):
        return True
        dllpath = self.syfilename
        dll = CDLL(dllpath)
        fileserver = create_string_buffer(1024)
        #删除文件
        return dll.deletedirectioryfile(filepath.replace('/', '\\').encode(),2, pointer(fileserver))
        
    
    #删除linux
    def deletefilefromlinux(self,filepath,filetype):
        return True
        username ='root'
        password ='Thunder'
        execpath=os.path.join(AppSet().ApachPath,str(int(time.time()))+'.txt')
        #self.servers 需要获取所有视频服务器的ip地址
        servers=list()
        for item in  self.setbll.GetServer():
            servers.append(item['FileServer_IpAddress'])
        deletefile(execpath,username,password,servers,filepath.rstrip("/"))
        
if __name__ == '__main__':
    pass
