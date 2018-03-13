#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import logging
import commands
import threading
import traceback
import md5
from control.modbc import get_all_thunder_ini
from setting import MYSQL
from control.fileservers import conn as connY

import pymysql

logger = logging.getLogger(__name__)

conn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')

connMusic = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')

def getDataBaseConnection():
    conn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')
    return conn

def getDataBaseConnectionMusic():
    connMusic = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')
    return connMusic

def getKaraokConn_dict():
    conn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0], charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    return conn



def createSQLTabel(sql):
    try:
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        n = cursor.execute(sql)
        cursor.close()
    except:
        print traceback.print_exc()
        pass

def activation():
    connMessage = getDataBaseConnection()
    cursorMessage = connMessage.cursor()
    cursorMessage.execute("select version()")
    for i in cursorMessage:
        print(i)
    cursorMessage.close()
    cursorY = connY.cursor()
    cursorY.execute("select version()")
    for i in cursorY:
        print(i)
    cursorY.close()
    cursorMusic = connMusic.cursor()
    cursorMusic.execute("select version()")
    for i in cursorMusic:
        print(i)
    cursorMusic.close()
    timer = threading.Timer(7200, activation)
    timer.start()
timer = threading.Timer(7200, activation)
timer.daemon = True
timer.start()


def isvild_sql(kwargs):
    try:
        mconn = pymysql.connect(host=kwargs['DataBaseServerIp'], port=3306, user=kwargs['UserName'], password=kwargs['Password'], db='karaok',charset='UTF8')
        cur = mconn.cursor()
        cur.execute("select version()")
        for i in cur:
            print(i)
        cur.close()
        return 0
    except:
        return 1


def foo(*args,**kwargs):
    print('args=',args)
    print('kwargs=',kwargs)
    print('**********************')

def opendb():
    print('open mysql')

def closedb():
    conn.close()

def executedb():
    cur = conn.cursor()
    cur.execute("select version()")
    for i in cur:
        print(i)
    cur.close()

def addSong(**kwargs):
    print(kwargs['server'])

def sp_execute(sql):
    print("sp_execute: " + sql)
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n = cursor.execute(sql)
    conn.commit()
    cursor.close()
    return n

def sp_sql2json(sql):
    print("!!!!sql2json not implements!!!!")



def sp_createuniqueid(**kwargs):

    tabname = kwargs['table']
    objname = kwargs['columname']
    if tabname=='' or objname =='':
        return -1

    ncount = 1
    sql = "select max(" + objname + "_ID) + 1 from " + tabname
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] is not None:
            ncount = row[0]



    cursor.close()
    print("sp_createuniqueid: " + tabname + "." + objname + " " + str(ncount))
    return ncount


def sp_GetFirstAvailableID(**kwargs):

    tabname = kwargs['table']
    objname = kwargs['columname']

    id = 1
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select max(" + objname + ")+1 from " + tabname
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        if row[0] is not None:
              id = row[0]
    cursor.close()
    print("sp_GetFirstAvailableID: " + tabname + "." + objname + " " + str(id))
    return id



#serverIp NVARCHAR(50), mid, no, version, date
def sp_ImportMaterial(**kwargs):

    sql = "insert into Cloud_ServerImport(Import_No,Import_Version,Import_Versiondate,Import_Ip,Import_Mid,Import_Type) values("
    sql += "'" + kwargs['no'] + "','" + kwargs['version'] + "','" + kwargs['date'] + "','" + kwargs['serverIp'] + "','" + kwargs['mid']+"',1)"
    print(sql)
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    cursor.execute(sql)

    _have = 0
    sql = "select fileserver_ipAddress from fileservers a, servergroups b, Cloud_ServerImport c "
    sql+= "where FileServer_Group_ID = ServerGroup_ID and fileserver_ipAddress=Import_Ip and Import_Mid='" + kwargs['mid'] + "' and Import_Type=1"
    print(sql)

    cursor.execute(sql)
    rows = cursor.fetchall()
    for row  in rows:
        _have = 1
    print('_have: ' + str(_have))
    if(_have==1):
        sql = "update cloud_Material set operation=2 where mid='" + kwargs['mid'] + "'"
        print(sql)
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        cursor.execute(sql)

    cursor.close()



#in serverIp NVARCHAR(50),
#in mid int, in no NVARCHAR(256),
#in version NVARCHAR(50),
#in date NVARCHAR(50)
def sp_ImportMusic(**kwargs):
    serverIp = kwargs['serverIp']
    mid = kwargs['mid']
    version = kwargs['version']
    date = date['mid']

def sp_getaddmediamark(**kwargs):

    num = 0
    sql = "select count(*) from configures"
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n=cursor.execute(sql)
    for row in cursor.fetchall():
        num = row[0]
    if num==1:
        sql = "select Configure_Set03 from configures where Configure_ID = 1"
        n=cursor.execute(sql)
        for row in cursor.fetchall():
            num = row[0]
    cursor.close()
    return num



#############2016-07-28 新增 sp_getserialno  spm_getserialno
#media_name name = null,
#media_actor_id1 normalid = null,
#media_actor_id2 normalid = null,
#media_actor_id3 normalid = null,
#media_actor_id4 normalid = null,
#media_type_id1 normalid = null,
#media_type_id2 normalid = null,
#media_type_id3 normalid = null,
#typeid normalid = null,
#group_id normalid = null,
#fileserver_id normalid = null,
#isMenpai  int  =0                --是否是门牌广告 0，普通 1，门牌广告
def sp_getserialno(**kwargs):

    media_name = kwargs['media_name']
    media_actor_id1 = kwargs['media_actor_id1']
    media_actor_id2 = kwargs['media_actor_id2']
    media_actor_id3 = kwargs['media_actor_id3']
    media_actor_id4 = kwargs['media_actor_id4']
    media_type_id1 = kwargs['media_type_id1']
    media_type_id2 = kwargs['media_type_id2']
    media_type_id3 = kwargs['media_type_id3']
    typeid = kwargs['typeid']
    group_id = kwargs['group_id']
    fileserver_id = kwargs['fileserver_id']
    isMenpai = kwargs['isMenpai']


    if typeid=='' or int(typeid)<0 or int(typeid)>8:
        return -100
    if media_name=='':
        return -101
    conn = getDataBaseConnection()
    cursor = conn.cursor()

    maxserialno = 9000000
    sql = "select max(cast(Media_SerialNo as int))+1 from medias where cast(Media_SerialNo as int) >= 9000000"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] != None:
            maxserialno = int(row[0])
    if maxserialno>9999999:
        cursor.close()
        return -102
    cursor.close()

    return maxserialno







def sp_modifyusersonglist(**kwargs):

    media_id = kwargs['media_id']
    SitPlaySongList_Shunxu = kwargs['SitPlaySongList_Shunxu']
    SitPlaySongList_OldShunxu = kwargs['SitPlaySongList_OldShunxu']
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    _have = 0
    sql = "select 1 from MediaUserSet where MediaUserSet_MediaId='" + media_id + "' and MediaUserSet_Shunxu='" + SitPlaySongList_OldShunxu + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        _have = row[1]

    if _have == 1:
        sql = "update MediaUserSet set MediaUserSet_Shunxu='" + str(SitPlaySongList_Shunxu) + "' where "
        sql+= "MediaUserSet_MediaId='" + str(media_id) + "' and MediaUserSet_Shunxu='" + str(SitPlaySongList_OldShunxu) + "'"
        cursor.execute(sql)
    else:
        songlist_id=''
        sql = "select max(MediaUserSet_Id)+1 from MediaUserSet"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            songlist_id = row[0]
        if songlist_id==None:
            songlist_id = '1'

        sql = "insert into MediaUserSet(MediaUserSet_Id,MediaUserSet_MediaId,MediaUserSet_Shunxu) values "
        sql+= "('" + str(songlist_id) + "','" + str(media_id) + "','" + str(SitPlaySongList_Shunxu) + "')"
        print(sql)
        cursor.execute(sql)
    cursor.close()



if __name__=='__main__':
    insertest()
#     addSong(server='192.100.110.1')
#     opendb()
#     sp_AddActor(actor_name='张学友XXX',actor_no='0',actor_typename='男',actor_photo='',actor_jianpin='ZXY',actor_pinyin='ZXY')
#     sp_ImportMaterial(serverIp='192.100.110.252', mid='1', no='0', version='1', date='2016-07-28')
#     sp_addmediatype(curid='102', name='XYZ', description='HRU', typeid='1')
#
#     sp_addmedias(serialno='11111', iname='iname', lname='lname', type1 = 'type1', type2='type2',  \
#         jianpin= 'jianpin', pinyin= 'pinyin', sname1= 'sname1', sname2= 'sname2', sname3= 'sname3', \
#         sname4= 'sname4', ltype= '1', volume= '9', stroke= '5', bihua= 'bihua', \
#         videoformat= 'videoformat', audioformat= 'audioformat', videotype= '1', \
#         ztrack= '2', ytrack= '3', isnew= '1', groupid= '1', filename= '/nnt/ss/0000.mp4', \
#         lyric= 'lyric')
#     sp_deletemedia(media_id='253608')

#     n = spm_getserialno(media_name='123123', media_actor_name1 = '10cm', media_actor_name2 = '17岁女生', \
#                     media_actor_name3 = '1sagain', media_actor_name4 = '24K', \
#                     media_type_name1 = '校园民谣', media_type_name2 = '男女对唱', media_type_name3 = '', \
#                     typeid = '0', group_id = '1', fileserver_id = '', isMenpai = '0')
#     print("spm_getserialno: ", str(n))
#     sp_getsitsonginfo()
#     sp_modifyadvertisementstatus(typeid=0)
#     sp_modifyusersonglist(media_id='0', SitPlaySongList_Shunxu='0', SitPlaySongList_OldShunxu='2')
#     closedb()
#     m_a=[]
#     m_a.append({"a":1})
#     m_a.append({"b":2})
#     m_a.append({"c":3})
#     for i in range(len(m_a)):
#         if i<len(m_a)-1:
#             print i










#isMenpai 是否是门牌广告 0，普通 1，门牌广告
def spm_getserialno(**kwargs):

    media_name = kwargs['iname']
    media_actor1 = kwargs['sname1']
    media_actor2 = kwargs['sname2']
    media_actor3 = kwargs['sname3']
    media_actor4 = kwargs['sname4']

    media_type_name1 = kwargs['type1']
    media_type_name2 = kwargs['type2']
    media_type_name3 = kwargs['type3']

    typeid =  kwargs['typeid']
    group_id =  kwargs['group_id']
    fileserver_id =  kwargs['fileserver_id']
    isMenpai =  kwargs['isMenpai']

    if typeid=='' or int(typeid)<0 or int(typeid)>8:
        return 1
    if group_id=='':
        return -1
    if media_name=='':
        return -2

    conn = getDataBaseConnection()
    cursor = conn.cursor()

    _have = 0
    sql = "select 1 from servergroups where ServerGroup_ID = '" + group_id +"' and ServerGroup_IsValid = 1"
    cursor.execute(sql)
    for row in cursor.fetchall():
        _have = 1
    if _have==0:
        cursor.close()
        return -3

    sql = "select 1 from fileservers where FileServer_ID = '" + fileserver_id + "' and FileServer_IsValid = 1"
    _have = 0
    cursor.execute(sql)
    for row in cursor.fetchall():
        _have = 1
    if _have==0:
        fileserver_id = ''

    media_actor_id1 = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor1 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id1 = row[0]

    media_actor_id2 = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor2 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id2 = row[0]

    media_actor_id3 = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor3 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id3 = row[0]

    media_actor_id4 = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor4 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id4 = row[0]



    if (media_actor_id1 == media_actor_id2 and media_actor_id1 != '' and media_actor_id2 != '') or (media_actor_id1 == media_actor_id3 and media_actor_id1 != '' and media_actor_id3 != '') or (media_actor_id1 == media_actor_id4 and media_actor_id1 != '' and media_actor_id4 != '') or \
            (media_actor_id2 == media_actor_id3 and media_actor_id2 != '' and media_actor_id3 != '') or (media_actor_id2 == media_actor_id4 and media_actor_id2 != '' and media_actor_id4 != '') or (media_actor_id3 == media_actor_id4 and media_actor_id3 != '' and media_actor_id4 != ''):
        cursor.close()
        return -4

    media_type_id1 = ''
    sql = "select MediaType_ID from mediatypes where MediaType_Name ='" + media_type_name1 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_type_id1 = row[0]

    media_type_id2 = ''
    sql = "select MediaType_ID from mediatypes where MediaType_Name ='" + media_type_name2 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_type_id2 = row[0]

    media_type_id3 = ''
    sql = "select MediaType_ID from mediatypes where MediaType_Name ='" + media_type_name3 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_type_id3 = row[0]
    if (media_type_id1 == media_type_id2 and media_type_id1 != '' and media_type_id2 != '') or (media_type_id1 == media_type_id3 and media_type_id1 != '' and media_type_id3 != '') or (media_type_id2 == media_type_id3 and media_type_id2 != '' and media_type_id3 != ''):
        return -5

    n = sp_getserialno(media_name=media_name, \
             media_actor_id1=media_actor_id1, \
             media_actor_id2=media_actor_id2, \
             media_actor_id3=media_actor_id3, \
             media_actor_id4=media_actor_id4, \
             media_type_id1=media_type_id1, \
             media_type_id2=media_type_id2, \
             media_type_id3=media_type_id3, \
             typeid=typeid, group_id=group_id, \
             fileserver_id=fileserver_id, \
             isMenpai=isMenpai)

    cursor.close()
    return n











