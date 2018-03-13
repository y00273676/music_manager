#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月14日

@author: yeyinlin
'''

from modules.dal.CodeExecDAL import CodeExecDAL
from common.dateutils import getYesterday

class CodeExecBLL(object):
    def __init__(self):
        self.dal=CodeExecDAL()
        pass

    def ExecuteProOrSql(self,sqlContent, type, result, dbName, ErpConnectionString):
        dt={}
        print (type,result)
        if type==0 and result==0:
            self.dal.ExecuteSqlWithoutResult(sqlContent, dbName, ErpConnectionString)
        elif type==0 and result==1:
            dt=self.dal.ExecuteSql(sqlContent, dbName, ErpConnectionString)
        elif type==1 and result==0:
            self.dal.ExecuteProc(sqlContent, dbName, ErpConnectionString)
        elif type==1 and result==1:
            dt=self.dal.ExecuteProc(sqlContent, dbName, ErpConnectionString)

    def ExecuteResult(self,sqlContent,sqlOrProc,isHasResult,dbName,ErpConnectionString,time):
        if "*" in sqlContent and "&" in sqlContent:
            sqlContent=(sqlContent.replace("*",time)).replace("&",getYesterday())
        self.ExecuteProOrSql(sqlContent, int(sqlOrProc), int(isHasResult), dbName, ErpConnectionString)
    
    def ExcuteSql(self,dbConnectionString, sql):
        self.dal.ExcuteSql(sql)

if __name__ == '__main__':
    pass




