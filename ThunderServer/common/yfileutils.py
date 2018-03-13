#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年4月6日

@author: yeyinlin
'''
import os
import zipfile
import sys


def getlistfile(path): 
    ret = [] 
    for root, dirs, files in os.walk(path):
        for filespath in files: 
            ret.append(os.path.join(root,filespath)) 
    return ret

def GetFileNameAndExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return shotname,extension

def unzip(path):
    zfile = zipfile.ZipFile(path,'r')
    for filename in zfile.namelist():
        data = zfile.read(filename)
        try:
            filename = filename.encode("mbcs").decode('utf8')
        except:
            filename = filename.encode("cp437").decode('mbcs')
        print(filename)
        file = open(filename, 'w+b')
        file.write(data)
        file.close()
    zfile.close()
    return True

def syncdata(module_path, Unpath, err_sb,type):
    
    return 1
    

if __name__ == '__main__':
    pass