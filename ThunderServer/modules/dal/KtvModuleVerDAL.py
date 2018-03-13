#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月13日

@author: yeyinlin
'''
#from modules.jobmanager.db.dbhelper import dbhelper
from common.Thunder import * 
from time import strftime, localtime
import time
import datetime

import logging
logger = logging.getLogger(__name__)

class KtvModuleVerDAL():
    def __init__(self):
        self.helper=Thunder().Ins().Karaokdbhelper

    def GetModuleVer(self):
        try:
            sql = "select * from ktvmodule_ver order by addtime desc"
            data = self.helper.Query(sql)
            if data and len(data)>0:
                return data
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def DeleteVer(self,mid):
        try:
            sql = "delete from ktvmodule_ver where id='" + str(mid)+"'"
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def AddModule(self, ver):
        #先删除当前存在一样的
        try:
            self.DeleteVer(ver.id)
            mid = ver.id
            name = ver.name
            addtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(ver.addtime)))
            fileurl = ver.fileurl
            unpath = ver.unpath
            version = ver.version
            isuse = ver.isuse
            needun = ver.needun
            desc = ver.desc
            msgtime = ver.msgtime
            isshow = 1 if ver.isshow else 0
            bagtype = ver.bagtype
            isdefault = 1 if ver.isdefault else 0
            revision = 0.0 if not ver.reversion else dicimal(ver.reversion)
            vertype = ver.vertype
    
            sql = "update ktvmodule_ver set isuse=0 where isuse=1 and bagtype=" + str(bagtype) + ";"
            sql += "delete from ktvmodule_ver where id=" + str(mid) + ";"
            sql += "insert into ktvmodule_ver(id, name, addtime, fileurl, unpath,"\
                    "{0}version{1},isuse,needun,{0}desc{1}, msgtime,"\
                    "isshow,bagtype,isdefault,revision,vertype) "
            sql += " values(%d, '%s', '%s', '%s'," % (mid, name, addtime, fileurl)
            sql += " '%s', '%s', %d, %d," % (unpath, version, isuse, needun)
            sql += " '%s', '%s', %d, %d," % (desc, msgtime, isshow, bagtype)
            sql += " %d, '%s', %d);" % (isdefault, revision, vertype)
            
            sqlone=sql
            if AppSet().DBtype==1:
                sqlone=sql.format("[","]")
            else:
                sqlone=sql.format("`","`")
            return self.helper.ExecuteSql(sqlone)
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def UpdateModule(self,moduleid,bagtype):
        try:
            sql="update ktvmodule_ver set isuse=0 where isuse=1 and bagtype={0};"\
                    "update ktvmodule_ver set isuse=1 where id=%d and bagtype=%d;" % (moduleid, bagtype)
            return self.helper.ExecuteSql(sql) > 0
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

    def AddModule_Theme(self, theme):
        try:
            theme_id = theme.theme_id
            theme_name = theme.theme_name
            theme_desc = theme.theme_desc
            theme_path = theme.theme_path
            theme_unpath = theme.theme_unpath
            theme_type = theme.theme_type
            theme_date = theme.theme_date
            theme_author = theme.theme_author
            theme_state = theme.theme_state
            theme_bagtype = theme.theme_bagtype
    
            sql = "delete from themes where theme_id=%d;" % theme_id
            sql += "insert themes(theme_id,theme_name,theme_desc,theme_path,theme_unpath,"\
                    "theme_type,theme_date,theme_author,theme_state,theme_bagtype)"
            sql += " values(%d,'%s','%s','%s','%s'," % (theme_id, theme_name, theme_desc, theme_path, theme_unpath)
            sql += "'%s','%s','%s',%d,%d)" % (theme_type, theme_date, theme_author, theme_state, theme_bagtype)
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            logger.error(traceback.format_exc())
            return None 

    def UpdateModule_Theme(self,id):
        try:
            sql = "update themes set theme_state=0, theme_date=%s where theme_id=%d;" % (strftime("%Y-%m-%d %H:%M", localtime()), id)
            return self.helper.ExecuteSql(sql)
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
    
    def GetAllModule_Theme(self,state=1):
        try:
            sql = "select * from themes"
            if state>-1:
                sql+=" where theme_state=%d " % (state)
            if state==0:
                sql+=" and theme_date<'" + (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime("%Y-%m-%d %H:%M:%S")+"'"
            data=self.helper.Query(sql)
            if data and len(data)>0:
                return data[0]
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

# if __name__ == '__main__':
#     dal=KtvModuleVerDAL()
#     print (dal.GetModuleVer())
