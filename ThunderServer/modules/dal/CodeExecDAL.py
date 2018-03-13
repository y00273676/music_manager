#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月14日

@author: yeyinlin
'''
#from modules.jobmanager.db.dbhelper import dbhelper
from common.MysqlDbHelper import MysqlDbHelper as dbhelper
from common.Thunder import * 
from time import strftime, localtime
import time
import datetime
class CodeExecDAL(object):
    def __init__(self):
        self.helper=Thunder().Ins().Karaokdbhelper
#         self.erphelper=Thunder().Ins().erpdbhelper
        
    def ExecuteSql(self,sqlContent,erpConn, ErpConnectionString):
        if erpConn and erpConn.lower() != "karaok":
            data=self.erphelper.Query(sqlContent)
        else:
            data=self.helper.Query(sqlContent)
        if data and len(data)>0:
            return data[0]
        else:
            return None

    def ExecuteSqlWithoutResult(self,sqlContent,erpConn,ErpConnectionString):
        if erpConn and erpConn.lower()!="karaok":
            data=self.erphelper.ExecuteSql(sqlContent)
        else:
            data=self.helper.ExecuteSql(sqlContent)
        if data and len(data)>0:
            return data[0]
        else:
            return None
    
    def ExecuteProc(self,sqlContent,erpConn,ErpConnectionString):
        return self.helper.ExecuteSqlProc(sqlContent)
    
    def ExecuteProcWithoutResult(self,sqlContent,erpConn,ErpConnectionString):
        return self.helper.ExecuteSqlProc(sqlContent)
    
    def ExcuteSql(self,sql):
        return self.helper.ExecuteSql(sql)

if __name__ == '__main__':
    pass
