#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setting import DB
import MySQLdb
import MySQLdb.cursors
import time
import sys


class mainSource(object):

    def __init__(self,conf):
        self.conf = conf
        self.data = []
        self.idx = 0
        self.r= None

    def GetScheme(self):

        return [
            ('docid',{'docid':True}),
            ('aid',{'type':'integer'}),
            ('name',{'type':'string_text'}),
            ('jp',{'type':'string_text'}),
            ('py',{'type':'string_text'}),
            ('ano',{'type':'integer'}),
        ]

    def GetFieldOrder(self):
        return [('name','jp','py')]

    def Connected(self):

        try:
            self.dbconn = MySQLdb.connect(host=DB['host'],port=DB['port'],user=DB['user'],passwd=DB['pass'],db=DB['dbname'],charset=DB['charset'],cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor = self.dbconn.cursor()
        except Exception,ex:
            print ex
            if self.cursor:
                self.cursor.close()
            if self.dbconn:
                self.dbconn.close()
        return True

    def OnBeforeIndex(self):

        limit_record = (self.conf.has_key('limit') and ' LIMIT '+ str(self.conf['limit'])) or ''
        sql = 'select * from actors %s'%(limit_record)
        try:
            self.cursor.execute(sql)
            self.data = self.cursor.fetchall()
            if self.cursor:
                self.cursor.close()
            if self.dbconn:
                self.dbconn.close()
            if len(self.data) < 10: 
                sys.exit(-1)
        except Exception, ex: 
            #logging.error("query: %s:  %s", Exception, ex) 
            if self.cursor:
                self.cursor.close()
            if self.dbconn:
                self.dbconn.close()
            sys.exit(-1)
        return True

    def NextDocument(self,err=''):

        if self.idx < len(self.data):
            actor = self.data[self.idx]
            self.aid = self.docid = actor['Actor_ID']
            self.name = ( actor['Actor_Name'] and actor['Actor_Name'] ) or ''
            self.jp = ( actor['Actor_HeaderSoundSequence'] and actor['Actor_HeaderSoundSequence'] ) or ''
            self.py = ( actor['Actor_AllSoundSequence'] and actor['Actor_AllSoundSequence'] ) or ''
            self.ano = actor['Actor_No']
            self.idx += 1
            return True
        else:
            return False


if __name__ == '__main__':
    conf = { 'limit': 11 }
    s = mainSource(conf)
    s.Connected()
    s.OnBeforeIndex()

    while s.NextDocument():
        print 'docid=%d, name=%s, jp=%s, py=%s, ano=%s' % (s.docid, s.name, s.jp, s.py, s.ano )
    pass
