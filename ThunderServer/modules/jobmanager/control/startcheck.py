#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月13日

@author: yeyinlin
'''
import logging
logger = logging.getLogger(__name__)

class startcheck(object):
    def __init__(self):
        self._appver=''
        pass
    def appver(self):
        logger.error("********************* TODO: the _appver data ***************************")
        if not self._appver:
            #TODO: get appver
#             FileVersionInfo myFileVersion = FileVersionInfo.GetVersionInfo(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ktvmoduleservice.exe"));
            #FileVersion
            return '0'
        return self._appver

if __name__ == '__main__':
    pass
