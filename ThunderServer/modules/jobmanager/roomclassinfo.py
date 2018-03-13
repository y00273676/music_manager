#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年4月6日
房台信息
@author: yeyinlin
'''

from modules.model.Roominfo import Roominfo
from modules.bll.SettingBll import SettingBll
class roomclassinfo():
    __singleton = None
    @staticmethod
    def get_instance():
        if roomclassinfo.__singleton is None:
            roomclassinfo.__singleton = roomclassinfo('roomclassinfo')
        return roomclassinfo.__singleton
    def __init__(self,name):
        self._room_dict={}
        self._bll=SettingBll()
        self.start()
    def start(self):
        self.updatejob()
        return True
    def updatejob(self):
        list=self._bll.GetRooms()
        if list and len(list)>0:
            self._room_dict.clear()
            for ri in list:
                self._room_dict[ri["room_ip"]]=ri


def getRooms():
    list=[]
    room ={}
    room['room_name']='101'
    room['room_mac']='xxxxxxxxxxxx'
    room['room_ip']='192.168.0.101'
    room['room_class_name'] = '101'
    list.append(room)
    return list

if __name__ == '__main__':
    roomclassinfo=roomclassinfo().get_instance()
    roomclassinfo.start()
    print(roomclassinfo._room_dict)
    