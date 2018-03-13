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
            ('mid',{'type':'integer'}),
            ('mno',{'type':'integer'}),
            ('name',{'type':'string_text'}),
            ('jp',{'type':'string_text'}),
            ('py',{'type':'string_text'}),
            ('lyric',{'type':'string_text'}),
            ('sid1',{'type':'integer'}),
            ('sid2',{'type':'integer'}),
            ('sid3',{'type':'integer'}),
            ('sid4',{'type':'integer'}),
            ('sno1',{'type':'integer'}),
            ('sno2',{'type':'integer'}),
            ('sno3',{'type':'integer'}),
            ('sno4',{'type':'integer'}),
            ('sname1',{'type':'string_text'}),
            ('sname2',{'type':'string_text'}),
            ('sname3',{'type':'string_text'}),
            ('sname4',{'type':'string_text'}),
            ('sjp1',{'type':'string_text'}),
            ('sjp2',{'type':'string_text'}),
            ('sjp3',{'type':'string_text'}),
            ('sjp4',{'type':'string_text'}),
            ('spy1',{'type':'string_text'}),
            ('spy2',{'type':'string_text'}),
            ('spy3',{'type':'string_text'}),
            ('spy4',{'type':'string_text'}),
            ('sort',{'type':'integer'}),
            ('lid',{'type':'integer'}),
            ('videotype',{'type':'integer'}),
            ('groupid',{'type':'integer'}),
            ('ltype',{'type':'integer'}),
        ]

    def GetFieldOrder(self):
        return [('name','jp','py','sname1','sjp1','spy1','sname2','sjp2','spy2','sname3','sjp3','spy3','sname4','sjp4','spy4','lyric')]

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
    def getactors(self):
        try:
            if not self.dbconn or not self.cursor:
                self.Connected()
            self.cursor.execute('select actor_id as aid,actor_name as name,actor_headersoundsequence as jp,actor_allsoundsequence as py,actor_no as ano from actors')
            data = self.cursor.fetchall()
            return {row['aid']:row for row in data}
        except Exception,ex:
            print ex
        return {}

    def getmangeractor(self):
        try:
            if not self.dbconn or not self.cursor:
                self.Connected()
            self.cursor.execute('select mediamanage_id,actor_id  from mediamanageactor')
            data = self.cursor.fetchall()
            self.cursor.execute('select mediamanage_id as mid,mediamanage_ordercount as total,mediamanage_language_id as lid from mediasmanage')
            mdata = self.cursor.fetchall()
            if mdata:
                mdata = {row['mid']:row for row in mdata}
            else:
                mdata={}
            if data:
                res={}
                for row in data:
                    mid = row['mediamanage_id']
                    if not res.has_key(mid):
                        res[mid]={'actor':[]}
                    res[mid]['actor'].append(row['actor_id'])
                    mm = mdata.get(mid)
                    res[mid]['total'] = mm['total'] if mm else 0
                    res[mid]['lid'] = mm['lid'] if mm else 0
                return res
        except Exception,ex:
            print ex
        return {}

    def OnBeforeIndex(self):
        self.manage = self.getmangeractor()
        self.actor = self.getactors()
        limit_record = (self.conf.has_key('limit') and ' LIMIT '+ str(self.conf['limit'])) or ''
        sql = 'select Media_Id,Media_Name,Media_HeaderSoundSequence,Media_AllSoundSequence,Media_Lyric,Media_SerialNo,Media_Manage_ID,media_isreserved3 as videotype,media_isreserved4 as groupid,media_isreserved5 as ltype from medias %s'%(limit_record)
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
            media = self.data[self.idx]
            self.mid = self.docid = media['Media_Id']
            self.name = ( media['Media_Name'] and media['Media_Name'] ) or ''
            self.jp = ( media['Media_HeaderSoundSequence'] and media['Media_HeaderSoundSequence'] ) or ''
            self.py = ( media['Media_AllSoundSequence'] and media['Media_AllSoundSequence'] ) or ''
            self.lyric = ( media['Media_Lyric'] and media['Media_Lyric'] ) or ''
            self.mno = int(media['Media_SerialNo'])
            self.sort = 0
            self.lid = 0
            manageid = media['Media_Manage_ID']
            actor1 = None
            actor2 = None
            actor3 = None
            actor4 = None
            if manageid:
                if self.manage.has_key(manageid):
                    self.sort = self.manage[manageid]['total']
                    self.lid= self.manage[manageid]['lid']
                    a_list = self.manage[manageid]['actor']
                    a_len = len(a_list)
                    if a_len>0:
                        actor1 = self.actor.get(a_list[0])
                    if a_len>1:
                        actor2 = self.actor.get(a_list[1])
                    if a_len>2:
                        actor3 = self.actor.get(a_list[2])
                    if a_len>3:
                        actor4 = self.actor.get(a_list[3])
            self.sid1 = actor1['aid'] if actor1 else 0
            self.sid2 = actor2['aid'] if actor2 else 0
            self.sid3 = actor3['aid'] if actor3 else 0
            self.sid4 = actor4['aid'] if actor4 else 0
            self.sno1 = actor1['ano'] if actor1 else 0
            self.sno2 = actor2['ano'] if actor2 else 0
            self.sno3 = actor3['ano'] if actor3 else 0
            self.sno4 = actor4['ano'] if actor4 else 0
            self.sname1 = actor1['name'] if actor1 else ''
            self.sname2 = actor2['name'] if actor2 else ''
            self.sname3 = actor3['name'] if actor3 else ''
            self.sname4 = actor4['name'] if actor4 else ''
            self.sjp1 = actor1['jp'] if actor1 else ''
            self.sjp2 = actor2['jp'] if actor2 else ''
            self.sjp3 = actor3['jp'] if actor3 else ''
            self.sjp4 = actor4['jp'] if actor4 else ''
            self.spy1 = actor1['py'] if actor1 else ''
            self.spy2 = actor2['py'] if actor2 else ''
            self.spy3 = actor3['py'] if actor3 else ''
            self.spy4 = actor4['py'] if actor4 else ''
            self.ltype = media['ltype']
            self.groupid = media['groupid']
            self.videotype = media['videotype']
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
        print 'docid=%d, name=%s, jp=%s, py=%s, ano=%s, sname1=%s' % (s.docid, s.name, s.jp, s.py, s.mno,s.sname1 )
    pass
