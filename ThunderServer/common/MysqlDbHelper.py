#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import pymysql
import logging
import traceback

class MysqlDbHelper():
    _ins = None
    _dbtype = 2
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        self._host = host
        self._user = user
        self._pwd = passwd
        self._db = db
        self._port = port
        self._charset = charset
        self._cur = None
        self._conn = None

    @staticmethod
    def Ins(connstr):
        if not MysqlDbHelper._ins:
            #parse connstr to call init method
            t_connstr = connstr.strip()
            t_dict = dict(((lambda i:(i[0], i[1]))(l.split('=')) for l in t_connstr.split(';')))
            host = '127.0.0.1'
            user = 'sa'
            passwd = ''
            db = ''
            if 'host' in  t_dict.keys():
                host = t_dict['host']
            if 'user' in t_dict.keys():
                user = t_dict['user']
            if 'password' in t_dict.keys():
                passwd = t_dict['password']
            if 'db' in t_dict.keys():
                db = t_dict['db']
            MysqlDbHelper._ins = MysqlDbHelper(host, user, passwd, db)

        return MysqlDbHelper._ins

    def Connected(self):
        try:
            if self._cur:
                self._cur.close()

            if self._conn:
                self._conn.close()

            self._conn = pymysql.connect(host=self._host, user=self._user, passwd = self._pwd, db = self._db, port=self._port, charset=self._charset, cursorclass = pymysql.cursors.DictCursor)
            self._cur = self._conn.cursor()
            self._cur.execute('SET NAMES UTF8') 
            return True
        except Exception as ex:
            logging.error('Connect %s %s excepted' % (self._host, self._db))
            logging.error(str(ex))
            logging.error(traceback.format_exc())
            if self._cur:
                self._cur.close()
                self._cur = None
            if self._conn:
                self._conn.close()
                self._conn = None
            return False

 	#执行查询语句
    def ExecuteQuery(self, sql):
        res = None
        if self.Connected():
            try:
                self._cur.execute(sql)
                res = self._cur.fetchall()
            except Exception as ex:
                self._conn.rollback() 
                logging.error('ExecuteQuery excepted:%s' % (sql))
                logging.error(str(ex))
                logging.error(traceback.format_exc())
            finally:
                if self._cur:
                    self._cur.close()
                if self._conn:
                    self._conn.close()
                self._conn = None
                self._cur = None
        logging.debug('ExecuteQuery sql %s\n result:\n %s' % (sql, res))
        return res

    def ExecuteProc(self, sql):
        res = None
        if self.Connected():
            try:
                self._cur.callproc(sql)
                res = self._cur.fetchall()
            except Exception as ex:
                self._conn.rollback() 
                logging.error('ExecuteQuery excepted:%s' % (sql))
                logging.error(str(ex))
                logging.error(traceback.format_exc())
            finally:
                if self._cur:
                    self._cur.close()
                if self._conn:
                    self._conn.close()
                self._conn = None
                self._cur = None
        logging.debug('ExecuteQuery sql %s\n result:\n %s' % (sql, res))
        return res

    #执行非查询语句
    def ExecuteNonQuery(self, sql):
        res = False
        if self.Connected():
            try:
                self._cur.execute(sql)
                self._conn.commit()
                res = True
            except Exception as ex:
                self._conn.rollback() 
                logging.error('ExecuteNonQuery excepted:{0}'.format(sql))
                logging.error(str(ex))
                logging.error(traceback.format_exc())
            finally:
                if self._cur:
                    self._cur.close()
                    self._cur = None
                if self._conn:
                    self._conn.close()
                    self._conn = None
        logging.debug('ExecuteNonQuery sql %s\n result:\n %s' % (sql, res))
        return res

    @property
    def dbtype(self):
        return self._dbtype 

    @dbtype.setter
    def dbtype(self, value):
        self._dbtype = value
    
    def Query(self, sql):
        return self.ExecuteQuery(sql)
    
    def ExecuteSql(self,sql):
        return self.ExecuteNonQuery(sql)
    
    def ExecuteSqlProc(self,sql):
        return self.ExecuteProc(sql)