#in actor_no int, in actor_name nvarchar(256), in actor_typename nvarchar(8),
#in actor_photo nvarchar(256), in actor_jianpin nvarchar(256),
#in actor_pinyin nvarchar(256), out actor_id int
def sp_AddActor(**kwargs):
    global conn
    if kwargs['actor_name']=='':
        return 0

    actorNo = kwargs['actorNo']
    actorSequence = kwargs['actorSequence']

    typeid = 0
    sql = ''

    cursor = conn.cursor()
    try:
        cursor.execute("select ActorType_ID from actortypes where ActorType_Name='"+ filterText(kwargs['actor_typename']) + "'")
        rows = cursor.fetchall()
        for row in rows:
            typeid = row[0]
    except:
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        cursor.execute("select ActorType_ID from actortypes where ActorType_Name='"+ filterText(kwargs['actor_typename']) + "'")
        rows = cursor.fetchall()
        for row in rows:
            typeid = row[0]

    print typeid
    sequence = actorSequence()
#     cursor.execute("select IFNULL(max(Actor_Sequence),0)+1 from actors where Actor_Sequence<>''")
#     rows = cursor.fetchall()
#     for row in rows:
#         sequence = row[0]

    soundsequence=kwargs['actor_jianpin'][0]
#     cursor.execute("select (case when length('" + kwargs['actor_jianpin']+ "') <= 0 then '' else substring('" + kwargs['actor_jianpin']+"',1, 1) end)")
#     for row in cursor.fetchall():
#         soundsequence = row[0]

    if kwargs.has_key("markName"):
        if kwargs['markName']!=kwargs['actor_name']:
            r_id = 0
            cursor.execute("select Actor_ID, Actor_PictureFilePath from actors where Actor_Name='" + filterText(kwargs['actor_name']) + "'")
            rows = cursor.fetchall()
            for row in rows:
                r_id = row[0]
            if r_id==0 or r_id is None:
                sql = "update actors set Actor_Name='"+filterText(kwargs['actor_name'])+"', Actor_IsSongerStar = 1, Actor_Type_ID='" + str(typeid) + "',"
                sql += "Actor_Description='" + filterText(kwargs['actor_name']) + "', Actor_SoundSequence = '" + soundsequence + "',"
                sql += "Actor_HeaderSoundSequence='" + filterText(kwargs['actor_jianpin']) + "', Actor_AllSoundSequence='" + filterText(kwargs['actor_pinyin']) + "',"
                sql += "Actor_No='" + kwargs['actor_no'] + "' where Actor_Name='" + filterText(kwargs['markName']) + "'"
                cursor.execute(sql)
                cursor.close()
                return r_id
            else:
                return None;

    r_id = 0
    cursor.execute("select Actor_ID, Actor_PictureFilePath from actors where Actor_Name='" + filterText(kwargs['actor_name']) + "'")
    rows = cursor.fetchall()
    for row in rows:
        r_id = row[0]

    sql = ''
    if r_id==0 or r_id is None:
#         id = sp_GetFirstAvailableID(table='actors', columname='Actor_ID')
        id = actorNo()
        r_id = id
        sql = "insert into actors(Actor_ID, Actor_Name, Actor_Type_ID, Actor_Description, Actor_IsSongerStar, Actor_Sequence, Actor_SoundSequence, Actor_PictureFilePath, "
        sql += "Actor_HeaderSoundSequence,Actor_AllSoundSequence,Actor_No) values "
        sql += "('" + str(r_id) + "','" + kwargs['actor_name'] + "','" + str(typeid) + "','" + kwargs['actor_name'] + "',1,'" + str(sequence) + "','" + soundsequence + "',"
        sql += "'" + kwargs['actor_photo'] + "','" + kwargs['actor_jianpin'] + "','" + kwargs['actor_pinyin'] + "','" + kwargs['actor_no'] + "')"
    else:
        sql = "update actors set Actor_IsSongerStar = 1, Actor_Type_ID='" + str(typeid) + "',"
        sql += "Actor_Description='" + kwargs['actor_name'] + "', Actor_SoundSequence = '" + soundsequence + "',"
        sql += "Actor_HeaderSoundSequence='" + kwargs['actor_jianpin'] + "', Actor_AllSoundSequence='" + kwargs['actor_pinyin'] + "',"
        sql += "Actor_No='" + kwargs['actor_no'] + "' where Actor_Name='" + kwargs['actor_name'] + "'"
    #print(sql)
    cursor.execute(sql)
    cursor.close()
    return r_id


#in curid int
#in iname varchar(80)
#in description varchar(2048)
#in typeid int
#out result int
def sp_addmediatype(**kwargs):

    curid = kwargs['curid']
    iname = kwargs['name']
    description = kwargs['description']
    typeid = kwargs['typeid']
    iname = filterText(iname)
    mediatypesNo = kwargs['mediatypesNo']


    sql = ''
    flag = 0
    if curid=='':
        return 1
    if int(typeid)<0 or int(typeid)>6:
        return 1
    if description=='':
        description = iname
    cursorMusic = connMusic.cursor()
    if int(curid)>101 or int(curid) <= 0:
        flag = 0
        sql = "select MediaType_ID from mediatypes where MediaType_ID = '" +  str(curid) + "'"
        cursorMusic.execute(sql)
        rows = cursorMusic.fetchall()
        for row  in rows:
            flag = 1
        if flag==0:
#             curid = sp_createuniqueid(table='mediatypes', columname='MediaType')
            curid = mediatypesNo()
        if curid<101:
            curid = 101

    sql = ''
    if typeid=='0':
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 and MediaType_IsKaraok = 0 and MediaType_IsAds = 0)"
    elif typeid=='1':
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 0 and MediaType_IsKaraok = 1 and MediaType_IsAds = 0)"
    elif typeid=='2':
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 0 and MediaType_IsKaraok = 0 and MediaType_IsAds = 1)"
    elif typeid=='3':
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 and MediaType_IsKaraok = 1 and MediaType_IsAds = 0)"
    elif typeid=='4':
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 and MediaType_IsKaraok = 0 and MediaType_IsAds = 1)"
    elif typeid=='5':
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 0 and MediaType_IsKaraok = 1 and MediaType_IsAds = 1)"
    else:
        sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 and MediaType_IsKaraok = 1 and MediaType_IsAds = 1)"
    flag = 0
    cursorMusic.execute(sql)
    rows = cursorMusic.fetchall()
    for row in rows:
        flag = 1

    if flag==1:
        cursorMusic.close()
        return 2
    flag = 0
    sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "'"
    cursorMusic.execute(sql)
    rows = cursorMusic.fetchall()
    for row in rows:
        flag = 1

    if flag==1:
        if typeid == '0':
            sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsKaraok = 0, MediaType_IsAds = 0, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
        elif typeid == '1':
            sql = "update mediatypes set MediaType_IsMovie = 0, MediaType_IsKaraok = 1, MediaType_IsAds = 0, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
        elif typeid == '2':
            sql = "update mediatypes set MediaType_IsMovie = 0, MediaType_IsKaraok = 0, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
        elif typeid == '3':
            sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsKaraok = 1, MediaType_IsAds = 0, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
        elif typeid == '4':
            sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsKaraok = 0, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
        elif typeid == '5':
            sql = "update mediatypes set MediaType_IsMovie = 0, MediaType_IsKaraok = 1, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
        else:
            sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsKaraok = 1, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
    else:
        if typeid == '0':
            sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql += "('" + str(curid) + "','" + iname + "','" + description + "',1,0,0)"
        elif typeid == '1':
            sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql+="('" + str(curid) + "','" + iname + "','" + description + "',0,1,0)"
        elif typeid == '2':
            sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql+="('" + str(curid) + "','" + iname + "','" + description + "',0,0,1)"
        elif typeid == '3':
            sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql+="('" + str(curid) + "','" + iname + "','" + description + "',1,1,0)"
        elif typeid == '4':
            sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql +="('" + str(curid) + "','" + iname + "','" + description + "',1,0,1)"
        elif typeid == '5':
            sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql +="(" + str(curid) + "','" + iname + "','" + description + "',0,1,1)"
        else:
            sql  = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
            sql +="('" + str(curid) + "','" + iname + "','" + description + "',1,1,1)"

    print sql

    cursorMusic.execute(sql)

    sql = "update systemsettinginfo set SettingInfo_Value = date_add(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    cursorMusic.execute(sql)
    cursorMusic.close()
    return curid





    #serialno int,           --编号
#name nvarchar(256),     --歌曲名称
#lname nvarchar(16),     --语言
#type1 nvarchar(16),     --类型
#type2 nvarchar(16),     --类型
#jianpin nvarchar(256),  --简拼
#pinyin nvarchar(256),   --全拼
#sname1 nvarchar(256),   --歌星名称
#sname2 nvarchar(256),   --歌星名称
#sname3 nvarchar(256),     --歌星名称
#sname4 nvarchar(256),   --歌星名称
#ltype int,              --语言类型 0 国语 1 日语  2韩语
#volume int,             --音量
#stroke int,             --歌曲首字母的笔画数（第一笔）
#bihua nvarchar(64),     --歌曲名称的笔划数
#videoformat nvarchar(8),--视频类型
#audioformat nvarchar(8),--音频类型
#videotype int,          -- 0 流水影 1 MV  2  演唱会
#ztrack int,             --左声道
#ytrack int,             --右声道
#isnew int,              --是否新歌
#groupid int,            --歌曲组ID
#filename nvarchar(256), --文件保存目录
#lyric nvarchar(2048)    --歌词
# cloud_sp_addmedias
def sp_addmedias(**kwargs):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    serialno = ""
    if "serialno" in kwargs:
        serialno =  kwargs['serialno']
    iname = ""
    if "iname" in kwargs:
        iname = kwargs['iname']
    lname = ""
    if "lname" in kwargs:
        lname = kwargs['lname']
    mctypes = []
    type1 = ""
    if "type1" in kwargs:
        type1 = kwargs['type1']
        mctypes.append(type1)
    type2 = ""
    if "type2" in kwargs:
        type2 = kwargs['type2']
        mctypes.append(type2)
    jianpin = ""
    if "jianpin" in kwargs:
        jianpin= kwargs['jianpin']
    pinyin = ""
    if "pinyin" in kwargs:
        pinyin= kwargs['pinyin']
    sname1 = ""
    if "sname1" in kwargs:
        sname1= kwargs['sname1']
    sname2 = ""
    if "sname2" in kwargs:
        sname2= kwargs['sname2']
    sname3 = ""
    if "sname3" in kwargs:
        sname3= kwargs['sname3']
    sname4 = ""
    if "sname4" in kwargs:
        sname4= kwargs['sname4']
    ltype = ""
    if "ltype" in kwargs:
        ltype= kwargs['ltype']
    volume = ""
    if "volume" in kwargs:
        volume= kwargs['volume']
    stroke = ""
    if "stroke" in kwargs:
        stroke= kwargs['stroke']
    bihua = ""
    if "bihua" in kwargs:
        bihua= kwargs['bihua']
    videoformat = ""
    if "videoformat" in kwargs:
        videoformat= kwargs['videoformat']
    audioformat = ""
    if "audioformat" in kwargs:
        audioformat= kwargs['audioformat']
    videotype = ""
    if "videotype" in kwargs:
        videotype= kwargs['videotype']
    ztrack = ""
    if "ztrack" in kwargs:
        ztrack= kwargs['ztrack']
    ytrack = ""
    if "ytrack" in kwargs:
        ytrack= kwargs['ytrack']
    ordercount = '0'
    if "ordercount" in kwargs:
        ordercount = kwargs['ordercount']
    isnew = 0
    if "isnew" in kwargs:
        isnew = 1 if kwargs['isnew'] else 0
    groupid = 1
    if "groupid" in kwargs:
        groupid= kwargs['groupid']
    filename = ""
    if "filename" in kwargs:
        filename= kwargs['filename']
    lyric = ""
    if "lyric" in kwargs:
        lyric= kwargs['lyric']
    lights = 0
    if "lights" in kwargs:
        lights = kwargs['lights']

    iname=filterText(iname)
    lname=filterText(lname)
    type1=filterText(type1)
    type2=filterText(type2)
    jianpin=filterText(jianpin)
    pinyin=filterText(pinyin)
    sname1=filterText(sname1)
    sname2=filterText(sname2)
    sname3=filterText(sname3)
    sname4=filterText(sname4)
    ltype=filterText(ltype)
    lyric=filterText(lyric)

    IsMovie= 0
    IsKaraok= 1
    IsAds= 0

    if kwargs.has_key("IsMovie"):
        IsMovie= kwargs['IsMovie']
    if kwargs.has_key("IsKaraok"):
        IsKaraok= kwargs['IsKaraok']
    if kwargs.has_key("IsAds"):
        IsAds= kwargs['IsAds']

    mediasNo = kwargs['mediasNo']
    managerNo = kwargs['managerNo']
    mediadetailNo = kwargs['mediadetailNo']
    mediafilesNo = kwargs['mediafilesNo']

    if videoformat=='':
        videoformat = 'MPEG1'

    if audioformat=='':
        audioformat = 'MPEG'

    if groupid=='':
        groupid = '1'

    marker = kwargs['marker']

    if marker<0 or marker>1:
        marker = 0

    sequence = 0
    soundsequence = ''

    sequence = getSequence()

    #获取歌曲首字母
    if jianpin != '':
        soundsequence = jianpin[0]
