'''
Created on 2017年4月14日

@author: yeyinlin
'''
from modules.dal.ModuleVersionDAL import ModuleVersionDAL
class ModuleVersionBll(object):
    def __init__(self):
        self._dal=ModuleVersionDAL()
       
    def GetModuleVer(self):
        return self._dal.GetModuleVer()
    
    def AddModule(self,model):
        return self._dal.AddModule(model)
    
    def UpdateModule(self,moduleid):
        return self._dal.UpdateModule(moduleid);
    
    def GetModule(self):
        pass

if __name__ == '__main__':
    pass