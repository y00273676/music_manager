#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import logging
import traceback
import sys

from config.appConfig import AppSet
from common.MysqlDbHelper import MysqlDbHelper
from common.tstypes import try_to_int

class Thunder():
    _ins = None
    _Karaokdbhelper = None
    _erpdbhelper = None

    @staticmethod
    def Ins():
        if not Thunder._ins:
            Thunder._ins = Thunder()

        return Thunder._ins

    #返回可使用的dbhelper  可通过 dbtype 区分是sqlserver 或 mysql
    @property
    def Karaokdbhelper(self):
        if Thunder._Karaokdbhelper:
            return Thunder._Karaokdbhelper
        else:
            try:
                istry = False
                print(AppSet().Karaok.mysqlconnstring)
                if MysqlDbHelper.Ins(AppSet().Karaok.mysqlconnstring).Connected():
                    print('连上了')
                    Thunder._Karaokdbhelper = MysqlDbHelper.Ins(AppSet().Karaok.mysqlconnstring)
                    #AppSet().SetCloudKtvIniValue("DBtype", 2)
                    return Thunder._Karaokdbhelper
                else:
                    print('没连上')
                    sys.exit(0)
                    if not istry:
                        istry = True

            except Exception as ex:
                logging.error('Karaokdbhelper excepted: %s' % str(ex))
                logging.error(traceback.format_exc())
                sys.exit(0)

            return None

    '''
    #返回可使用的dbhelper  可通过 dbtype 区分是sqlserver 或 mysql 
    @property
    def erpdbhelper(self):
        if Thunder._Karaokdbhelper:
            return Thunder._Karaokdbhelper
        else:
            try:
                istry = False
                appset = AppSet()
                dbtype = try_to_int(appset.DBtype, 1)
                if dbtype == 2:
                    if MysqlDbHelper.Ins(appset.Karaok.mysqlconnstring).Connected():
                        Thunder._Karaokdbhelper = MysqlDbHelper.Ins(appset.Karaok.mysqlconnstring)
                        appset.SetCloudKtvIniValue("DBtype", 2)
                        return Thunder._Karaokdbhelper
                    else:
                        if not istry:
                            istry = True
                
                if dbtype ==1 or istry:
                    if DbHelper.Ins(appset.Karaok.connstring).Connected():
                        Thunder._Karaokdbhelper = DbHelper.Ins(appset.Karaok.connstring)
                        appset.SetCloudKtvIniValue("DBtype", 1)
                        return Thunder._Karaokdbhelper
            except Exception as ex:
                logging.error('Karaokdbhelper excepted')
                logging.error(str(ex))
                logging.error(traceback.format_exc())

            logging.error('Get Karaokdbhelper Failed')
            return None
    '''


    #返回可使用的dbhelper  可通过 dbtype 区分是sqlserver 或 mysql 
    @property
    def erpdbhelper(self):
        if Thunder._erpdbhelper:
            return Thunder._erpdbhelper
        else:
            try:
                appset = AppSet()
                if DbHelper.Ins(appset.Erp.connstring).Connected():
                    Thunder._erpdbhelper = DbHelper.Ins(appset.Erp.connstring)
                    return Thunder._erpdbhelper

                if MysqlDbHelper.Ins(appset.Erp.mysqlconnstring).Connected():
                    Thunder._erpdbhelper = MysqlDbHelper.Ins(appset.Erp.mysqlconnstring)
                    return Thunder._erpdbhelper
            except Exception as ex:
                logging.error('erpdbhelper excepted')
                logging.error(str(ex))
                logging.error(traceback.format_exc())

            logging.error('Get erpdbhelper Failed')
            return None

if __name__ == '__main__':
    helper=Thunder().Ins().Karaokdbhelper
    res=helper.Query("select * from ktvmodule_ver")
    print (res)

'''
class ServerConnstring():
    #服务器IP
    _dbip = ''
    #用户名
    _user = ''
    #密码
    _pwd = ''
    #数据库名称
    _db = ''
    #程序名称
    _application = ''
    #连接字符串
    _connstring = ''
    #连接字符串
    _mysqlconnstring = ''

    @property
    def dbip(self):
        return self._dbip
    @dbip.setter
    def dbip(self, value):
        self._dbip = value

    @property
    def user(self):
        return self._user
    @user.setter
    def user(self, value):
        self._user = value

    @property
    def pwd(self):
        return self._pwd
    @pwd.setter
    def pwd(self, value):
        self._pwd = value

    @property
    def db(self):
        return self._db
    @db.setter
    def db(self, value):
        self._db = value

    @property
    def application(self):
        return self._application
    @application.setter
    def application(self, value):
        self._application = value

    @property
    def connstring(self):
        #return 'Application Name={4}; Data Source={0};User ID={1};Password={2};Initial Catalog={3};Pooling=true'.format(self._dbip, self._user, self._pwd, self._db, self._application) 
        return 'application={4}; host={0};user={1};password={2};db={3};Pooling=true'.format(self._dbip, self._user, self._pwd, self._db, self._application) 

    @property
    def mysqlconnstring(self):
        #return 'Data Source={0};User ID={1};Password={2};Initial Catalog={3};Pooling=true;CharSet=utf8;port=3306'.format(self._dbip, self._user, self._pwd, self._db)
        return 'host={0};user={1};password={2};db={3};Pooling=true;CharSet=utf8;port=3306'.format(self._dbip, self._user, self._pwd, self._db)
'''