#     sql = "select case when length('" + jianpin + "') <= 0 then null else substring('" + jianpin  + "', 1, 1) end"
#     n = cursor.execute(sql)
#     for row in cursor.fetchall():
#          soundsequence = row[0]
    #获取视频格式ID
    media_carrier_id = ''
    sql = "select Carrier_ID from carriers where Carrier_Name='" + str(videoformat) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        media_carrier_id = row[0]
    if media_carrier_id=='':
        carriersMaxId=0
        sql = "select max(Carrier_ID)+1 from carriers"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            maxId=row[0]
            if maxId:
                carriersMaxId=maxId

        sql = "insert into carriers(Carrier_ID,Carrier_Name,Carrier_Description) values('"+ str(carriersMaxId) +"','"+str(videoformat)+"','"+str(videoformat)+"')"
        n = cursor.execute(sql)
        media_carrier_id = conn.insert_id()


    #获取音频格式ID
    media_audio_id = ''
    sql = "select Audio_ID into @media_audio_id from audios where Audio_Name = '" + str(audioformat) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
         media_audio_id = row[0]

    if media_audio_id=='':
        sql = "select Audio_ID from audios where Audio_Name = 'MPEG'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            media_audio_id = row[0]

    media_language_id = ltype
    sql = "select Language_ID from languages where Language_Name='" + str(lname) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] is not None:
            media_language_id = row[0]
    media_id = '0'
    manageid = '1'
    sql = "select Media_id, Media_Manage_ID from medias where Media_SerialNo='" + str(serialno) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        media_id = row[0]
        manageid = row[1]

    if media_id=='0':
#         mediamanage_id = sp_createuniqueid(table='mediasmanage', columname='MediaManage')
#         media_id = sp_createuniqueid(table='medias', columname='Media')
        mediamanage_id = managerNo()
        media_id = mediasNo()

        if media_id>mediamanage_id:
            mediamanage_id = media_id
        else:
            media_id = mediamanage_id
        #添加mediasmanage表
        sql = "insert into mediasmanage(MediaManage_ID,  MediaManage_Language_ID, MediaManage_Carrier_ID, MediaManage_Audio_ID, "
        sql+= "MediaManage_Format_ID, MediaManage_RegisterTime,MediaManage_IsNew, MediaManage_OriginalTrack, MediaManage_AccompanyTrack, MediaManage_OrderCount) "
        sql+= "values('" + str(mediamanage_id) +"','" +str(media_language_id) +"','" + str(media_carrier_id) + "',"
        sql +="'" + str(media_audio_id) + "','" + str(media_carrier_id) + "', now()," + str(isnew) + ",'" + str(ztrack) +  "','" + str(ytrack) + "'," + ordercount + ")"

#         sp_execute(sql)
        n = cursor.execute(sql)

        Media_Status = 0
        if type1!="":
            Media_Status = 1

        manageid = mediamanage_id
        sql = "insert into medias (Media_ID,Media_Name,Media_serialno,Media_Length,Media_Description,Media_Manage_ID,Media_Price,Media_Name_Length,"
        sql+= "Media_Sequence,Media_SoundSequence,Media_HeaderSoundSequence,Media_IsMovie,Media_IsKaraok,Media_IsAds,Media_CreatedbyCustomer,"
        sql+= "Media_IsReserved2,Media_IsReserved3,Media_IsReserved4,Media_IsReserved5,Media_HeadStroke,Media_StrokeNum,Media_Lyric,Media_AllSoundSequence, Media_Status, media_light) "
        sql+= "values('" + str(media_id) + "','" + str(iname) + "','" + str(serialno) + "','0','','" + str(manageid) + "','0','"+str(str_len(str(iname).replace(' ', '')))+"',"
        sql+= "'" + str(sequence) + "','" + str(soundsequence) + "','" + str(jianpin) + "','"+str(IsMovie)+"','"+str(IsKaraok)+"','"+str(IsAds)+"','" + str(marker) + "','" + str(volume) + "','" + str(videotype) + "',"
        sql+= "'" + str(groupid) + "','" + str(ltype) + "','" + str(bihua) + "','"  + str(stroke) + "','" + str(lyric) + "','" + str(pinyin) + "','"+str(Media_Status)+"'," + str(lights) + ")"
        n = cursor.execute(sql)
        conn.commit()
#         sp_execute(sql)

#         mediadetail_id = sp_createuniqueid( table='mediadetails', columname='MediaDetail')
        mediadetail_id = mediadetailNo()
        sql = "insert into mediadetails(Media_ID, Media_Name, Media_SerialNo, Nation_Name, Language_Name, "
        sql+= "Actor_Name1, Actor_Name2, Actor_Name3, Actor_Name4, Director_Name1, Director_Name2, MediaType_Name1, MediaType_Name2,"
        sql+= "Carrier_Name, MediaManage_OriginalTrack, MediaManage_AccompanyTrack, MediaManage_OrderCount, MediaDetail_ID, "
        sql+= "Media_CreatedbyCustomer, Media_ExportMark, Media_Name_Length, Audio_Name, FileServer_ID, ServerGroup_ID) "
        sql+= "values('" + str(media_id) + "','" + str(iname) + "','" + str(serialno) + "','','" + str(lname) + "','"  + str(sname1) + "','" + str(sname2) + "',"
        sql+= "'" + str(sname3) + "','" + str(sname4) + "','','','" + str(type1) + "','" + str(type2) + "','" + str(videoformat) + "','" + str(ztrack) + "','" + str(ytrack) + "',"
        sql+= "'0','" + str(mediadetail_id) + "','" + str(marker) + "','0', '"+str(str_len(str(iname).replace(' ', '')))+"','" + str(audioformat) + "','" + str(groupid) + "','" + str(groupid) +"')"
        n = cursor.execute(sql)
#         sp_execute(sql)

        #添加歌曲到mediafiles
        sql = "delete from mediafiles where MediaFile_MediaManage_ID=" + str(manageid)
        n = cursor.execute(sql)
    #     n = sp_execute(sql)

        MediaFile_IsValid=0
        if type1 != "":
            MediaFile_IsValid=1

        #错误定义，标记循环结束
        sql = "select FileServer_ID, ServerGroup_ID from servergroups1 where FileServer_IsValid = 1 and ServerGroup_ID='" + str(groupid) +"'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
    #         mediafile_id = sp_createuniqueid( table = 'mediafiles', columname='MediaFile')
            mediafile_id = mediafilesNo()
            sql = "insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo, "
            sql+= "MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid) "
            sql+= "values('" + str(mediafile_id) + "','" + str(manageid) + "', "
            sql+= "concat('" + str(serialno) + "','00'),'" + str(row[0]) + "','" + str(filename) + "','1','"+str(MediaFile_IsValid)+"')"
            n = cursor.execute(sql)
    #          sp_execute(sql)
    else:
        sql = "update medias set Media_Name='" + str(iname) + "',Media_Name_Length='"+str(str_len(str(iname).replace(' ', '')))+"',Media_SoundSequence=@soundsequence,"
        sql+= "Media_HeaderSoundSequence='" + str(jianpin) + "',Media_IsReserved2='" + str(volume) + "',"
        sql+= "Media_IsReserved3='" + str(videotype) + "',Media_IsReserved4='" + str(groupid) + "',Media_IsReserved5='" + str(ltype) + "',"
        sql+= "Media_HeadStroke='" + str(bihua) + "',Media_StrokeNum='" + str(stroke) + "',Media_Lyric='" + str(lyric) + "',Media_AllSoundSequence='" + str(pinyin) + "',Media_Status=1,Media_IsMovie='"+ str(IsMovie) +"' ,Media_IsKaraok='"+ str(IsKaraok) +"' ,Media_IsAds='"+ str(IsAds) +"', media_light="+ str(lights) +" "
        sql+= "where Media_ID=" + str(media_id)
        logger.error(sql)
        n = cursor.execute(sql)
        logger.error('add 01************in sp_addmedia()************* %s' % n)

        sql = "update mediadetails set Media_Name='" + str(iname) + "',Language_Name='" + str(lname) + "',Actor_Name1='" + str(sname1) + "',"
        sql+= "Actor_Name2='" + str(sname2) + "',Actor_Name3='" + str(sname3) + "',Actor_Name4='" + str(sname4) + "',MediaType_Name1='" + str(type1) + "',"
        sql+= "MediaType_Name2='" + str(type2) + "',Carrier_Name='" + str(videoformat) + "',MediaManage_OriginalTrack='" + str(ztrack) + "',"
        sql+= "MediaManage_AccompanyTrack='" + str(ytrack) + "',Media_Name_Length='"+str(str_len(str(iname).replace(' ', '')))+"',Audio_Name='" + str(audioformat) + "',ServerGroup_ID='" + str(groupid) + "' "
        sql+= "where Media_ID=" + str(media_id)
        logger.error(sql)
        n = cursor.execute(sql)
        logger.error('add 02************in sp_addmedia()************* %s' % n)

        sql = "update mediasmanage set MediaManage_AccompanyTrack='" + str(ytrack) + "',MediaManage_OriginalTrack='" + str(ztrack) + "',"
        sql+= "MediaManage_Audio_ID='" + str(media_audio_id) + "',MediaManage_Carrier_ID='" + str(media_carrier_id) + "',"
        sql+= "MediaManage_Language_ID='" + str(media_language_id) + "',MediaManage_IsNew='" + str(isnew) + "',MediaManage_OrderCount=" + ordercount + " "
        sql+= "where MediaManage_ID=" + str(manageid)
        logger.error(sql)
        n = cursor.execute(sql)
        logger.error('add 03************in sp_addmedia()************* %s' % n)

    #添加歌曲对应歌星ID表
    sql = "delete from mediamanageactor where MediaManage_ID=" + str(manageid)
    n = cursor.execute(sql)
#     n = sp_execute(sql)

    sql = "insert into mediamanageactor(MediaManage_ID, Actor_ID) "
    sql+= "select " + str(manageid) + ", Actor_ID from actors where Actor_Name in ('" + str(sname1) + "','"+ str(sname2) +"','" + str(sname3) + "','" + str(sname4) + "')"
    n = cursor.execute(sql)
#     n = sp_execute(sql)

    #添加歌曲分类
    sql = "delete from mediamanagetype where MediaManage_ID=" + str(manageid)
    n = cursor.execute(sql)
#     n = sp_execute(sql)

    sql = "insert into mediamanagetype(MediaManage_ID, MediaType_ID)"
    sql+= "select  " + str(manageid) + ", MediaType_ID from mediatypes where MediaType_Name in('" + str(type1) + "','" + str(type2) + "')"
    n = cursor.execute(sql)
#     n = sp_execute(sql)


    if isnew=="1":
        ncount = 0
        sql = "select count(*) from medianewsong where Media_ID=" + str(media_id)
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            ncount = row[0]
        if ncount<1:
            sql = "INSERT INTO medianewsong(Media_ID,Media_InTime,Media_ValidUntil) values('" + str(media_id) + "', now(), DATE_ADD(now(), INTERVAL 1 YEAR))"
            n = cursor.execute(sql)
            conn.commit()
    sql = "delete from Cloud_MusicRecord where R_No='" + str(serialno) + "'"
    n = cursor.execute(sql)
#     n = sp_execute(sql)
    if kwargs.has_key('isNullData'):
        pass
    else:
        sql = "select count(meidasindex.MeidasIndex_Media_ID) from meidasindex WHERE MeidasIndex_Media_ID="+str(media_id)
        n = cursor.execute(sql)
        cnt=0
        for row in cursor.fetchall():
            cnt = row[0]
        if cnt==0 or cnt is None:
            sql = "INSERT INTO meidasindex(MeidasIndex_ID,MeidasIndex_Media_ID) select ifnull(MAX(MeidasIndex_ID),0)+1,"+ str(media_id) +" from meidasindex;"
            n = cursor.execute(sql)
    conn.commit()

    #update table ktvmodule_classdata
    if serialno and int(serialno) >= 9000000 and IsKaraok == 1:
        sql = 'delete from ktvmodule_classdata where serialno = "%s"' % serialno
        n = cursor.execute(sql)
        if len(mctypes) > 0:
            sql = "insert into ktvmodule_classdata(dataid, serialno, sort) "\
                    "select MediaType_NewTypeID, '%s', 9999 from mediatypes "\
                    "where MediaType_Name in %s" % (serialno, "('%s')" % "','".join(mctypes))
            print sql
            n = cursor.execute(sql)
        conn.commit()

    cursor.close()

def str_len(str):
    return len(str.decode("UTF-8"))


#media_id normalid = null,
#media_name name = null
def sp_deletemedia(**kwargs):

    media_id = kwargs['media_id']
#     media_name = kwargs['media_name']

#     sql = "select md.media_name, md.media_serialno, Actor_Name1, Actor_Name2, Actor_Name3, Actor_Name4, language_name,"
#     sql+= "Media_IsReserved2, Mediatype_name1, Mediatype_name2, Mediatype_name3, Carrier_Name,MediaManage_OriginalTrack,"
#     sql+= "MediaManage_AccompanyTrack,Media_IsReserved3,Audio_name,Media_HeaderSoundSequence,Media_IsReserved4,Media_StrokeNum,"
#     sql+= "Media_HeadStroke,Media_IsReserved5,Media_unitedCode,Media_IsAds,Media_IsMovie,Media_IsKaraok from mediadetails md,medias m "
#     sql+= "where md.media_id=m.media_id and m.media_id='" + str(media_id) +" ' and md.media_id=m.media_id"
    conn = getDataBaseConnection()
    cursor = conn.cursor()

    media_manage_id = '0'
    media_serialno='0'
    sql = "select  Media_Manage_ID,Media_SerialNo from medias where Media_ID ='" + str(media_id) + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_manage_id = row[0]
        media_serialno = row[1]

    sql = "select distinct MediaFile_Name from mediafiles where MediaFile_SerialNo='"+str(media_serialno)+"00'"
    filePath=""
    cursor.execute(sql)
    for row in cursor.fetchall():
        filePath = row[0]

    sql = "delete from mediamanageactor where MediaManage_ID = '" + str(media_manage_id) + "'"
    sp_execute(sql)

    sql = "delete from mediamanagedirector where MediaManage_ID = '" + str(media_manage_id) + "'"
    sp_execute(sql)

    sql = "delete from mediamanagetype where MediaManage_ID = '" + str(media_manage_id) + "'"
    sp_execute(sql)

    sql = "delete from mediafiles where MediaFile_MediaManage_ID = '" + str(media_manage_id) + "'"
    sp_execute(sql)

    sql = "delete from mediasmenu where MediaMenu_Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "delete from medias where Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "delete from mediasmanage where MediaManage_ID = '" + str(media_manage_id) + "'"
    sp_execute(sql)

    sql = "delete from mediadetails where Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "delete from meidasindex where MeidasIndex_Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "delete from medianewsong where Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "delete from mediasorder where MediaOrder_Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "update systemsettinginfo set SettingInfo_Value = Date_Add(now(), Interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    sp_execute(sql)

