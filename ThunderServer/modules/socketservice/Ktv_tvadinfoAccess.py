#!/usr/bin/python
# -*- coding: UTF-8 -*-
from modules.model.ktv_tvadinfo import *

class Ktv_tvadinfoAccess():
    _ins=None
    @staticmethod
    def Ins(self):
        global _ins
        if _ins==None:
            _ins=Ktv_tvadinfoAccess()
        return _ins
    
    def Addktv_tvadlog(self):
        flag = False
        key = ktv_tvadlog()
        
        
    def ktv_tvadlog():
#         return string.Format("tvadlist_{0}_{1}",DateTime.Now.Day,DateTime.Now.Hour);
        return "tvadlist_"+str()+"_"+str()
    
    def ktv_tvadTimesKey():
#         return string.Format("tvadset_{0}_{1}", roomstatus,DateTime.Now.Day);
        return "tvadset_"+str()+"_"+str()
    
    def AddKtv_tvadTimes(_count):
        flag = False
        key = ktv_tvadTimesKey(_count.roomstatus)
#         if (!Redisset.Exists(key))
#             flag = True
        values = to_str(_count)
#         Redisset.zincrby(key, values, 1);
        if flag:
            pass
#             Redisset.Expire(key, 60 * 60 * 24 * 3);
        






