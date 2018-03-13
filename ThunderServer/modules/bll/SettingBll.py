#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月18日

@author: yeyinlin
'''
from modules.dal.SettingDAL import SettingDAL

class SettingBll(object):
    def __init__(self):
        self._dal=SettingDAL()
        pass

    def GetRooms(self):
        return self._dal.GetRooms()

    def GetRoomByDT(self):
        pass

    def SetSettingInfo(self, name, value):
        return self._dal.SetSettingInfo(name, value)

    def GetSettingInfo(self,name):
        return self._dal.GetSettingValue(name)
    
    def GetServer(self):
        return self._dal.GetServer()

    def getKaraokVer(self):
        return self._dal.GetKaraokVersion()


if __name__ == '__main__':
    bll=SettingBll()
    a=list(bll.GetServer())
    print(a)
