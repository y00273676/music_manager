#!/usr/bin/env python
#-*- coding:utf-8 -*-
#media and actor keyword searcd
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
            ('name',{'type':'string_text'}),
            ('jp',{'type':'string_text'}),
            ('py',{'type':'string_text'}),
            ('total',{'type':'integer'}),
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
        sql = 'select distinct name,py,jp from (select Actor_Name name,Actor_HeaderSoundSequence jp ,Actor_AllSoundSequence py from actors union all select Media_Name,Media_HeaderSoundSequence,Media_AllSoundSequence from medias)a group by name,py,jp %s'%(limit_record)
        try:
            print sql
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
            self.docid = self.idx+1
            self.name = ( actor['name'] and actor['name'] ) or ''
            self.jp = ( actor['jp'] and actor['jp'] ) or ''
            self.py = ( actor['py'] and actor['py'] ) or ''
            self.total = 0
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
        print 'docid=%d, name=%s, jp=%s, py=%s, total=%s' % (s.docid, s.name, s.jp, s.py, s.total )
    pass