#     updateDeleteForStorNo('medias','Media_ID',media_id)
#     updateDeleteForStorNo('mediadetails','Media_ID',media_id)
#     updateDeleteForStorNo('mediadetails','MediaDetail_ID',media_id)
#     updateDeleteForStorNo('mediasmanage','MediaManage_ID',media_id)
#     updateDeleteForStorNo('mediafiles','MediaFile_MediaManage_ID',media_id)
#     updateDeleteForStorNo('mediamanageactor','MediaManage_ID',media_id)
#     updateDeleteForStorNo('mediamanagedirector','MediaManage_ID',media_id)
#     updateDeleteForStorNo('mediamanagetype','MediaManage_ID',media_id)
#     updateDeleteForStorNo('mediasmenu','MediaMenu_Media_ID',media_id)
#     updateDeleteForStorNo('medianewsong','Media_ID',media_id)
#     updateDeleteForStorNo('mediasorder','MediaOrder_Media_ID',media_id)
    try:
        sql = 'INSERT INTO deleteMedia VALUES ('+ str(media_id) +',\''+ str(media_serialno) +'\')'
        sp_execute(sql)
    except:
        pass
    print '*'*1000
    print filePath
    if os.path.exists(filePath):
        os.remove(filePath)
    conn.commit()
    cursor.close()


#显示所有过场
def sp_getsitsonginfo(**kwargs):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select media_name,media_serialno,actor_name1,mus.* from MediaUserSet mus,mediadetails m where mus.MediaUserSet_MediaId=m.Media_id  order by MediaUserSet_Shunxu"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        print(row)
    cursor.close()

#0 播放广告，1 播放电影 2 播放歌曲排行榜。 下拉选项
def  sp_modifyadvertisementstatus(**kwargs):

    typeid = kwargs['typeid']
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    if typeid<0 or typeid>2:
        _have = 0
        sql = "select 1 from Configures"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            _have = row[0]
        if _have!=1:
            return -1
    sql = "select max(Configure_ID) from Configures"
    maxid = 0
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        maxid = row[0]
    if maxid>1:
        return -2
    sql = "update Configures set Configure_Set01 = '" + str(typeid) + "' where Configure_ID = 1"
    n = cursor.execute(sql)

    changetime = ''
    sql = "select SettingInfo_Value  from SystemsettingInfo where SettingInfo_Name = 'MeidasIndexCreateTime'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        changetime = row[0]
    if changetime!='':
        sql = "update SystemsettingInfo set SettingInfo_Value = DATE_ADD(now(),INTERVAL -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime'"
        n = cursor.execute(sql)

    cursor.close()

def sp_selectmediassequence(**media):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    id = media['Language_ID']
    page = media['page']
    psize = media['psize']
    start = (int(page) - 1) * int(psize)
    sql = 'select * from mediassequence'+str(id)+' ORDER BY MediaManage_OrderCount desc LIMIT '+str(start)+','+ str(psize)
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        obj = {}
        obj['Media_ID'] = row[0]
        obj['Media_SerialNo'] = row[1]
        obj['Media_Name'] = row[2]
        obj['Media_Description'] = row[3]
        obj['Media_Name_Length'] = row[4]
        obj['Media_Sequence'] = row[5]
        obj['Media_SoundSequence'] = row[6]
        obj['MediaManage_OrderCount'] = row[7]
        obj['MediaManage_OriginalTrack'] = row[8]
        obj['Actor_Name1'] = row[10]
        obj['Actor_Name2'] = row[11]
        obj['Actor_Name3'] = row[12]
        obj['Actor_Name4'] = row[13]
        obj['Media_IsReserved4'] = row[14]
        obj['Media_IsReserved3'] = row[15]
        obj['Media_IsReserved5'] = row[16]
        obj['Media_IsReserved6'] = row[17]
        ret.append(obj)
    cursor.close()
    return ret

def sp_selectMediaDetailsForType(**media):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    type = media['type']
    page = media['page']
    psize = media['psize']
    start = (int(page) - 1) * int(psize)
    sql = 'select Media_ID,Media_SerialNo,Media_Name,Language_Name,Actor_Name1,Actor_Name2,Actor_Name3,Actor_Name4,MediaType_Name1,MediaType_Name2,MediaType_Name3,MediaManage_OrderCount from mediadetails where MediaType_Name1=\''+type+'\' or MediaType_Name2=\''+type+'\' or MediaType_Name3=\''+type+'\' ORDER BY MediaManage_OrderCount DESC LIMIT '+str(start)+','+ str(psize)
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        obj = {}
        obj['Media_ID']=row[0]
        obj['Media_SerialNo']=row[1]
        obj['Media_Name']=row[2]
        obj['Language_Name']=row[3]
        obj['Actor_Name1']=row[4]
        obj['Actor_Name2']=row[5]
        obj['Actor_Name3']=row[6]
        obj['Actor_Name4']=row[7]
        obj['MediaType_Name1']=row[8]
        obj['MediaType_Name2']=row[9]
        obj['MediaType_Name3']=row[10]
        obj['MediaManage_OrderCount']=row[11]
        ret.append(obj)
    cursor.close()
    return ret

def sp_updateMediaDetailsCount(id,count):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "update mediadetails set MediaManage_OrderCount="+str(count)+" where Media_ID='"+str(id)+"'"
    cursor.execute(sql)
    cursor.close()

def sp_selectmediassequencecount(**media):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    id = media['Language_ID']
    sql = 'select count(Media_ID) from mediassequence'+str(id)
    n = cursor.execute(sql)
    ret = 0
    for row in cursor.fetchall():
        ret = row[0]
    cursor.close()
    return ret

def sp_selectMediaTypeFromMediaDetailsCount(type):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select count(Media_ID) from mediadetails where MediaType_Name1=\''+type+'\' or MediaType_Name2=\''+type+'\' or MediaType_Name3=\''+type+'\''
    n = cursor.execute(sql)
    ret = 0
    for row in cursor.fetchall():
        ret = row[0]
    cursor.close()
    return ret

def sp_getexportdata(**media):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    no = media['Media_SerialNo']
    sql = 'select distinct medias.Media_SerialNo,medias.Media_Name, \
    mediadetails.Language_Name, \
    mediasmanage.MediaManage_ID, \
    mediadetails.Carrier_Name, \
    mediadetails.MediaManage_OriginalTrack, \
    mediadetails.MediaManage_AccompanyTrack, \
    mediafiles.MediaFile_Name, \
    medias.Media_IsReserved3, \
    medias.Media_IsReserved2, \
    mediadetails.Audio_Name, \
    medias.Media_HeaderSoundSequence, \
    medias.Media_IsReserved5, \
    medias.Media_HeadStroke, \
    medias.Media_StrokeNum, \
    medias.Media_AllSoundSequence, \
    medias.Media_ID, \
    medias.Media_Lyric, \
    medias.Media_IsMovie, \
    medias.Media_IsKaraok, \
    medias.Media_IsAds, \
    medias.media_light, \
    mediasmanage.MediaManage_OrderCount \
    from medias \
    LEFT JOIN mediadetails on medias.Media_SerialNo=mediadetails.Media_SerialNo \
    LEFT JOIN mediasmanage on medias.Media_Manage_ID=mediasmanage.MediaManage_ID \
    LEFT JOIN mediafiles on mediafiles.MediaFile_SerialNo=medias.Media_SerialNo*100 \
    LEFT JOIN languages on mediadetails.Language_Name=languages.Language_Name \
    where medias.Media_SerialNo=\''+str(no)+'\''
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        m_exportdata={}
        m_exportdata['Media_SerialNo']=row[0]
        m_exportdata['Media_Name']=row[1]
        m_exportdata['Language_Name']=row[2]
        m_exportdata['MediaManage_ID']=row[3]
        m_exportdata['Carrier_Name']=row[4]
        m_exportdata['MediaManage_OriginalTrack']=row[5]
        m_exportdata['MediaManage_AccompanyTrack']=row[6]
        m_exportdata['MediaFile_Name']=row[7]
        m_exportdata['Media_IsReserved3']=row[8]
        m_exportdata['Media_IsReserved2']=row[9]
        m_exportdata['Audio_Name']=row[10]
        m_exportdata['Media_HeaderSoundSequence']=row[11]
        m_exportdata['Media_IsReserved5']=row[12]
        m_exportdata['Media_HeadStroke']=row[13]
        m_exportdata['Media_StrokeNum']=row[14]
        m_exportdata['Media_AllSoundSequence']=row[15]
        m_exportdata['Media_ID']=row[16]
        m_exportdata['Media_Lyric']=row[17]
        m_exportdata['Media_IsMovie']=row[18]
        m_exportdata['Media_IsKaraok']=row[19]
        m_exportdata['Media_IsAds']=row[20]
        m_exportdata['medias_light']=row[21]
        m_exportdata['MediaManage_OrderCount']=row[22]
        ret.append(m_exportdata)
    cursor.close()
    return ret


def deleteFromMediafilesview():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = """
    delete from mediafilesview;
    """
    n = cursor.execute(sql)
    cursor.close()

def insertIntoMediafilesview():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = """
    INSERT into mediafilesview select MediaFile_SerialNo/100 as MediaFile_SerialNo,MediaFile_Name from mediafiles GROUP BY MediaFile_SerialNo;
    """
    n = cursor.execute(sql)
    cursor.close()

def sp_getexportdataAll():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select distinct medias.Media_SerialNo,medias.Media_Name, \
    mediadetails.Language_Name, \
    mediasmanage.MediaManage_ID, \
    mediadetails.Carrier_Name, \
    mediadetails.MediaManage_OriginalTrack, \
    mediadetails.MediaManage_AccompanyTrack, \
    mediafilesview.MediaFile_Name, \
    medias.Media_IsReserved3, \
    medias.Media_IsReserved2, \
    mediadetails.Audio_Name, \
    medias.Media_HeaderSoundSequence, \
    medias.Media_IsReserved5, \
    medias.Media_HeadStroke, \
    medias.Media_StrokeNum, \
    medias.Media_AllSoundSequence, \
    medias.Media_ID, \
    medias.Media_Lyric, \
    medias.Media_IsMovie, \
    medias.Media_IsKaraok, \
    medias.Media_IsAds \
    from medias \
    LEFT JOIN mediadetails on medias.Media_SerialNo=mediadetails.Media_SerialNo \
    LEFT JOIN mediasmanage on medias.Media_Manage_ID=mediasmanage.MediaManage_ID \
    LEFT JOIN mediafilesview on mediafilesview.MediaFile_SerialNo=medias.Media_SerialNo \
    LEFT JOIN languages on mediadetails.Language_Name=languages.Language_Name where medias.Media_IsKaraok=1'
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        m_exportdata={}
        m_exportdata['Media_SerialNo']=row[0]
        m_exportdata['Media_Name']=row[1]
        m_exportdata['Language_Name']=row[2]
        m_exportdata['MediaManage_ID']=row[3]
        m_exportdata['Carrier_Name']=row[4]
        m_exportdata['MediaManage_OriginalTrack']=row[5]
        m_exportdata['MediaManage_AccompanyTrack']=row[6]
        m_exportdata['MediaFile_Name']=row[7]
        m_exportdata['Media_IsReserved3']=row[8]
        m_exportdata['Media_IsReserved2']=row[9]
        m_exportdata['Audio_Name']=row[10]
        m_exportdata['Media_HeaderSoundSequence']=row[11]
        m_exportdata['Media_IsReserved5']=row[12]
        m_exportdata['Media_HeadStroke']=row[13]
        m_exportdata['Media_StrokeNum']=row[14]
        m_exportdata['Media_AllSoundSequence']=row[15]
        m_exportdata['Media_ID']=row[16]
        m_exportdata['Media_Lyric']=row[17]
        m_exportdata['Media_IsMovie']=row[18]
        m_exportdata['Media_IsKaraok']=row[19]
        m_exportdata['Media_IsAds']=row[20]
        ret.append(m_exportdata)
    cursor.close()
    return ret

