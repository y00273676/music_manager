'''
Created on 2017年4月14日

@author: yeyinlin
'''
from modules.jobmanager.db.dbhelper import dbhelper
from common.Thunder import * 
from time import strftime, localtime
import time
import datetime
class ModuleVersionDAL(object):
    def __init__(self):
        self.helper=Thunder().Ins().Karaokdbhelper
        
    def GetModuleVer(self):
        try:
            sql = "select  * from moduleversion where modulebagtype=2 order by moduleid desc";
            data=self.helper.Query(sql)
            if data and len(data)>0:
                return data[0]
            else:
                return None
        except Exception as e:
            print("traceback.format_exc()",traceback.format_exc())
    def DeleteVer(self,id):
        try:
            sql = "delete from ModuleVersion where ModuleId='"+str(id)+"'"
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            print("traceback.format_exc()",traceback.format_exc())
            return None
        
    def AddModule(self,model):
        try:
            ModuleID=model['ModuleId']
            ModuleName=model['ModuleName']
            ModulePath=model['ModulePath']
            ModuleUnPath=model['ModuleUnPath']
            ModuleVersion=model['_ModuleVersion']
            ModuleIsUser=model['ModuleIsUser']
            ModuleNeedun=model['ModuleNeedun']
            ModuleDesc=model['ModuleDesc']
            ModuleMsgTime=model['ModuleMsgTime']
            ModuleIsShow=model['ModuleIsShow']
            ModuleBagType=model['ModuleBagType']
            ModuleIsDefault=model['ModuleIsDefault']
            sql="INSERT INTO [ModuleVersion]"
            sql+="(ModuleId,ModuleName, ModuleDate, ModulePath, ModuleUnPath, ModuleVersion, ModuleIsUser, ModuleNeedun, ModuleIsSkip,ModuleDesc,ModuleMsgTime, ModuleIsShow, ModuleBagType,ModuleIsDefault) values ("
            sql+="'"+str(ModuleID)+"'," 
            sql+="'"+str(ModuleName)+"'," 
            sql+="'"+str(strftime("%Y-%m-%d %H:%M", localtime()))+"'," 
            sql+="'"+str(ModulePath)+"'," 
            sql+="'"+str(ModuleUnPath)+"'," 
            sql+="'"+str(ModuleVersion)+"'," 
            sql+="'"+str(ModuleIsUser)+"'," 
            sql+="'"+str(ModuleNeedun)+"'," 
            sql+="'"+str(ModuleDesc)+"'," 
            sql+="'"+str(ModuleMsgTime)+"'," 
            sql+="'"+str(ModuleIsShow)+"'," 
            sql+="'"+str(ModuleBagType)+"'," 
            sql+="'"+str(ModuleIsDefault)+"')" 
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            print("traceback.format_exc()",traceback.format_exc())
            return None
    
    def UpdateModule(self,moduleid):
        try:
            sql = "update ModuleVersion set ModuleIsUser=0 where ModuleIsUser=1;update ModuleVersion set ModuleIsUser=1 where ModuleId='" + str(moduleid)+"'";
            return self.helper.ExecuteSql(sql) > 0
        except Exception as e:
            print("traceback.format_exc()",traceback.format_exc())
            return None
    
  
if __name__ == '__main__':
    pass