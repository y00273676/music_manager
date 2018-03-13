#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月7日
执行在线数据库语句
@author: yeyinlin
'''
from config.appConfig import AppSet
from common.KtvInfo import KtvInfo
from common.yhttp import yhttp
from common.fileutils import fileUtils
import json
from modules.model.YCode import Code
import os
from modules.bll.CodeExecBLL import CodeExecBLL

class codeexec():
    def __init__(self):
        self.ktvinfo=KtvInfo()._info
        self.basecodeurl=os.path.join(AppSet().BaseDirectory,'Code')
        self.bll=CodeExecBLL()

    def runexec(self):
        res_list=self.getsqlscript()
        if res_list:
            self.executecode(res_list)
    
    def getsqlscript(self):
        baseurl=AppSet().GetCloudKtvIniValue('Alter90URL')
        endurl="/CodeService.aspx?"
        param="op=getonlyoncejson&dogname="+yhttp().UrlEncode(str(AppSet()._dogname))+"&storeId="+str(self.ktvinfo._ktvid)
        print(baseurl+endurl+param)
        res=yhttp().get_y(baseurl+endurl+param)
        res=json.loads(res)
        if res['code']==1 and res['result']:
            return res['result']['matches']
        return None

    """
        "cachekey": "",
    "CodeID": 16,
    "SqlOrProc": 0,
    "CodeTime": "/Date(1453562963000)/",
    "IsDel": false,
    "CodeName": "删除ktvcloud_content表数据",
    "CodeContent": "http://sysres.ktvdaren.com/sysres/ktvdata/code/20160128134204.txt",
    "IsHasResult": false,
    "Days": -1,
    "DbName": "karaok",
    "execrange": 0"""
    def executecode(self,exelist):
        fu = fileUtils('fileUtils')
#         exelist=self.getlist()
        if exelist and len(exelist)>0:
            for model in exelist:
                try:
                    codeContentUrl=model['CodeContent']
                    sqlOrProc=model['SqlOrProc']
                    codeContent=model['CodeContent']
                    isHasResult=model['IsHasResult']
                    dbName=model['DbName']
                    time=model['CodeTime']
                    #获取执行文件的路径
                    codepath=os.path.join(self.basecodeurl,os.path.basename(codeContentUrl))
                    if not os.path.exists(self.basecodeurl):
                        os.mkdir(self.basecodeurl)
                        #下载文件
                    print("codepath",codepath)
                    res=fu.downfile(codeContentUrl,codepath)
                    print(res)
                    if res:
                        str = open(codepath).read()
                        splits=str.split("GO")
                        for sp in splits:
                            if not sp:
                                continue
                            print("执行",dbName)
                            print(sqlOrProc )
#                             self.execsql(sp, sqlOrProc, isHasResult, dbName,"thunderErpConnStr", time)
                        
#                         os.remove(codepath)
                except Exception as e:
                    print(e)
                pass
    def execsql(self,sql,sqlOrProc,isHasResult,dbName,str,time):
        return self.bll.ExecuteResult(sql, sqlOrProc, isHasResult, dbName, str, time)
               
    def getlist(self):
        list=[]
        code=Code()
        code._codeID=1
        code._sqlOrProc="1"
        code._codeContent="select * from ktvmodule_ver"
        code._isHasResult="1"
        code._dbName="smart"
        code._codeTime="1"
        list.append(code)
        return list    
        
        
        
if __name__ == '__main__':
    yexec=codeexec()
    yexec.runexec()