def sp_getexportdataNullData():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select distinct medias.Media_SerialNo,medias.Media_Name, \
    mediadetails.Language_Name, \
    mediasmanage.MediaManage_ID, \
    mediadetails.Carrier_Name, \
    mediadetails.MediaManage_OriginalTrack, \
    mediadetails.MediaManage_AccompanyTrack, \
    mediafilesview.MediaFile_Name, \
    medias.Media_IsReserved3, \
    medias.Media_IsReserved2, \
    mediadetails.Audio_Name, \
    medias.Media_HeaderSoundSequence, \
    medias.Media_IsReserved5, \
    medias.Media_HeadStroke, \
    medias.Media_StrokeNum, \
    medias.Media_AllSoundSequence, \
    medias.Media_ID, \
    medias.Media_Lyric, \
    medias.Media_IsMovie, \
    medias.Media_IsKaraok, \
    medias.Media_IsAds \
    from medias \
    LEFT JOIN mediadetails on medias.Media_SerialNo=mediadetails.Media_SerialNo \
    LEFT JOIN mediasmanage on medias.Media_Manage_ID=mediasmanage.MediaManage_ID \
    LEFT JOIN mediafilesview on mediafilesview.MediaFile_SerialNo=medias.Media_SerialNo \
    LEFT JOIN languages on mediadetails.Language_Name=languages.Language_Name where medias.Media_IsKaraok=1 and medias.Media_Status=0'
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        m_exportdata={}
        m_exportdata['Media_SerialNo']=row[0]
        m_exportdata['Media_Name']=row[1]
        m_exportdata['Language_Name']=row[2]
        m_exportdata['MediaManage_ID']=row[3]
        m_exportdata['Carrier_Name']=row[4]
        m_exportdata['MediaManage_OriginalTrack']=row[5]
        m_exportdata['MediaManage_AccompanyTrack']=row[6]
        m_exportdata['MediaFile_Name']=row[7]
        m_exportdata['Media_IsReserved3']=row[8]
        m_exportdata['Media_IsReserved2']=row[9]
        m_exportdata['Audio_Name']=row[10]
        m_exportdata['Media_HeaderSoundSequence']=row[11]
        m_exportdata['Media_IsReserved5']=row[12]
        m_exportdata['Media_HeadStroke']=row[13]
        m_exportdata['Media_StrokeNum']=row[14]
        m_exportdata['Media_AllSoundSequence']=row[15]
        m_exportdata['Media_ID']=row[16]
        m_exportdata['Media_Lyric']=row[17]
        m_exportdata['Media_IsMovie']=row[18]
        m_exportdata['Media_IsKaraok']=row[19]
        m_exportdata['Media_IsAds']=row[20]
        ret.append(m_exportdata)
    cursor.close()
    return ret

def sp_getacotr(**media):
    cursor = None
    if media.has_key('isAllData'):
        cursor = conn.cursor()
    else:
        connn = getDataBaseConnection()
        cursor = connn.cursor()
    no = media['MediaManage_ID']
    sql='select actors.Actor_No,actors.Actor_Name,actortypes.ActorType_Name,actors.Actor_HeaderSoundSequence,actors.Actor_AllSoundSequence \
    from mediamanageactor \
    LEFT JOIN actors on actors.Actor_ID=mediamanageactor.Actor_ID \
    LEFT JOIN actortypes on actortypes.ActorType_ID=actors.Actor_Type_ID \
    where MediaManage_ID=\''+ str(no) +'\''
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        m_exportactor={}
        m_exportactor['Actor_No']=row[0]
        m_exportactor['Actor_Name']=row[1]
        m_exportactor['ActorType_Name']=row[2]
        m_exportactor['Actor_HeaderSoundSequence']=row[3]
        m_exportactor['Actor_AllSoundSequence']=row[4]
        ret.append(m_exportactor)
    cursor.close()
    return ret

def sp_getmediatype(**media):
    cursor = None
    if media.has_key('isAllData'):
        cursor = conn.cursor()
    else:
        connn = getDataBaseConnection()
        cursor = connn.cursor()
    no = media['MediaManage_ID']
    sql='select mediatypes.MediaType_Name from mediamanagetype \
    LEFT JOIN mediatypes on mediamanagetype.MediaType_ID=mediatypes.MediaType_ID \
    where mediamanagetype.MediaManage_ID=\''+ str(no) +'\''
    n = cursor.execute(sql)
    ret = []
    for row in cursor.fetchall():
        m_mediatype={}
        m_mediatype['MediaType_Name']=row[0]
        ret.append(m_mediatype)
    cursor.close()
    return ret

def sp_isnewsong(**media):
    cursor = None
    if media.has_key('isAllData'):
        cursor = conn.cursor()
    else:
        connn = getDataBaseConnection()
        cursor = connn.cursor()
    no = media['Media_ID']
    sql='select Media_ID from medianewsong where medianewsong.Media_ID=\''+ str(no) +'\''
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        cursor.close()
        return 1
    cursor.close()
    return 0

def sp_updateordercount(**media):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    id = media['Language_ID']
    no = media['Media_ID']
    num = media['MediaManage_OrderCount']
    sql='update mediassequence'+str(id)+' set MediaManage_OrderCount='+str(num)+' where Media_ID='+str(no)
    n = cursor.execute(sql)
    cursor.close()
    if n>0:
        return True
    else:
        return False

def sp_getmediasfromfilename(**media):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    name = media['Media_Name']
    no = 0
    name = name.split('.')
    name = name[0]
    sql = 'select medias.media_no from medias where medias.media_no=\''+name+'\''
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        no = row[0]
    cursor.close()
    return no


def scanvideos2(filepath,fn):

    print(filepath)
    if filepath[0] == '$':
        return
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            scanvideos(filepath + fi + "/",fn)
        else:
            if fi.endswith(".txt")==False:
    #             sql = "update mediafiles set MediaFile_Name='" + fi + "', MediaFile_IsValid='1' where MediaFile_SerialNo='" + fi + "'"
#                 sql = "insert into addmedia(AddMedia_Name, AddMedia_Path,AddMedia_SerialNo) values('" + fi + "','" + filepath + fi + "','"+ fi[0:fi.find(".")] +"')"
#                 n = cursor.execute(sql)
#                 conn.commit()
                fn(fi,filepath)
    cursor.close()

def updatepath():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql = "update mediafiles mf, addmedia am set mf.MediaFile_IsValid='1', mf.MediaFile_Name=am.AddMedia_Path "
        sql+= "where mf.MediaFile_Name=am.AddMedia_Name"
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    try:
        sql = "update medias ms, mediafiles mf,fileservers fs set Media_Status=1,Media_IsReserved4=fs.FileServer_Group_ID where concat( ms.Media_SerialNo, '00')= mf.MediaFile_SerialNo AND mf.MediaFile_ServerID=fs.FileServer_ID"
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

# def deleteAllFileData():
#     conn = getDataBaseConnection()
    cursor = conn.cursor()
#     sql = 'update mediafiles set MediaFile_IsValid=0'
#     cursor.execute(sql)
#     sql = 'update medias set Media_Status=0'
#     cursor.execute(sql)
#     conn.commit()
#     cursor.close()

def createMediasSequence():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql = 'call sp_startupForMedia()'
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

def getMedia_sequenceNoPY(initNo):
    i = {}
    i[0]=initNo
    def getNoPY():
        i[0]+=1
        return i[0]
    return getNoPY

def getSequence():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sequence = 0
    #获取歌曲的排序
    sql = "select MAX(media_sequence)+1 from medias where Media_Sequence<>''"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        sequence = row[0]
    if sequence is None:
        sequence = 1
    cursor.close()
    return sequence

def setUpdateDate():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        #修改设置的时间，以便dbass重新启动时能重新排序
        sql = "update systemsettinginfo set SettingInfo_Value = DATE_ADD(now(), INTERVAL -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime'"
        n = cursor.execute(sql)
    #     n = sp_execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

def addActorGetNo():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sequence = 0
    cursor.execute("select IFNULL(max(Actor_Sequence),0)+1 from actors where Actor_Sequence<>''")
    rows = cursor.fetchall()
    for row in rows:
        sequence = row[0]
    cursor.close()
    return sequence


def insertmediafilesbackups():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        n = cursor.execute("INSERT INTO mediafilesbackups select * from mediafiles")
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

def deleteMediaFilesData():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        n = cursor.execute("delete FROM mediafiles where mediafiles.MediaFile_IsValid=0")
        conn.commit()
    except:
        conn.rollback()
    cursor.close()


def checkDisk(fileList):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    fileArrList = {}
    cursor.execute("SELECT distinct mediafiles.MediaFile_Name FROM mediafiles")
    rows = cursor.fetchall()

    for row in rows:
        path = row[0]
#         print fileList.has_key(path[(path.rfind('/')+1):])
        if fileList.has_key(path[(path.rfind('/')+1):]):
            if fileArrList.has_key('h'):
                fileArrList['h']+=1
            else:
                fileArrList['h']=1
        else:
            if fileArrList.has_key('n'):
                fileArrList['n']+=1
            else:
                fileArrList['n']=1
    cursor.close()
    return fileArrList



def sp_AddActor2(**kwargs):

    cursorMusic = connMusic.cursor()
    try:
        if kwargs['actor_name']=='':
            cursorMusic.close()
            return 0

        actor_name = kwargs['actor_name']
        actor_typename = kwargs['actor_typename']
        actor_photo = kwargs['actor_photo']
        actor_jianpin = kwargs['actor_jianpin']
        actor_pinyin = kwargs['actor_pinyin']
        actor_no = kwargs['actor_no']
        actorNo = kwargs['actorNo']
        actorSequence = kwargs['actorSequence']

        sql = "insert into actors(Actor_ID, Actor_Name, Actor_Type_ID, Actor_Description,\
     Actor_IsSongerStar, Actor_Sequence, Actor_SoundSequence, Actor_PictureFilePath,\
    Actor_HeaderSoundSequence,Actor_OrderCount,Actor_AllSoundSequence,Actor_No) values \
    ("+str(actorNo())+",'"+actor_name+"',(select ActorType_ID from actortypes where ActorType_Name='"+actor_typename+"'),'"+actor_name+"',1,\
    "+str(actorSequence())+",'"+actor_jianpin[0]+"','"+actor_photo+"','"+actor_jianpin+"','0','"+actor_pinyin+"',"+actor_no+");"

        cursorMusic.execute(sql)
        connMusic.commit()
    except:
        connMusic.rollback()
    cursorMusic.close()

    return sql

def sp_UpdateActor2(**kwargs):

    cursorMusic = connMusic.cursor()
    if kwargs['actor_name']=='':
        cursorMusic.close()
        return 0
    try:
        actor_name = kwargs['actor_name']
        actor_typename = kwargs['actor_typename']
        actor_photo = kwargs['actor_photo']
        actor_jianpin = kwargs['actor_jianpin']
        actor_pinyin = kwargs['actor_pinyin']
        actor_no = kwargs['actor_no']
        typeid = kwargs['typeid']


        sql = "update actors set Actor_IsSongerStar = 1, Actor_Type_ID='" + str(typeid) + "',"
        sql += "Actor_Description='" + actor_name + "', Actor_SoundSequence = '" + actor_jianpin[0] + "',"
        sql += "Actor_HeaderSoundSequence='" + actor_jianpin + "', Actor_AllSoundSequence='" + actor_pinyin + "',"
        sql += "Actor_No='" + actor_no + "' where Actor_Name='" + actor_name + "'"

        print(sql)

        cursorMusic.execute(sql)
    except:
        connMusic.rollback()
    connMusic.commit()
    cursorMusic.close()

    return sql


def selectActorTypeList():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n = cursor.execute("select ActorType_ID,ActorType_Name from actortypes")
    rows = cursor.fetchall()
    ret = {}
    for row in rows:
        ret[row[1]]=row[0]
    cursor.close()
    return ret

def selectCarrierList():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n = cursor.execute("select Carrier_ID,Carrier_Name from carriers")
    rows = cursor.fetchall()
    ret = {}
    for row in rows:
        ret[row[1]]=row[0]
    cursor.close()
    return ret

def selectAudioList():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n = cursor.execute("select Audio_ID,Audio_Name from audios")
    rows = cursor.fetchall()
    ret = {}
    for row in rows:
        ret[row[1]]=row[0]
    cursor.close()
    return ret

def selectLanguageList():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    n = cursor.execute("select Language_ID,Language_Name from languages")
    rows = cursor.fetchall()
    ret = {}
    for row in rows:
        ret[row[1]]=row[0]
    cursor.close()
    return ret

def deleteAndInsertMediaManageActor():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql = "delete from mediamanageactor"
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    try:
        sql = "insert into mediamanageactor(MediaManage_ID, Actor_ID) \
    select mediadetails.Media_ID,actors.Actor_ID from mediadetails inner join actors on mediadetails.Actor_Name1=actors.Actor_Name where mediadetails.Actor_Name1!=''\
     UNION \
    select mediadetails.Media_ID,actors.Actor_ID from mediadetails inner join actors on mediadetails.Actor_Name2=actors.Actor_Name where mediadetails.Actor_Name2!=''\
     UNION \
    select mediadetails.Media_ID,actors.Actor_ID from mediadetails inner join actors on mediadetails.Actor_Name3=actors.Actor_Name where mediadetails.Actor_Name3!=''\
     UNION \
    select mediadetails.Media_ID,actors.Actor_ID from mediadetails inner join actors on mediadetails.Actor_Name4=actors.Actor_Name where mediadetails.Actor_Name4!=''"
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

def addMediaFilesForAddMedia():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql = "delete from mediafiles"
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    sql = "set @n = 0; \
insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo,MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid) \
select (@n := @n + 1), medias.Media_ID,concat(medias.Media_SerialNo,'00'),servergroups1.FileServer_ID,addMedia.AddMedia_Name,1,0 \
from medias inner join addMedia on medias.Media_SerialNo=addMedia.AddMedia_SerialNo and addMedia.AddMedia_Type=1 \
INNER JOIN servergroups1, fileservers where  servergroups1.FileServer_ID =fileservers.FileServer_ID and fileservers.fileserver_ismaingroup=1; \
insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo,MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid) \
select (@n := @n + 1), medias.Media_ID,concat(medias.Media_SerialNo,'00'),servergroups1.FileServer_ID,addMedia.AddMedia_Name,1,0 \
from medias inner join addMedia on medias.Media_SerialNo=addMedia.AddMedia_SerialNo and addMedia.AddMedia_Type=0 \
INNER JOIN servergroups1, fileservers where  servergroups1.FileServer_ID =fileservers.FileServer_ID and fileservers.fileserver_ismaingroup=0;"
    n = cursor.execute(sql)
    cursor.close()

def addShadowPath():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql = " update cloud_musicshadow,addmedia set savepath=AddMedia_Path where cloud_musicshadow.Shadow_no=addmedia.AddMedia_SerialNo;"
        n = cursor.execute(sql)
        conn.commit()
    except Exception as ex:
        print(traceback.format_exc())
        pass
    finally:
        cursor.close()

