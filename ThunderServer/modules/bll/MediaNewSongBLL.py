#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月14日

@author: yeyinlin
'''
from modules.dal.MediaNewSongDAL import MediaNewSongDAL
class MediaNewSongBLL(object):
    def __init__(self):
        self.dal=MediaNewSongDAL()
        
    def ResetSort(self):
        self.dal.ResetSort()
    
    def GetMediaIdbySerialNo(self,no):
        return self.dal.GetMediaIdbySerialNo(no)
    
    def GetMediaNewSongTime(self):
        return self.dal.GetMediaNewSongTime()
    
    def GetSongValidtime(self):
        return self.dal.GetSongValidtime()
    
    def insertMediaNewsong(self, media_ID, time, no):
        return self.dal.InsertMediaNewsong(media_ID, time, no)
        
if __name__ == '__main__':
    dal=MediaNewSongBLL()
    print(dal.GetSongValidtime())
