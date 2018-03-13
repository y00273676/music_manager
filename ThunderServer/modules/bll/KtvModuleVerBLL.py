#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月13日

@author: yeyinlin
'''

from modules.dal.KtvModuleVerDAL import KtvModuleVerDAL
from modules.model.KtvModule_Ver import KtvModule_Ver
from modules.model.Ktvmodule_theme import Ktvmodule_theme
class KtvModuleVerBll(object):
    def __init__(self):
        pass
    def GetModuleVer(self):
        mlist = KtvModuleVerDAL().GetModuleVer()
        res_list = []
        if mlist:
            if len(mlist)>0:
                for item in mlist:
                    var = KtvModule_Ver()
                    var.msgtime = item['msgtime']
                    var.version = item['version']
                    var.fileurl = item['fileurl']
                    var.desc = item['desc']
                    var.addtime = item['addtime']
                    var.needun = item['needun']
                    var.revision = item['revision']
                    var.bagtype = item['bagtype']
                    var.unpath = item['unpath']
                    var.name = item['name']
                    var.isshow = item['isshow']
                    var.id = item['id']
                    var.isuse = item['isuse']
                    var.vertype = item['vertype']
                    var.isdefault = item['isdefault']
                    res_list.append(var)
        return res_list

    def AddModule(self,ver):
        return KtvModuleVerDAL().AddModule(ver)

    def DeleteVer(self,id):
        return KtvModuleVerDAL().DeleteVer(id)

    def AddModule_Theme(self,ver):
        return KtvModuleVerDAL().AddModule_Theme(ver)

    def GetAllKtvModule_Theme(self,ver=-1):
        arr=[]
        obj=KtvModuleVerDAL().GetAllModule_Theme(ver)
        if obj:
            theme = Ktvmodule_theme()
            theme.theme_id = obj['theme_id']
            theme.theme_type = obj['theme_type']
            theme.theme_name = obj['theme_name']
            theme.theme_bagtype = obj['theme_bagtype']
            theme.theme_unpath = obj['theme_unpath']
            theme.theme_desc = obj['theme_desc']
            theme.theme_date = obj['theme_date']
            theme.theme_state = obj['theme_state']
            theme.theme_path = obj['theme_path']
            theme.theme_author = obj['theme_author']
            arr.append(theme)
        return arr

    def UpdateModule_Theme(self,ver):
        return KtvModuleVerDAL().UpdateModule_Theme(id)

    def GetKtvmodule_themeByDT(self,data):
        return {}

    def GetModule(self):
        pass
  

if __name__ == '__main__':
    aa=KtvModuleVerBll().GetModuleVer()
    print(aa)
    

    