def addIsNewSongForAddMedias():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql="delete from medianewsong"
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    try:
        sql="INSERT INTO medianewsong(Media_ID,Media_InTime,Media_ValidUntil) select MediaManage_ID,MediaManage_RegisterTime,DATE_ADD(MediaManage_RegisterTime, INTERVAL 1 YEAR) from mediasmanage where mediasmanage.MediaManage_IsNew='1'"
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

def deleteCloudRecordForAddMedias():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql="delete from Cloud_MusicRecord where Cloud_MusicRecord.R_No in (SELECT medias.Media_ID from medias)"
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

def AddShadow(**kwargs):
    try:
        cursor = connMusic.cursor()
        print("kwargs: %s" % str(kwargs))

        serialno =  kwargs['serialno']
        type1 = kwargs['type1']
        type2 = kwargs['type2']
        ltype= kwargs['ltype']

        type1=filterText(type1)
        type2=filterText(type2)
        ltype=filterText(ltype)

        sql = "insert into cloud_musicshadow(Shadow_no, music_type) values('" + str(serialno) + "', '" + str(type1) + "')"
        n = cursor.execute(sql)
        connMusic.commit()
    except:
        connMusic.rollback()
        print(traceback.format_exc())
    cursor.close()


def mainAddMedias(**kwargs):
    try:
        cursor = connMusic.cursor()
        serialno =  kwargs['serialno']
        iname = kwargs['iname']
        lname = kwargs['lname']
        type1 = kwargs['type1']
        type2 = kwargs['type2']
        jianpin= kwargs['jianpin']
        pinyin= kwargs['pinyin']
        sname1= kwargs['sname1']
        sname2= kwargs['sname2']
        sname3= kwargs['sname3']
        sname4= kwargs['sname4']
        ltype= kwargs['ltype']
        if kwargs['volume'].isdigit():
            volume = kwargs['volume']
        else:
            volume = 10
        stroke= kwargs['stroke']
        bihua= kwargs['bihua']
        videoformat= kwargs['videoformat']
        media_carrier_id= kwargs['media_carrier_id']
        audioformat= kwargs['audioformat']
        media_audio_id= kwargs['media_audio_id']
        videotype= kwargs['videotype']
        ztrack= kwargs['ztrack']
        ytrack= kwargs['ytrack']
        isnew= kwargs['isnew']
        groupid= kwargs['groupid']
        filename= kwargs['filename']
        lyric= kwargs['lyric']


        iname=filterText(iname)
        lname=filterText(lname)
        type1=filterText(type1)
        type2=filterText(type2)
        jianpin=filterText(jianpin)
        pinyin=filterText(pinyin)
        sname1=filterText(sname1)
        sname2=filterText(sname2)
        sname3=filterText(sname3)
        sname4=filterText(sname4)
        ltype=filterText(ltype)
        lyric=filterText(lyric)


        orderCount=kwargs['orderCount']

        mediasNo = kwargs['mediasNo']

        media_id = mediasNo()
        mediamanage_id = media_id
        mediadetail_id = media_id
        manageid = mediamanage_id

        mediaSequence = kwargs['mediasSequence']
        sequence = mediaSequence()

        soundsequence = ''
        if jianpin != '':
            soundsequence = jianpin[0]

        marker = kwargs['marker']


        media_language_id = kwargs['media_language_id']

        sql = "insert into mediasmanage(MediaManage_ID,  MediaManage_Language_ID, MediaManage_Carrier_ID, MediaManage_Audio_ID, "
        sql+= "MediaManage_Format_ID, MediaManage_RegisterTime,MediaManage_IsNew, MediaManage_OriginalTrack, MediaManage_AccompanyTrack, MediaManage_OrderCount) "
        sql+= "values('" + str(mediamanage_id) +"','" +str(media_language_id) +"','" + str(media_carrier_id) + "',"
        sql +="'" + str(media_audio_id) + "','0', now()," + str(isnew) + ",'" + str(ztrack) +  "','" + str(ytrack) + "',\'"+str(orderCount)+"\')"

        n = cursor.execute(sql)


        sql = "insert into medias (Media_ID,Media_Name,Media_serialno,Media_Length,Media_Description,Media_Manage_ID,Media_Price,Media_Name_Length,"
        sql+= "Media_Sequence,Media_SoundSequence,Media_HeaderSoundSequence,Media_IsMovie,Media_IsKaraok,Media_IsAds,Media_CreatedbyCustomer,"
        sql+= "Media_IsReserved2,Media_IsReserved3,Media_IsReserved4,Media_IsReserved5,Media_HeadStroke,Media_StrokeNum,Media_Lyric,Media_AllSoundSequence, Media_Status) "
        sql+= "values('" + str(media_id) + "','" + str(iname) + "','" + str(serialno) + "','0','','" + str(manageid) + "','0','"+str(str_len(str(iname).replace(' ', '')))+"',"
        sql+= "'" + str(sequence) + "','" + str(soundsequence) + "','" + str(jianpin) + "','0','1','0','" + str(marker) + "','" + str(volume) + "','" + str(videotype) + "',"
        sql+= "'" + str(groupid) + "','" + str(ltype) + "','" + str(bihua) + "','"  + str(stroke) + "','" + str(lyric) + "','" + str(pinyin) + "','0')"
        n = cursor.execute(sql)

        sql = "insert into mediadetails(Media_ID, Media_Name, Media_SerialNo, Nation_Name, Language_Name, "
        sql+= "Actor_Name1, Actor_Name2, Actor_Name3, Actor_Name4, Director_Name1, Director_Name2, MediaType_Name1, MediaType_Name2,"
        sql+= "Carrier_Name, MediaManage_OriginalTrack, MediaManage_AccompanyTrack, MediaManage_OrderCount, MediaDetail_ID, "
        sql+= "Media_CreatedbyCustomer, Media_ExportMark, Media_Name_Length, Audio_Name, FileServer_ID, ServerGroup_ID) "
        sql+= "values('" + str(media_id) + "','" + str(iname) + "','" + str(serialno) + "','','" + str(lname) + "','"  + str(sname1) + "','" + str(sname2) + "',"
        sql+= "'" + str(sname3) + "','" + str(sname4) + "','','','" + str(type1) + "','" + str(type2) + "','" + str(videoformat) + "','" + str(ztrack) + "','" + str(ytrack) + "',"
        sql+= "'"+str(orderCount)+"','" + str(mediadetail_id) + "','" + str(marker) + "','0', '"+str(str_len(str(iname).replace(' ', '')))+"','" + str(audioformat) + "','" + str(groupid) + "','" + str(groupid) +"')"
        n = cursor.execute(sql)
        connMusic.commit()
    except:
        connMusic.rollback()
    cursor.close()

def UpdateShadow(**kwargs):
    cursor = connMusic.cursor()
#   serialno =  kwargs['serialno']
    type1 = kwargs['type1']
    type2 = kwargs['type2']
    ltype= kwargs['ltype']
    videotype= kwargs['videotype']


    type1=filterText(type1)
    type2=filterText(type2)
    ltype=filterText(ltype)

    media_id = kwargs['media_id']
    mediamanage_id = media_id

    media_language_id = kwargs['media_language_id']

    sql = "update medias set music_type='" + str(ltype) + "' where Media_ID=" + str(media_id)
    n = cursor.execute(sql)
    cursor.close()


def mainUpdateMedias(**kwargs):
    cursor = connMusic.cursor()
#     serialno =  kwargs['serialno']
    iname = kwargs['iname']
    lname = kwargs['lname']
    type1 = kwargs['type1']
    type2 = kwargs['type2']
    jianpin= kwargs['jianpin']
    pinyin= kwargs['pinyin']
    sname1= kwargs['sname1']
    sname2= kwargs['sname2']
    sname3= kwargs['sname3']
    sname4= kwargs['sname4']
    ltype= kwargs['ltype']
    volume= kwargs['volume']
    stroke= kwargs['stroke']
    bihua= kwargs['bihua']
    videoformat= kwargs['videoformat']
    media_carrier_id= kwargs['media_carrier_id']
    audioformat= kwargs['audioformat']
    media_audio_id= kwargs['media_audio_id']
    videotype= kwargs['videotype']
    ztrack= kwargs['ztrack']
    ytrack= kwargs['ytrack']
    isnew= kwargs['isnew']
    groupid= kwargs['groupid']
#     filename= kwargs['filename']
    lyric= kwargs['lyric']


    iname=filterText(iname)
    lname=filterText(lname)
    type1=filterText(type1)
    type2=filterText(type2)
    jianpin=filterText(jianpin)
    pinyin=filterText(pinyin)
    sname1=filterText(sname1)
    sname2=filterText(sname2)
    sname3=filterText(sname3)
    sname4=filterText(sname4)
    ltype=filterText(ltype)
    lyric=filterText(lyric)

    orderCount=kwargs['orderCount']

#     mediasNo = kwargs['mediasNo']


    media_id = kwargs['media_id']
    mediamanage_id = media_id
#     mediadetail_id = media_id
    manageid = mediamanage_id

    soundsequence = ''
    if jianpin != '':
        soundsequence = jianpin[0]

#     marker = kwargs['marker']


    media_language_id = kwargs['media_language_id']

    sql = "update medias set Media_Name='" + str(iname) + "',Media_Name_Length='"+str(str_len(str(iname).replace(' ', '')))+"',Media_SoundSequence='"+str(soundsequence)+"',"
    sql+= "Media_HeaderSoundSequence='" + str(jianpin) + "',Media_IsReserved2='" + str(volume) + "',"
    sql+= "Media_IsReserved3='" + str(videotype) + "',Media_IsReserved4='" + str(groupid) + "',Media_IsReserved5='" + str(ltype) + "',"
    sql+= "Media_HeadStroke='" + str(bihua) + "',Media_StrokeNum='" + str(stroke) + "',Media_Lyric='" + str(lyric) + "',Media_AllSoundSequence='" + str(pinyin) + "' "
    sql+= "where Media_ID=" + str(media_id)
    n = cursor.execute(sql)

    sql = "update mediadetails set Media_Name='" + str(iname) + "',Language_Name='" + str(lname) + "',Actor_Name1='" + str(sname1) + "',"
    sql+= "Actor_Name2='" + str(sname2) + "',Actor_Name3='" + str(sname3) + "',Actor_Name4='" + str(sname4) + "',MediaType_Name1='" + str(type1) + "',"
    sql+= "MediaType_Name2='" + str(type2) + "',Carrier_Name='" + str(videoformat) + "',MediaManage_OriginalTrack='" + str(ztrack) + "',"
    sql+= "MediaManage_AccompanyTrack='" + str(ytrack) + "',Media_Name_Length='"+str(str_len(str(iname).replace(' ', '')))+"',Audio_Name='" + str(audioformat) + "',ServerGroup_ID='" + str(groupid) + "' "
    sql+= "where Media_ID=" + str(media_id)
    n = cursor.execute(sql)

    sql = "update mediasmanage set MediaManage_AccompanyTrack='" + str(ytrack) + "',MediaManage_OriginalTrack='" + str(ztrack) + "',"
    sql+= "MediaManage_Audio_ID='" + str(media_audio_id) + "',MediaManage_Carrier_ID='" + str(media_carrier_id) + "',"
    sql+= "MediaManage_Language_ID='" + str(media_language_id) + "',MediaManage_IsNew='" + str(isnew) + "',MediaManage_OrderCount='"+str(orderCount)+"' "
    sql+= "where MediaManage_ID=" + str(manageid)
    n = cursor.execute(sql)
    cursor.close()

def scanvideos(output,isMain,fn):

    t = time.time()

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    fileListDsic={}

    num = 0
    results=[]

    #print status, output
    files = output.split('\n');
    path = ''
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            if file.lower().endswith('.txt')==False:
                if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True or file.lower().endswith('.ls')==True:
                    no = file[0:file.find('.')]
                    if fileListDsic.has_key(no)==False:
                        fileListDsic[no]=no
                        results.append([file, '/' + path + '/' + file,no,isMain])
                        fn(no)
            #print file + '    ' + path + '/' + file
        if len(results)==1000:
            sql = 'insert into addmedia(AddMedia_Name, AddMedia_Path, AddMedia_SerialNo,AddMedia_Type) values (%s,%s,%s,%s)'
            cursor.executemany(sql, results)
            conn.commit()
            num = num + len(results)
            del results[:]

    if len(results)>0:
        sql = 'insert into addmedia(AddMedia_Name, AddMedia_Path, AddMedia_SerialNo,AddMedia_Type) values (%s,%s,%s,%s)'
        cursor.executemany(sql, results)
        conn.commit()
        num = num + len(results)
        del results[:]

    print( time.time() - t )

def deleteAllData():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'delete from medias;\
           delete from actors;\
           delete from mediafiles;\
           delete from  cloud_musicshadow;'
    n = cursor.execute(sql)
    cursor.close()
    conn = getDataBaseConnection()
    cursor = conn.cursor()

    conn.commit()
    cursor.close()

def selectAllActorsDataForUpdateMedias():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select Actor_Name from actors'
    n = cursor.execute(sql)
    ret = {}
    for row in cursor.fetchall():
        ret[row[0]]=''
    return ret

def selectAllMediaDataForUpdateMedias():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select Media_ID,Media_SerialNo from medias'
    n = cursor.execute(sql)
    ret = {}
    for row in cursor.fetchall():
        ret[row[1]]=row[0]
    return ret

def selectAllShadowDataForUpdateMedias():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select id, Shadow_no from cloud_musicshadow'
    n = cursor.execute(sql)
    ret = {}
    for row in cursor.fetchall():
        ret[row[1]]=row[0]
    return ret



