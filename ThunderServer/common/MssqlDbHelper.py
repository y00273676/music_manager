#!/usr/bin/env python
#! -*- encoding:utf-8 -*-


import logging
import traceback
import pymssql


class DbHelper():
    _ins = None
    _dbtype = 1
    def __init__(self, host, user, passwd, db,port=1433, charset='utf8', as_dict=True):
        self._host = host
        self._user = user
        self._pwd = passwd
        self._port=port
        self._charset=charset
        self._as_dict=as_dict
        self._db = db
        self._cur = None
        self._conn = None

    @staticmethod
    def Ins(connstr):
        if not DbHelper._ins:
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
            DbHelper._ins = DbHelper(host, user, passwd, db)

        return DbHelper._ins

    def Connected(self):
        try:
            if self._cur:
                self._cur.close()

            if self._conn:
                self._conn.close()

            self._conn = pymssql.connect(host=self._host,user=self._user, password=self._pwd, database=self._db,port=self._port,charset=self._charset)
            self._cur = self._conn.cursor()
            return True
        except Exception as ex:
            logging.error('Connect {0} {1} excepted'.format(self._host, self._db))
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
                logging.error('ExecuteQuery excepted:{0}'.format(sql))
                logging.error(str(ex))
                logging.error(traceback.format_exc())
            finally:
                if self._cur:
                    self._cur.close()
                if self._conn:
                    self._conn.close()
                self._conn = None
                self._cur = None
        logging.debug('ExecuteQuery sql {0}\n result:\n {1}'.format(sql, res))
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
        logging.debug('ExecuteNonQuery sql {0}\n result:\n {1}'.format(sql, res))
        return res

    @property
    def dbtype(self):
        return self._dbtype 

    @dbtype.setter
    def dbtype(self, value):
        self._dbtype = value

    def Query(self, sql):
        return self.ExecuteQuery(sql)