def deleteAllAddMedias():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    try:
        sql = 'delete from addmedia'
        n = cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()

# def deleteNotFindMedia():
#     cursorForNotFind = connForNotFind.cursor()
#     sql = 'delete from notfindmedia'
#     n = cursorForNotFind.execute(sql)
#     connForNotFind.commit()
#     cursorForNotFind.close()

# def addNotFindMedia(cursorForNotFind,sql,result):
#     n = cursorForNotFind.executemany(sql,result)

# def createConnForNotFind():
#     cursorForNotFind = connForNotFind.cursor()
#     return cursorForNotFind

# def closeConnForNotFind(cursorForNotFind):
#     connForNotFind.commit()
#     cursorForNotFind.close()
#     connForNotFind.close()

def startCreateManagerType():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'delete from mediamanagetype'
    n = cursor.execute(sql)
    conn.commit()

    sql='insert into mediamanagetype(MediaManage_ID, MediaType_ID) select MediaDetail_ID,MediaType_ID from mediatypes,mediadetails where mediadetails.MediaType_Name1=mediatypes.MediaType_Name OR mediadetails.MediaType_Name2=mediatypes.MediaType_Name OR mediadetails.MediaType_Name3=mediatypes.MediaType_Name'
    n = cursor.execute(sql)
    conn.commit()
    cursor.close()


def scanFilesFormOutput(output):
    t = time.time()
    fileListDsic={}
    #print status, output
    files = output.split('\n')
    path = ''
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            if file.lower().endswith('.txt')==False:
                if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True or file.lower().endswith('.ls')==True:
                    no = file[0:file.find('.')]
                    if fileListDsic.has_key(no)==False:
                        fileListDsic[no]='/' + path + '/' + file
    print( time.time() - t )
    return fileListDsic

def addmediaToFiles(no):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql="delete from mediafiles where MediaFile_SerialNo='"+str(no)+"00';"
    n = cursor.execute(sql)
    conn.commit()
    id = sp_GetFirstAvailableID(table='mediafiles', columname='MediaFile_ID')


    sql="set @n = "+str(id)+"; \
insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo,MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid) \
select (@n := @n + 1), medias.Media_ID,concat(medias.Media_SerialNo,'00'),servergroups1.FileServer_ID,addMedia.AddMedia_Path,1,0 \
from medias inner join addMedia on medias.Media_SerialNo=addMedia.AddMedia_SerialNo and addMedia.AddMedia_Type=1 \
INNER JOIN servergroups1, fileservers where  servergroups1.FileServer_ID =fileservers.FileServer_ID and fileservers.fileserver_ismaingroup=1 and addMedia.AddMedia_SerialNo='"+str(no)+"'; \
insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo,MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid) \
select (@n := @n + 1), medias.Media_ID,concat(medias.Media_SerialNo,'00'),servergroups1.FileServer_ID,addMedia.AddMedia_Path,1,0 \
from medias inner join addMedia on medias.Media_SerialNo=addMedia.AddMedia_SerialNo and addMedia.AddMedia_Type=0 \
INNER JOIN servergroups1, fileservers where  servergroups1.FileServer_ID =fileservers.FileServer_ID and fileservers.fileserver_ismaingroup=0 and addMedia.AddMedia_SerialNo='"+str(no)+"';"
    n = cursor.execute(sql)
    cursor.close()

def getIpIsMain(ip):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select f.FileServer_IsMainGroup from fileservers f where f.FileServer_IpAddress='"+str(ip)+"'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        return row[0]
    return None

def login(username,password):
    try:
        connLogin = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')
        cursorLogin = connLogin.cursor()
        sql = "select count(Staff_ID) from staffs where Staff_SerialNo='"+str(username)+"' and Staff_Password='"+str(password)+"'"
        n = cursorLogin.execute(sql)
        count = 0
        for row in cursorLogin.fetchall():
            count=row[0]
        cursorLogin.close()
        connLogin.close()
        return count
    except:
        pass
    return None

def selectMediaTypeForMap():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select MediaType_Name from mediatypes'
    n = cursor.execute(sql)
    ret = {}
    for row in cursor.fetchall():
        ret[row[0]]=''
    return ret

def updateDeleteForStorNo(tableName,lineName,id):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'UPDATE '+ str(tableName) +' SET '+ str(lineName) +'='+ str(lineName) +'-1 WHERE '+ str(lineName) +'>'+ str(id) +' ORDER BY '+ str(lineName) +' ASC'
    n = cursor.execute(sql)
    cursor.close()

def selectAllDeleteMedia():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select Media_ID,Media_NO from deleteMedia'
    n = cursor.execute(sql)
    ret = {}
    for row in cursor.fetchall():
        ret[row[1]]=row[0]
    return ret

def deleteDeleteMedia(id):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'DELETE FROM deletemedia where Media_ID='+str(id)
    n = cursor.execute(sql)
    conn.commit()
    cursor.close()

def getMediaFileCountFromIp(ip):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select COUNT(mediafiles.MediaFile_ID) from mediafiles INNER JOIN fileservers on mediafiles.MediaFile_ServerID=fileservers.FileServer_ID WHERE fileservers.FileServer_IpAddress=\''+ip+'\''
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        return row[0]
    return None

def getAddMediaFileFormScpOtherService(no,ip):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select fileservers.FileServer_IpAddress,(select addmedia.AddMedia_Path from addmedia where addmedia.AddMedia_SerialNo=\''+str(no)+'\') from fileservers where fileservers.FileServer_IsMainGroup=(\
select fileservers.FileServer_IsMainGroup from fileservers where fileservers.FileServer_IpAddress=\''+str(ip)+'\') AND fileservers.FileServer_IpAddress!=\''+str(ip)+'\''
    n = cursor.execute(sql)
    ret={}
    for row in cursor.fetchall():
        ret[row[0]]=row[1]
    return ret

def sp_removeDuplicateMediatype():
    try:
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        n = cursor.execute("update mediatypes set MediaType_IsKaraok=1 where MediaType_IsKaraok>1")
        conn.commit()
        n = cursor.execute("select MediaType_Name, min(MediaType_ID) from mediatypes GROUP BY MediaType_Name having count(MediaType_Name)>1")
        for row in cursor.fetchall():
            cursor.execute("delete from mediatypes where MediaType_Name='" + row[0] + "' and MediaType_ID!=" + str(row[1]))
        cursor.close()
    except:
        print traceback.print_exc()

def createInitProcedure():
    try:
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        existed = 0
        n = cursor.execute("show procedure STATUS where name='sp_getmediainfofor3d'")
        for row in cursor.fetchall():
            existed = 1
        if existed == 0:
            print("create sp_getmediainfofor3d proc");
            sql =  """CREATE procedure sp_getmediainfofor3d(in Time varchar(30))
                proc:BEGIN
                select md.servergroup_id,md.media_serialno,md.media_id,md.media_name ,m.Media_HeaderSoundSequence
                            ,0 as language_id,m.Media_IsReserved3,m.Media_IsReserved5,actor_name1,a1.actor_id as actor_id1 ,a1.Actor_Type_ID as Actor_Type_ID1,a1.Actor_HeaderSoundSequence as Actor_HeaderSoundSequence1,a1.Actor_AllSoundSequence as Actor_AllSoundSequence1
                            ,actor_name2,a2.actor_id as actor_id2 ,a2.Actor_Type_ID as Actor_Type_ID2,a2.Actor_HeaderSoundSequence as Actor_HeaderSoundSequence2,a2.Actor_AllSoundSequence as Actor_AllSoundSequence2
                            ,actor_name3,0 as actor_id3 ,0 as Actor_Type_ID3,'' as Actor_HeaderSoundSequence3,'' as Actor_AllSoundSequence3
                            ,actor_name4,0 as actor_id4 ,0 as Actor_Type_ID4,'' as Actor_HeaderSoundSequence4,'' as Actor_AllSoundSequence4
                            ,m.Media_Lyric,md.MediaManage_OrderCount,Media_StarLevel,m.Media_AllSoundSequence
                            ,0 as mediatype_id1,MediaType_Name1,0 as mediatype_id2,MediaType_Name2
                            from mediadetails md
                            left join actors a1 on md.Actor_name1=a1.actor_name
                            left join actors a2 on md.Actor_name2=a2.actor_name
                            left join medias m on m.media_id=md.media_id
                            where  Media_IsKaraok=1 order by md.MediaManage_OrderCount desc,md.media_id;
                end;"""
            n = cursor.execute(sql)
        else:
            print("sp_getmediainfofor3d proc existed !!!")
    except:
        print traceback.print_exc()

def initDataBase():
    try:
#         createSQLTabel("""
#         CREATE TABLE IF NOT EXISTS `addmedia` (
#           `AddMedia_ID` int(11) NOT NULL AUTO_INCREMENT,
#           `AddMedia_Name` varchar(50) DEFAULT NULL,
#           `AddMedia_Path` varchar(200) DEFAULT NULL,
#           `AddMedia_Type` varchar(30) DEFAULT NULL,
#           `AddMedia_Size` int(11) DEFAULT NULL,
#           `AddMedia_CreateDate` datetime DEFAULT NULL,
#           `AddMedia_UpdateDate` datetime DEFAULT NULL,
#           `AddMedia_State` int(11) DEFAULT NULL,
#           `AddMedia_SerialNo` varchar(10) DEFAULT NULL,
#           PRIMARY KEY (`AddMedia_ID`),
#           KEY `index_Name` (`AddMedia_Name`),
#           KEY `index_SerialNo` (`AddMedia_SerialNo`)
#         )
#         """)
#         createSQLTabel("""
#         CREATE TABLE IF NOT EXISTS `deletemedia` (
#           `Media_ID` int(11) NOT NULL,
#           `Media_NO` varchar(10) CHARACTER SET utf8 NOT NULL,
#           PRIMARY KEY (`Media_ID`)
#         )
#         """)
#         createSQLTabel("""
#         alter table movie_library add column( ktvprice  numeric(8,2) default 0.0, infosource  int);
#         """)
#         createSQLTabel("""
#         alter table mediafiles modify column MediaFile_IsValid int default 1;
#         """)
#         createSQLTabel("""
#         CREATE TABLE IF NOT EXISTS `logs` (
#           `id` int(11) NOT NULL AUTO_INCREMENT,
#           `host` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#           `app` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
#           `title` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
#           `event` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
#           `time` datetime DEFAULT NULL,
#           `level` char(1) CHARACTER SET utf8 DEFAULT NULL,
#           `flag` char(1) CHARACTER SET utf8 DEFAULT NULL,
#           PRIMARY KEY (`id`)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#         """)
        createSQLTabel("""
            drop view v_mediadetails;
        """)
        createSQLTabel("""
            create view v_mediadetails
            as
            select `a`.`Media_ID` AS `Media_ID`,`a`.`Media_Name` AS `Media_Name`,`a`.`Media_SerialNo` AS `Media_SerialNo`,
            `a`.`Nation_Name` AS `Nation_Name`,`a`.`Language_Name` AS `Language_Name`,
            `a`.`Actor_Name1` AS `Actor_Name1`,`a`.`Actor_Name2` AS `Actor_Name2`,`a`.`Actor_Name3` AS `Actor_Name3`,`a`.`Actor_Name4` AS `Actor_Name4`,
            `a`.`Director_Name1` AS `Director_Name1`,`a`.`Director_Name2` AS `Director_Name2`,
            `a`.`MediaType_Name1` AS `MediaType_Name1`,`a`.`MediaType_Name2` AS `MediaType_Name2`,`a`.`MediaType_Name3` AS `MediaType_Name3`,
            `a`.`Carrier_Name` AS `Carrier_Name`,
            `a`.`MediaManage_OriginalTrack` AS `MediaManage_OriginalTrack`,
            `a`.`MediaManage_AccompanyTrack` AS `MediaManage_AccompanyTrack`,
            `a`.`MediaManage_OrderCount` AS `MediaManage_OrderCount`,
            `a`.`MediaDetail_ID` AS `MediaDetail_ID`,`a`.`Media_CreatedbyCustomer` AS `Media_CreatedbyCustomer`,
            `a`.`Media_ExportMark` AS `Media_ExportMark`,`a`.`Media_Name_Length` AS `Media_Name_Length`,
            `a`.`Audio_Name` AS `Audio_Name`,`a`.`FileServer_ID` AS `FileServer_ID`,`a`.`ServerGroup_ID` AS `ServerGroup_ID`,
            ifnull(`b`.`Actor_ID`,0) AS `actor_id1`,ifnull(`c`.`Actor_ID`,0) AS `actor_id2`,
            ifnull(`d`.`Actor_ID`,0) AS `actor_id3`,ifnull(`e`.`Actor_ID`,0) AS `actor_id4`
            from ((((`mediadetails` `a` left join `actors` `b` on((`a`.`Actor_Name1` = `b`.`Actor_Name`)))
            left join `actors` `c` on((`a`.`Actor_Name2` = `c`.`Actor_Name`))) left join `actors` `d` on((`a`.`Actor_Name3` = `d`.`Actor_Name`)))
            left join `actors` `e` on((`a`.`Actor_Name4` = `e`.`Actor_Name`)));
        """)
#         createSQLTabel("""
#             CREATE TABLE MenPaiAdSettings(
#             MenPaiAdSetting_Id int auto_increment PRIMARY key,
#             MenPaiAdSetting_SerialNo varchar(10) NULL ,
#             MenPaiAdSetting_PlayCount int NULL DEFAULT 1 ,
#             MenPaiType_ID int NULL DEFAULT 0 ,
#             MenPaiAdSettings_RoomID int NULL DEFAULT 0
#             )
#         """)
        createSQLTabel("""
        INSERT INTO `staffs` VALUES ('1', 'admin', 'admin', '系统管理员', '5', '1', null, '0', null, null, null, null, null, null, null, 'Y', null, null, '0.00', '0.00')
        """)
#         createSQLTabel("""
#         alter table movie_library add column( ktvprice  numeric(8,2) default 0.0, infosource  int);
#         """)
#         createSQLTabel("""
#         alter table fileservers modify column FileServer_ModifyDate varchar(40) default NULL;
#         """)
#         createSQLTabel("""
#         alter table fileservers modify column  FileServer_ExpireDate  varchar(40) default NULL;
#         """)
#         createSQLTabel("""
#         CREATE TABLE mediafilesview(
#           MediaFile_SerialNo int(10) NOT NULL PRIMARY key,
#           MediaFile_Name varchar(255) DEFAULT NULL
#         )
#         """)
        sp_removeDuplicateMediatype()
        createInitProcedure()

#         createSQLTabel("""
#         DELIMITER $$
#         DROP PROCEDURE if EXISTS sp_testPROCEDURE_sp;
#         CREATE PROCEDURE `sp_testPROCEDURE_sp`()
#         BEGIN
#         if not exists (SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE table_name = 'movie_library' AND COLUMN_NAME = 'ktvprice') then
#             alter table movie_library add column( ktvprice  numeric(8,2) default 0.0, infosource  int);
#         else
#           begin end;
#         end if;
#         END$$
#         CALL sp_testPROCEDURE_sp()$$
#         DELIMITER ;
#         """)

        print '创建表完成'
    except:
        print '创建表失败'
        pass

def updateDatabase():
    print("updateDatabase")
    result = commands.getstatusoutput("cat /etc/network/interfaces | sed -n '/address/p' | awk '{print $2}'")
    ips = result[1]
    result = commands.getstatusoutput("cat /etc/odbc.ini | sed -n '/SERVER/p' | cut -d= -f2 | tail -n 1 | sed s/[[:space:]]//g")
    mysql = result[1]
    print("network " + ips)
    print("mysql " +  mysql)
    if mysql=="127.0.0.1" or mysql in ips:
        initDataBase()
        print("database can be updated")
    else:
        print("skip update")
    print("updateDatabase over")

#updateDatabase()

def scanLyricText():
    otpList = {}
    output = commands.getoutput('ls -R /video/*')
    files = output.split('\n')
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            if file.lower().endswith('.txt')==True:
                otpList[file[0:file.find(".")]]='/' + path + '/' + file
    return otpList

def saveLyricText(no,text):
    cursor = conn.cursor()
    try:
        if len(text) > 2048:
            text = text[:2048]
        sql = "UPDATE medias SET Media_Lyric='"+str(text).replace("'", "''")+"' WHERE Media_SerialNo='"+str(no)+"'"
        n = cursor.execute(sql)
        cursor.close()
        if n > 0:
            return True
    except:
        return False
    return False


def addMessage(obj):
    id=''
    connMessage = getDataBaseConnection()
    cursorMessage = connMessage.cursor()
    sql="INSERT INTO `mesgs`(mesg_ip,mesg_app,mesg_title,mesg_content,mesg_time,mesg_level,mesg_flag) VALUES ('"+str(obj['ip'])+"', '"+str(obj['app'])+"', '"+str(obj['title'])+"', '"+str(obj['content'])+"', '"+str(obj['time'])+"', '"+str(obj['state'])+"', '"+str(obj['unRead'])+"');"
    n = cursorMessage.execute(sql)
    n = cursorMessage.execute("select last_insert_id();")
    for row in cursorMessage.fetchall():
        id=row[0]
    connMessage.commit()
    cursorMessage.close()
    return id

def updateUnRead(id):
    connMessage = getDataBaseConnection()
    cursorMessage = connMessage.cursor()
    sql = "UPDATE `mesgs` SET mesg_flag=1"
    if id != "":
        sql += " WHERE mesg_id='"+str(id)+"'"
    n = cursorMessage.execute(sql)
    connMessage.commit()
    cursorMessage.close()

def selectMessage(page,count):
    connMessage = getDataBaseConnection()
    cursorMessage = connMessage.cursor()
    sql='SELECT * from `mesgs` ORDER BY mesg_time desc LIMIT '+str(int(page)-1)+','+str(count)+';'
    n = cursorMessage.execute(sql)
    res=[]
    for row in cursorMessage.fetchall():
        obj={}
        obj['id']=row[0]
        obj['ip']=row[1]
        obj['app']=row[2]
        obj['title']=row[3]
        obj['content']=row[4]
        obj['time']=row[5]
        obj['state']=row[6]
        obj['unRead']=row[7]
        res.append(obj)
    return res

def selectAllMusicNoArrList():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select Media_SerialNo from medias'
    n = cursor.execute(sql)
    ret=[]
    for row in cursor.fetchall():
        ret.append(row[0])
    return ret

def spm_getserialnoIsAdvertisement():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select max(medias.Media_SerialNo) from medias where medias.Media_SerialNo > 3000000 and medias.Media_SerialNo < 4000000"
    n = cursor.execute(sql)
    no = 0
    for row in cursor.fetchall():
        no = row[0]
    if no == None or no == 0:
        return 3000000
    return int(no)+1

def selectConfigures55():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select Configure_Set55 from configures'
    n = cursor.execute(sql)
    result=0
    for row in cursor.fetchall():
        result=row[0]
    return result

def setConfigures55(data):

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'update configures SET Configure_Set55='+str(data)
    n = cursor.execute(sql)
    cursor.close()

def deleteMediaUserSet():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'delete from mediauserset'
    n = cursor.execute(sql)
    conn.commit()
    cursor.close()

def selectAdvertisementIdList():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select Media_ID from medias where Media_IsAds='1';"
    n = cursor.execute(sql)
    ret=[]
    for row in cursor.fetchall():
        ret.append(row[0])
    return ret

def selectAllAddMedia():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select media_type,media_no,media_name,media_file,media_no from medias where medias.media_no>=9000000;"
    n = cursor.execute(sql)
    ret=[]
    for row in cursor.fetchall():
        M_AddMedia={}
        M_AddMedia['AddMedia_Type']=row[0]
        M_AddMedia['AddMedia_ID']=row[1]
        M_AddMedia['AddMedia_UpdateDate']='0000-00-00'
        M_AddMedia['AddMedia_Name']=row[2]
        M_AddMedia['AddMedia_Size']=0
        M_AddMedia['AddMedia_CreateDate']='0000-00-00'
        M_AddMedia['AddMedia_Path']=row[3]
        M_AddMedia['AddMedia_SerialNo']=row[4]
        M_AddMedia['AddMedia_State']=1
        ret.append(M_AddMedia)
    return ret

def getOtherFileListSerialNo():

    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = 'select medias.Media_SerialNo,medias.Media_Name from medias;'
    n = cursor.execute(sql)
    ret={}
    for row in cursor.fetchall():
        ret[row[0]]=row[1]
    cursor.close()
    return ret

def insertMeidaFilesForAddMedia(serialno,filename,groupid=1):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select medias.Media_Manage_ID from medias where medias.Media_SerialNo='"+str(serialno)+"'"
    manageid = ""
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        manageid = row[0]

#添加歌曲到mediafiles
    sql = "delete from mediafiles where MediaFile_MediaManage_ID=" + str(manageid)
    n = cursor.execute(sql)
#     n = sp_execute(sql)

    #错误定义，标记循环结束
    sql = "select FileServer_ID, ServerGroup_ID from servergroups1 where FileServer_IsValid = 1 and ServerGroup_ID='" + str(groupid) +"'"
    n = cursor.execute(sql)
    mediafilesNo = getMedia_sequenceNoPY(sp_createuniqueid( table = 'mediafiles', columname='MediaFile')-1)
    for row in cursor.fetchall():
#         mediafile_id = sp_createuniqueid( table = 'mediafiles', columname='MediaFile')
        mediafile_id = mediafilesNo()
        sql = "insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo, "
        sql+= "MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid) "
        sql+= "values('" + str(mediafile_id) + "','" + str(manageid) + "', "
        sql+= "concat('" + str(serialno) + "','00'),'" + str(row[0]) + "','" + str(filename) + "','1','0')"
        n = cursor.execute(sql)

    conn.commit()
    cursor.close()

def getFileServerIdFromIp(ip):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select FileServer_ID from fileservers where FileServer_IpAddress='"+str(ip)+"'"
    id = ""
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        id = row[0]
    return id
def upfilepath(fileList,id):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in fileList:
        results.append([fileList[no],str(no)+"00",id])
        if len(results)==1000:
            sql="UPDATE mediafiles SET MediaFile_Name=%s where MediaFile_SerialNo=%s AND MediaFile_ServerID=%s;"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="UPDATE mediafiles SET MediaFile_Name=%s where MediaFile_SerialNo=%s AND MediaFile_ServerID=%s;"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def updateActorOrderCount():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql="update actors a, mediadetails b set actor_ordercount=actor_ordercount+b.MediaManage_OrderCount where a.Actor_Name = b.Actor_Name1"
    n = cursor.execute(sql)
    cursor.close()


def filterText(text):
    try:
        text=pymysql.escape_string(str(text))
    except:
        text="_ERROR_"
        logger.error(traceback.format_exc())
        logger.error(text)
        print traceback.format_exc()
        print text
    return text

def getFileServerAllGroup():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select DISTINCT FileServer_Group_ID from fileservers"
    res=[]
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        res.append(row[0])
    return res

def getFileServerAllIp(groupId):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "select FileServer_IpAddress from fileservers where FileServer_Group_ID='"+str(groupId)+"'"
    res=[]
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        res.append(row[0])
    return res

def scanvideosArr(output,fn):
    t = time.time()
    files = output.split('\n');
    path = ''
    print len(files)
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            if file.lower().endswith('.txt')==False:
                if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True or file.lower().endswith('.ls')==True:
                    no = file[0:file.find('.')]
                    pa = '/' + path + '/' + file
                    fn(no,pa)
    print( time.time() - t )

def selectAllDataForNullData(dataList,groupId):
    conn = getDataBaseConnection()
    cursor = conn.cursor()

    sql = 'drop table if exists mediafilesviewForNullData;'
    n = cursor.execute(sql)
    conn.commit()
    print 'drop - OK'

    createSQLTabel("""
        CREATE TABLE mediafilesviewForNullData(
            MediaFile_SerialNo int(10) NOT NULL PRIMARY key,
            MediaFile_Name varchar(255) DEFAULT NULL,
            MediaFile_ServerID int DEFAULT NULL
        );
    """)
    print 'mediafilesviewForNullData - OK'
    sql = 'INSERT into mediafilesviewForNullData select MediaFile_SerialNo/100 as MediaFile_SerialNo,MediaFile_Name,MediaFile_ServerID from mediafiles GROUP BY MediaFile_SerialNo'
    n = cursor.execute(sql)
    conn.commit()
    print 'insert - OK'

    sql = "select Media_SerialNo,MediaFile_Name from medias inner join mediafilesviewForNullData on medias.Media_SerialNo=MediaFile_SerialNo inner join fileservers on MediaFile_ServerID=fileservers.FileServer_ID where fileservers.FileServer_Group_ID='"+str(groupId)+"'"
    res={}
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        no=row[0]
        path=row[1]
        m1 = md5.new()
        m1.update(path)
        md5Str = m1.hexdigest()
        if md5Str not in dataList:
            res[no]=""
    print 'select - OK'

    return res

def deleteMediamanageactorForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediamanageactor where mediamanageactor.MediaManage_ID=(select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediamanageactor where mediamanageactor.MediaManage_ID=(select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediamanagedirectorForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediamanagedirector where MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediamanagedirector where MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediamanagetypeForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediamanagetype where MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediamanagetype where MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediafilesForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediafiles where MediaFile_MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediafiles where MediaFile_MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediasmenuForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediasmenu where MediaMenu_Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediasmenu where MediaMenu_Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediasForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from medias where Media_SerialNo=%s;"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from medias where Media_SerialNo=%s;"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediasmanageForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediasmanage where MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediasmanage where MediaManage_ID = (select medias.Media_Manage_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediadetailsForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediadetails where Media_SerialNo = %s;"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediadetails where Media_SerialNo = %s;"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMeidasindexForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from meidasindex where MeidasIndex_Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from meidasindex where MeidasIndex_Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMedianewsongForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from medianewsong where Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from medianewsong where Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def deleteMediasorderForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="delete from mediasorder where MediaOrder_Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="delete from mediasorder where MediaOrder_Media_ID = (select medias.Media_ID from medias where Media_SerialNo=%s);"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]


def updateSystemsettinginfoForNullData():
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    sql = "update systemsettinginfo set SettingInfo_Value = Date_Add(now(), Interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    sp_execute(sql)
    conn.commit()
    cursor.close()

def updateMediasForNullData(noList):
    conn = getDataBaseConnection()
    cursor = conn.cursor()
    results=[]
    for no in noList:
        results.append([no])
        if len(results)==1000:
            sql="update medias set Media_Status=0 where Media_SerialNo=%s;"
            cursor.executemany(sql, results)
            conn.commit()
            del results[:]
    sql="update medias set Media_Status=0 where Media_SerialNo=%s;"
    cursor.executemany(sql, results)
    conn.commit()
    del results[:]

def cloud_music_get_count():
    total = 0
    conn = getKaraokConn_dict()
    cursor = conn.cursor()
    sql = "select count(*) as total from cloud_musicinfo"
    cursor.execute(sql)
    rows = cursor.fetchall()
    print rows
    for row in rows:
        if row is not None:
              total = row['total']
    cursor.close()
    return total

def cloud_music_get_list(offset, limit):
    mlist = []
    sql = "select * from cloud_musicinfo order by music_lastverdate desc limit %d, %d" % (offset, limit)
    conn = getKaraokConn_dict()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    mlist = rows
    return mlist

