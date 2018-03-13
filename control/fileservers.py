#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
from lib import http
from orm import orm as _mysql
from setting import MYSQL
from control.modbc import get_all_thunder_ini
from urllib import urlencode
conn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')

#conn.close()


def get_conn():
    tconn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')
    return tconn

def foo(*args,**kwargs):
    print('args=',args)
    print('kwargs=',kwargs)
    print('**********************')



def restartdb():
    closedb()
    opendb()

def opendb():
    global conn
    conn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')
# 	print('open mysql')

def closedb():
    try:
	   conn.close()
    except:
        pass

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
    cursor = conn.cursor()
    try:
        n = cursor.execute(sql)
        cursor.close()
        return n
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
        cursor.close()
        return n
	

def sp_sql2json(sql):
	print("!!!!sql2json not implements!!!!")



def sp_createuniqueid(**kwargs):
	tabname = kwargs['table']
	objname = kwargs['columname']
	if tabname=='' or objname =='':
		return -1;
	conn = pymysql.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], password=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')
	ncount = 1
	sql = "select count(*) from " + tabname
	cursor = conn.cursor()
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		ncount = row[0]
	if ncount>0:
		sql = "select max(" + objname + "_ID) + 1 from " + tabname
		cursor = conn.cursor()
		n = cursor.execute(sql)
		for row in cursor.fetchall():
			ncount = row[0]

	cursor.close()
	print("sp_createuniqueid: " + tabname + "." + objname + " " + str(ncount))
	return ncount


def sp_GetFirstAvailableID(**kwargs):
	tabname = kwargs['table']
	objname = kwargs['columname']

	id = 1
	cursor = conn.cursor()
	sql = "select max(" + objname + ")+1 from " + tabname
	print(sql)
	cursor.execute(sql);
	rows = cursor.fetchall()
	for row in rows:
		id =  row[0]
	cursor.close()
	print("sp_GetFirstAvailableID: " + tabname + "." + objname + " " + str(id))
	return id

#in actor_no int, in actor_name nvarchar(256), in actor_typename nvarchar(8),
#in actor_photo nvarchar(256), in actor_jianpin nvarchar(256),
#in actor_pinyin nvarchar(256), out actor_id int
def sp_AddActor(**kwargs):
	if kwargs['actor_name']=='':
		return 0

	typeid = 0
	sql = ''

	cursor = conn.cursor()
	cursor.execute("select ActorType_ID from actortypes where ActorType_Name='"+ kwargs['actor_typename'] + "'");
	rows = cursor.fetchall()
	for row in rows:
		typeid = row[0]

	sequence = 0
	cursor.execute("select IFNULL(max(Actor_Sequence),0)+1 from actors where Actor_Sequence<>''");
	rows = cursor.fetchall()
	for row in rows:
		sequence = row[0]

	soundsequence=''
	cursor.execute("select (case when length('" + kwargs['actor_jianpin']+ "') <= 0 then '' else substring('" + kwargs['actor_jianpin']+"',1, 1) end)");
	for row in cursor.fetchall():
		soundsequence = row[0]

	r_id = 0
	cursor.execute("select Actor_ID, Actor_PictureFilePath from actors where Actor_Name='" + kwargs['actor_name'] + "'");
	rows = cursor.fetchall()
	for row in rows:
		r_id = row[0]

	print(r_id)
	sql = ''
	if(r_id==0):
		id = sp_GetFirstAvailableID(table='actors', columname='Actor_ID')
		r_id = id;
		sql = "insert into actors(Actor_ID, Actor_Name, Actor_Type_ID, Actor_Description, Actor_IsSongerStar, Actor_Sequence, Actor_SoundSequence, Actor_PictureFilePath, "
		sql += "Actor_HeaderSoundSequence,Actor_AllSoundSequence,Actor_No) values "
		sql += "('" + str(r_id) + "','" + kwargs['actor_name'] + "','" + str(typeid) + "','" + kwargs['actor_name'] + "',1,'" + str(sequence) + "','" + soundsequence + "',"
		sql += "'" + kwargs['actor_photo'] + "','" + kwargs['actor_jianpin'] + "','" + kwargs['actor_pinyin'] + "','" + kwargs['actor_no'] + "')"
	else:
		sql = "update actors set Actor_IsSongerStar = 1, Actor_Type_ID='" + str(typeid) + "',"
		sql += "Actor_Description='" + kwargs['actor_name'] + "', Actor_SoundSequence = '" + soundsequence + "',"
		sql += "Actor_HeaderSoundSequence='" + kwargs['actor_jianpin'] + "', Actor_AllSoundSequence='" + kwargs['actor_pinyin'] + "',"
		sql += "Actor_No='" + kwargs['actor_no'] + "' where Actor_Name='" + kwargs['actor_name'] + "'"
	print(sql)
	cursor.execute(sql);
	cursor.close()
	return r_id;

#serverIp NVARCHAR(50), mid, no, version, date
def sp_ImportMaterial(**kwargs):
	sql  = "insert into Cloud_ServerImport(Import_No,Import_Version,Import_Versiondate,Import_Ip,Import_Mid,Import_Type) values("
	sql += "'" + kwargs['no'] + "','" + kwargs['version'] + "','" + kwargs['date'] + "','" + kwargs['serverIp'] + "','" + kwargs['mid']+"',1)"
	print(sql)
	cursor = conn.cursor()
	cursor.execute(sql);

	_have = 0
	sql = "select fileserver_ipAddress from fileservers a, servergroups b, Cloud_ServerImport c "
	sql+= "where FileServer_Group_ID = ServerGroup_ID and fileserver_ipAddress=Import_Ip and Import_Mid='" + kwargs['mid'] + "' and Import_Type=1"
	print(sql)

	cursor.execute(sql);
	rows = cursor.fetchall()
	for row  in rows:
		_have = 1
	print('_have: ' + str(_have))
	if(_have==1):
		sql = "update cloud_Material set operation=2 where mid='" + kwargs['mid'] + "'"
		print(sql)
		cursor = conn.cursor()
		cursor.execute(sql);

	cursor.close()

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
	sql = ''
	flag = 0
	if curid=='':
		return 1
	if int(typeid)<0 or int(typeid)>6:
		return 1
	if description=='':
		description = name
	cursor = conn.cursor()
	if int(curid)>101 or int(curid) <= 0:
		flag = 0
		sql = "select MediaType_ID from mediatypes where MediaType_ID = '" +  str(curid) + "'"
		print('1: '+ sql)
		cursor.execute(sql);
		rows = cursor.fetchall()
		for row  in rows:
			flag = 1
		if flag==1:
			curid = sp_GetFirstAvailableID(table='mediatypes', columname='MediaType_ID')
		if curid<101:
			curid = 101

	sql = ''
	if typeid==0:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and MediaType_IsMovie = 1"
	elif typeid==1:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and MediaType_IsKaraok = 1"
	elif typeid==2:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and MediaType_IsAds = 1"
	elif typeid==3:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 or MediaType_IsKaraok = 1)"
	elif typeid==4:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 or MediaType_IsAds = 1)"
	elif typeid==5:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsKaraok = 1 or MediaType_IsAds = 1)"
	else:
		sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "' and (MediaType_IsMovie = 1 or MediaType_IsKaraok = 1 or MediaType_IsAds = 1)"
	flag = 0
	print('2: '+ sql)
	cursor.execute(sql);
	rows = cursor.fetchall()
	for row in rows:
		flag = 1

	if flag==1:
		cursor.close()
		return 2
	flag = 0
	sql = "select MediaType_Name from mediatypes where MediaType_Name='" + iname + "'"
	print('3: '+ sql)
	cursor.execute(sql);
	rows = cursor.fetchall()
	for row in rows:
		flag = 1

	if flag==1:
		if typeid == 0:
			sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
		elif typeid == 1:
			sql = "update mediatypes set MediaType_IsKaraok= 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
		elif typeid == 2:
			sql = "update mediatypes set MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
		elif typeid == 3:
			sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsKaraok = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
		elif typeid == 4:
			sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
		elif typeid == 5:
			sql = "update mediatypes set MediaType_IsKaraok = 1, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
		else:
			sql = "update mediatypes set MediaType_IsMovie = 1, MediaType_IsKaraok = 1, MediaType_IsAds = 1, MediaType_Description = '" + description + "' where MediaType_Name = '" + iname + "'"
	else:
		if typeid == 0:
			sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie) values "
			sql += "('" + str(curid) + "','" + iname + "','" + description + "',1)"
		elif typeid == 1:
			sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsKaraok) values "
			sql+="('" + str(curid) + ",'" + iname + "','" + description + "',1)"
		elif typeid == 2:
			sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsAds) values "
			sql+="('" + str(curid) + "','" + iname + "','" + description + "',1)"
		elif typeid == 3:
			sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok) values "
			sql+="('" + str(curid) + ",'" + iname + "','" + description + "',1)"
		elif typeid == 4:
			sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsAds) values "
			sql +="('" + str(curid) + "','" + iname + "','" + description + "',1)"
		elif typeid == 5:
			sql = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsKaraok, MediaType_IsAds) values "
			sql +="(" + str(curid) + ",'" + iname + "','" + description + "',1)"
		else:
			sql  = "insert into mediatypes(MediaType_ID, MediaType_Name, MediaType_Description, MediaType_IsMovie, MediaType_IsKaraok, MediaType_IsAds) values "
			sql +="('" + str(curid) + "','" + iname + "','" + description + "',1,1,1)"

	print('4: '+ sql)
	cursor.execute(sql)

	sql = "update systemsettinginfo set SettingInfo_Value = dateadd(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
	print('5: '+ sql)
	cursor.execute(sql);
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

#serialno int,           --编号
#name nvarchar(256),     --歌曲名称
#lname nvarchar(16),     --语言
#type1 nvarchar(16),     --类型
#type2 nvarchar(16),     --类型
#jianpin nvarchar(256),  --简拼
#pinyin nvarchar(256),   --全拼
#sname1 nvarchar(256),   --歌星名称
#sname2 nvarchar(256),   --歌星名称
#sname3 nvarchar(256),	 --歌星名称
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
#isnew int,              -- 是否新歌
#groupid int,            --歌曲组ID
#filename nvarchar(256), --文件保存目录
#lyric nvarchar(2048)    --歌词
# cloud_sp_addmedias
def sp_addmedias(**kwargs):
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
	volume= kwargs['volume']
	stroke= kwargs['stroke']
	bihua= kwargs['bihua']
	videoformat= kwargs['videoformat']
	audioformat= kwargs['audioformat']
	videotype= kwargs['videotype']
	ztrack= kwargs['ztrack']
	ytrack= kwargs['ytrack']
	isnew= kwargs['isnew']
	groupid= kwargs['groupid']
	filename= kwargs['filename']
	lyric= kwargs['lyric']

	if videoformat=='':
		videoformat = 'MPEG1'

	if audioformat=='':
		audioformat = 'MPEG'

	if groupid=='':
		groupid = '1'

	marker = sp_getaddmediamark()

	if marker<0 or marker>1:
		marker = 0

	sequence = '0'
	soundsequence = ''
	cursor = conn.cursor()
	#获取歌曲的排序
	sql = "select IFNULL(MAX(media_sequence),0)+1 into @sequence from medias  where Media_Sequence<>''"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		sequence = row[0]

	#获取歌曲首字母
	sql = "select case when length('" + jianpin + "') <= 0 then null else substring('" + jianpin  + "', 1, 1) end"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		 soundsequence = row[0]

	#获取视频格式ID
	media_carrier_id = ''
	sql = "select Carrier_ID from carriers where Carrier_Name='" + videoformat + "'"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		 media_carrier_id = row[0]

	if media_carrier_id=='':
		sql = "select Carrier_ID from carriers where Carrier_Name = 'MPEG1'"
		n = cursor.execute(sql)
		for row in cursor.fetchall():
			media_carrier_id = row[0]
	#获取音频格式ID
	media_audio_id = ''
	sql = "select Audio_ID into @media_audio_id from audios where Audio_Name = '" + audioformat + "'"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		 media_audio_id = row[0]

	if media_audio_id=='':
		sql = "select Audio_ID from audios where Audio_Name = 'MPEG'"
		n = cursor.execute(sql)
		for row in cursor.fetchall():
			media_audio_id = row[0]

	media_language_id = '0'
	sql = "select Language_ID from languages where Language_Name='" + lname + "'"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		 media_language_id = row[0]

	media_id = '0'
	manageid = '0'
	sql = "select Media_id, Media_Manage_ID from medias where Media_SerialNo='" + serialno + "'"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
		media_id = row[0]
		manageid = row[1]

	if media_id=='0':
		mediamanage_id = sp_createuniqueid(table='mediasmanage', columname='MediaManage')
		media_id = sp_createuniqueid(table='medias', columname='Media')

		if media_id>mediamanage_id:
			mediamanage_id = media_id
		else:
			media_id = mediamanage_id

		#添加mediasmanage表
		sql = "insert into mediasmanage(MediaManage_ID,  MediaManage_Language_ID, MediaManage_Carrier_ID, MediaManage_Audio_ID, "
		sql+= "MediaManage_Format_ID, MediaManage_RegisterTime,MediaManage_IsNew, MediaManage_OriginalTrack, MediaManage_AccompanyTrack) "
		sql+= "values('" + str(mediamanage_id) +"','" +str(media_language_id) +"','" + str(media_carrier_id) + "',"
		sql +="'" + str(media_audio_id) + "','0', now()," + isnew + ",'" + ztrack +  "','" + ytrack + "')"
		n = cursor.execute(sql)

		manageid = mediamanage_id

		sql = "insert into medias (Media_ID,Media_Name,Media_serialno,Media_Length,Media_Description,Media_Manage_ID,Media_Price,Media_Name_Length,"
		sql+= "Media_Sequence,Media_SoundSequence,Media_HeaderSoundSequence,Media_IsMovie,Media_IsKaraok,Media_IsAds,Media_CreatedbyCustomer,"
		sql+= "Media_IsReserved2,Media_IsReserved3,Media_IsReserved4,Media_IsReserved5,Media_HeadStroke,Media_StrokeNum,Media_Lyric,Media_AllSoundSequence) "
		sql+= "values('" + str(media_id) + "','" + iname + "','" + str(serialno) + "','0','0','" + str(manageid) + "','0','" + str(len(iname)) + "',"
		sql+= "'" + str(sequence) + "','" + str(soundsequence) + "','" + str(jianpin) + "','0','1','0','" + str(marker) + "','" + str(volume) + "','" + str(videotype) + "',"
		sql+= "'" + str(groupid) + "','" + str(ltype) + "','" + str(bihua) + "','" + str(stroke) + "','" + lyric + "','" + pinyin + "')"

		print(sql)
		n = cursor.execute(sql)
		conn.commit()

		mediadetail_id = sp_createuniqueid( table='mediadetails', columname='MediaDetail')

		sql = "insert into mediadetails(Media_ID, Media_Name, Media_SerialNo, Nation_Name, Language_Name, "
		sql+= "Actor_Name1, Actor_Name2, Actor_Name3, Actor_Name4, Director_Name1, Director_Name2, MediaType_Name1, MediaType_Name2,"
		sql+= "Carrier_Name, MediaManage_OriginalTrack, MediaManage_AccompanyTrack, MediaManage_OrderCount, MediaDetail_ID, "
		sql+= "Media_CreatedbyCustomer, Media_ExportMark, Media_Name_Length, Audio_Name, FileServer_ID, ServerGroup_ID) "
		sql+= "values('" + str(media_id) + "','" + iname + "','" + str(serialno) + "','','" + lname + "','"  + sname1 + "','" + sname2 + "',"
		sql+= "'" + sname2 + "','" + sname4 + "','','','" + str(type1) + "','" + str(type2) + "','" + str(videoformat) + "','" + ztrack + "','" + ytrack + "',"
		sql+= "'0','" + str(mediadetail_id) + "','" + str(marker) + "','0', length('" + iname + "'),'" + str(audioformat) + "','" + str(groupid) + "','" + str(groupid) +"')"
		n = cursor.execute(sql)

		conn.commit()
	else:
		sql = "update medias set Media_Name='" + iname + "',Media_Name_Length=length('" + iname + "'),Media_SoundSequence=@soundsequence,"
		sql+= "Media_HeaderSoundSequence='" + jianpin + "',Media_IsReserved2='" + volume + "',"
		sql+= "Media_IsReserved3='" + videotype + "',Media_IsReserved4='" + str(groupid) + "',Media_IsReserved5='" + ltype + "',"
		sql+= "Media_HeadStroke='" + bihua + "',Media_StrokeNum='" + stroke + "',Media_Lyric='" + lyric + "',Media_AllSoundSequence='" + pinyin + "' "
		sql+= "where Media_ID=" + str(media_id)
		n = cursor.execute(sql)
		conn.commit()
		sql = "update mediadetails set Media_Name='" + iname + "',Language_Name='" + lname + "',Actor_Name1='" + sname1 + "',"
		sql+= "Actor_Name2='" + sname2 + "',Actor_Name3='" + sname3 + "',Actor_Name4='" + sname4 + "',MediaType_Name1='" + type1 + "',"
		sql+= "MediaType_Name2='" + type2 + "',Carrier_Name='" + videoformat + "',MediaManage_OriginalTrack='" + ztrack + "',"
		sql+= "MediaManage_AccompanyTrack='" + ytrack + "',Media_Name_Length=length('" + iname + "'),Audio_Name='" + audioformat + "',ServerGroup_ID='" + groupid + "' "
		sql+= "where Media_ID=" + str(media_id)
		n = cursor.execute(sql)
		conn.commit()
		sql = "update mediasmanage set MediaManage_AccompanyTrack='" + ytrack + "',MediaManage_OriginalTrack='" + ztrack + "',"
		sql+= "MediaManage_Audio_ID='" + str(media_audio_id) + "',MediaManage_Carrier_ID='" + str(media_carrier_id) + "',"
		sql+= "MediaManage_Language_ID='" + str(media_language_id) + "',MediaManage_IsNew='" + isnew + "' "
		sql+= "where MediaManage_ID=" + str(manageid)
		n = cursor.execute(sql)
		conn.commit()

	#添加歌曲对应歌星ID表
	sql = "delete from mediamanageactor where MediaManage_ID=" + str(manageid)
	n = cursor.execute(sql)

	sql = "insert into mediamanageactor(MediaManage_ID, Actor_ID) "
	sql+= "select " + str(manageid) + ", Actor_ID from actors where Actor_Name in ('" + sname1 + "','"+ sname2 +"','" + sname3 + "','" + sname4 + "')"
	n = cursor.execute(sql)

	#添加歌曲分类
	sql = "delete from mediamanagetype where MediaManage_ID=" + str(manageid)
	n = cursor.execute(sql)

	sql = "insert into mediamanagetype(MediaManage_ID, MediaType_ID)"
	sql+= "select  " + str(manageid) + ", MediaType_ID from mediatypes where MediaType_Name in('" + type1 + "','" +type2 + "')"
	n = cursor.execute(sql)

	#添加歌曲到mediafiles
	sql = "delete from mediafiles where MediaFile_MediaManage_ID=" + str(manageid)
	n = cursor.execute(sql)

	#错误定义，标记循环结束
	sql = "select FileServer_ID, ServerGroup_ID from servergroups1 where FileServer_IsValid = 1 and ServerGroup_ID='" + groupid +"'"
	n = cursor.execute(sql)
	for row in cursor.fetchall():
            mediafile_id = sp_createuniqueid( table = 'mediafiles', columname='MediaFile')
            sql = "insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo, "
            sql+= "MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence) "
            sql+= "values('" + str(mediafile_id) + "','" + str(manageid) + "',"
            sql+= "concat('" + serialno + "','00'),'" + groupid + "','" + filename + "','1')"

            sp_execute(sql)

	if isnew==1:
		ncount = 0
		sql = "select count(*) from medianewsong where Media_ID=" + str(media_id)
		n = cursor.execute(sql)
		for row in cursor.fetchall():
			ncount = row[0]

		if ncount<1:
			sql = "INSERT INTO medianewsong(Media_ID,Media_InTime,Media_ValidUntil) values('" + media_id + "', now(), DATE_ADD(now(), INTERVAL 1 YEAR))"
			n = cursor.execute(sql)

	sql = "delete from Cloud_MusicRecord where R_No='" + serialno + "'"
	n = cursor.execute(sql)

	#修改设置的时间，以便dbass重新启动时能重新排序
	sql = "update systemsettinginfo set SettingInfo_Value = DATE_ADD(now(), INTERVAL -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime'"
	n = cursor.execute(sql)

	cursor.close()

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

    print("@@@@@@@ sp_getserialno : " + media_name)
    ##################################
    if typeid=='' or int(typeid)<0 or int(typeid)>8:
        return -100
    if media_name=='':
        return -101
    cursor = conn.cursor()

    maxserialno = '9000000'
    sql = "select max(cast(Media_SerialNo as int))+1 from medias where cast(Media_SerialNo as int) >= 9000000"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        maxserialno = row[0]

    if maxserialno>9999999:
        cursor.close()
        return -102
    cursor.close()

    return maxserialno


#isMenpai 是否是门牌广告 0，普通 1，门牌广告
def spm_getserialno(**kwargs):
    media_name = kwargs['media_name']
    media_actor_name1 = kwargs['media_actor_name1']
    media_actor_name2 = kwargs['media_actor_name2']
    media_actor_name3 = kwargs['media_actor_name3']
    media_actor_name4 = kwargs['media_actor_name4']

    media_type_name1 = kwargs['media_type_name1']
    media_type_name2 = kwargs['media_type_name2']
    media_type_name3 = kwargs['media_type_name3']

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
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor_name1 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id1 = row[0]

    media_actor_id2 = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor_name2 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id2 = row[0]

    media_actor_ids = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor_name3 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id3 = row[0]

    media_actor_id4 = ''
    sql = "select Actor_ID from actors where Actor_Name ='" + media_actor_name4 + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_actor_id4 = row[0]

    if media_actor_id1 == media_actor_id2 or media_actor_id1 == media_actor_id3 or media_actor_id1 == media_actor_id4 or \
			media_actor_id2 == media_actor_id3 or media_actor_id2 == media_actor_id or media_actor_id3 == media_actor_id4:
        cursor.close()
        return -4

    media_type_id1 = ''
    cursor = "select MediaType_ID from mediatypes where MediaType_Name ='" + media_type_name1 + "'"
    curosr.execute(sql)
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
    if media_type_id1 == media_type_id2 or media_type_id1 == media_type_id3 or media_type_id2 == media_type_id3:
        return -5

    n = sp_getserialno(media_name, media_actor_id1, media_actor_id2, media_actor_id3, media_actor_id4, media_type_id1, media_type_id2, media_type_id3, typeid, roup_id, fileserver_id, isMenpai)

    cursor.close()
    return n

#media_id normalid = null,
#media_name name = null
def sp_deletemedia(**kwargs):
    media_id = kwargs['media_id']
    media_name = kwargs['media_name']

    sql = "select md.media_name, md.media_serialno, Actor_Name1, Actor_Name2, Actor_Name3, Actor_Name4, language_name,"
    sql+= "Media_IsReserved2, Mediatype_name1, Mediatype_name2, Mediatype_name3, Carrier_Name,MediaManage_OriginalTrack,"
    sql+= "MediaManage_AccompanyTrack,Media_IsReserved3,Audio_name,Media_HeaderSoundSequence,Media_IsReserved4,Media_StrokeNum,"
    sql+= "Media_HeadStroke,Media_IsReserved5,Media_unitedCode,Media_IsAds,Media_IsMovie,Media_IsKaraok from mediadetails md,medias m "
    sql+= "where md.media_id=m.media_id and m.media_id='" + media_id +" ' and md.media_id=m.media_id"
    cursor = conn.cursor()

    media_manage_id = '0'
    sql = "select  Media_Manage_ID from medias where Media_ID ='" + media_id + "'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        media_manage_id = row[0]
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

    sql = "delete from medianewsong where Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)

    sql = "delete from mediasorder where MediaOrder_Media_ID = '" + str(media_id) + "'"
    sp_execute(sql)


    sql = "update systemsettinginfo set SettingInfo_Value = Date_Add(now(), Interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    sp_execute(sql)

    cursor.close()


def sp_addfileserver(**kwargs):
    name = kwargs['name']
    ipaddress = kwargs['ipaddress']
    os = kwargs['os']
    isvalid = kwargs['isvalid']
    group_id = kwargs['group_id']
    group_name = kwargs['group_name']
    isMain=kwargs['ismain']

    if name==''  or len(name) < 1 or ipaddress=='':
        return -1
    if group_id=='' and group_name=='':
        return -2
    
    cursor = conn.cursor()
    _existed = 0
    sql = "select 1 from FileServers where FileServer_IpAddress = '" + ipaddress + "'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    for row in cursor.fetchall():
        _existed = 1
    if _existed==1:
        cursor.close();
        return -3


    if group_id > 0:
        sql = "select ServerGroup_Name from ServerGroups where ServerGroup_ID = '" + str(group_id) + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            group_name = row[0]
    else:
        if group_name!='':
            sql = "select ServerGroup_ID from ServerGroups where ServerGroup_Name = '" + group_name + "'"
            n = cursor.execute(sql)
            for row in cursor.fetchall():
                group_id = row[0]
    if group_id=='':
        cursor.close()
        return -4

    iExistsSameGroupServerID = '-1'
    sql = "SELECT FileServer_ID FROM FileServers WHERE FileServer_Group_ID = '" + str(group_id) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        iExistsSameGroupServerID = row[0]
    print "iExistsSameGroupServerID"+str(iExistsSameGroupServerID)

    curid = sp_createuniqueid(table='FileServers', columname='FileServer')
    if curid==0:
        curid=1
    sql = "insert into FileServers(FileServer_ID, FileServer_Name, FileServer_IpAddress, FileServer_OS, FileServer_CreateDate, FileServer_IsValid, FileServer_Group_ID, FileServer_IsMainGroup) values "
    sql+= "('" + str(curid) + "','"+ name + "','"+ ipaddress + "','" + os + "', now(),'" +str(isvalid) + "','" + str(group_id) + "', '"+str(isMain)+"')"
    try:
        n = cursor.execute(sql)
        conn.commit()
        cursor.close()
    except:
        cursor.close()
        conn.rollback()
        return -4
    #该组已经加过歌，则把组中歌曲复制一份给该服务器，如此在新添加服务器时不用给每个服务器都加歌。
    cursor = conn.cursor()
    if int(iExistsSameGroupServerID) > 0:

        _existed = 0
        sql = "SELECT 1 FROM MediaFiles WHERE MediaFile_ServerID = '" + str(iExistsSameGroupServerID) + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            _existed = row[0]

        print str(_existed)
        if _existed==1:

            #MediaFile_RegisterTime DATETIME default(getdate())
            sql = "create temporary table tMediaFiles(MediaFile_ID int not null,MediaFile_SerialNo VARCHAR(100) null,MediaFile_MediaManage_ID INT null, MediaFile_Name VARCHAR(250) null,"
            sql+= "MediaFile_Sequence INT,MediaFile_IsValid INT, MediaFile_RegisterTime varchar(40), MediaFile_AutoID int AUTO_INCREMENT PRIMARY KEY)"
            n = cursor.execute(sql)
            conn.commit()

            iMaxMediaFile_ID = sp_createuniqueid(table='MediaFiles', columname='MediaFile')

            sql = "INSERT INTO tMediaFiles(MediaFile_SerialNo, MediaFile_MediaManage_ID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid, MediaFile_RegisterTime) "
            sql+= "SELECT MediaFile_SerialNo, MediaFile_MediaManage_ID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid, MediaFile_RegisterTime "
            sql+= "FROM MediaFiles WHERE MediaFile_ServerID = '" + str(iExistsSameGroupServerID) + "'"
            n = cursor.execute(sql)
            conn.commit()



            sql  ="INSERT INTO MediaFiles(MediaFile_ID, MediaFile_SerialNo, MediaFile_MediaManage_ID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid, MediaFile_RegisterTime, MediaFile_ServerID) "
            sql +="SELECT " + str(iMaxMediaFile_ID) + "+ MediaFile_AutoID, MediaFile_SerialNo, MediaFile_MediaManage_ID, MediaFile_Name, MediaFile_Sequence, MediaFile_IsValid, MediaFile_RegisterTime, '" + str(curid) + "' "
            sql += "FROM tMediaFiles"
            n = cursor.execute(sql)
            sql="drop table tMediaFiles"
            n = cursor.execute(sql)
            conn.commit()



    sql = "update systemsettinginfo set SettingInfo_Value = date_add(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    # sql = "update SystemsettingInfo set SettingInfo_Value = Date_Add(now(), INTERVAL -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and  SettingInfo_Value<>''"
    n = cursor.execute(sql)
    conn.commit()


    cursor.close()

    return 0


def sp_modifyfileserver(kwargs):
    id = kwargs['id']
    ipaddress = kwargs['ipaddress']
    new_name = kwargs['new_name']
    new_ipaddress = kwargs['new_ipaddress']
    os = kwargs['os']
    isvalid = '1'
    group_id = kwargs['group_id']
    group_name = kwargs['group_name']
    cursor = conn.cursor();

    if id>0:
        sql = "select FileServer_IpAddress from FileServers where FileServer_ID = '" + str(id) + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            ipaddress = row[0]
    elif ipaddress!='':
        sql = "select  FileServer_ID from FileServers where FileServer_IpAddress = '" + ipaddress + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            id = row[0]
    if id=='':
        cursor.close()
        return -1
    print id
    _existed = 0
    sql = "select 1 from FileServers where FileServer_IpAddress = '" + new_ipaddress + "' and FileServer_ID = '" + str(id) + "'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    for row in cursor.fetchall():
        _existed = row[0]
    if _existed==1:
        cursor.close()
        return -2

    if os==None:
        os = ''
#     if isvalid==None or int(isvalid)!=0  or int(isvalid)!=1:
#         isvalid = ''
    if group_id > 0:
        sql = "select ServerGroup_Name from ServerGroups where ServerGroup_ID = '" + str(group_id) + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            group_name = row[0]
    elif group_name!=None:
        sql = "select ServerGroup_ID into @group_id from ServerGroups where ServerGroup_Name = '" + group_name + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            group_id = row[0]
    sql = "update FileServers set FileServer_Name = ifnull('" + new_name + "', FileServer_Name), "
    sql+= "FileServer_IpAddress = ifnull('" + new_ipaddress + "', FileServer_IpAddress),"
    sql+= "FileServer_OS = ifnull('" + os + "', FileServer_OS),"
    sql+= "FileServer_IsValid = ifnull('" + str(isvalid) + "', FileServer_IsValid),"
    sql+= "FileServer_Group_ID = ifnull('" + str(group_id) + "', FileServer_Group_ID)"
    sql+= "where FileServer_ID = '" + str(id) + "' and FileServer_IpAddress = '" + ipaddress + "'"
    print sql
    try:
        cursor.execute(sql)
    # sql = "update SystemsettingInfo set SettingInfo_Value = DateAdd(now(), INTERVAL -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and  SettingInfo_Value<>''"
        sql1 = "update systemsettinginfo set SettingInfo_Value = date_add(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
        cursor.execute(sql1)
        cursor.close()
        conn.commit()
    except:
        cursor.close()
        conn.rollback()
        
    return 0

# def sp_deletefileserver(**kwargs):
#     id = kwargs['rid']
#     ipaddress = kwargs['ipaddress']

#     if id=='' or ipaddress=='':
#         return 1

#     cursor = conn.cursor()
#     if id=='' and ipaddress!='':
#         sql = "select FileServer_Group_ID from fileservers where FileServer_IpAddress='" + ipaddress + "'"
#         for row in cursor.fetchall():
#             id = row[0]
#     if id=='':
#         return 2

#     sql = "delete from MediaFiles where MediaFile_ServerID = " + str(id)
#     sp_execute(sql)

#     sql = "delete from FileServerConnectionInfo where FileServer_ID ='" + str(id) + "'"
#     sp_execute(sql)

#     sql = "delete from FileServers where FileServer_ID = '"+ str(id) + "' and FileServer_IpAddress ='" + ipaddress + "'"
#     sp_execute(sql)

#     groupid = 0
#     sql = "select FileServer_Group_ID from fileservers where FileServer_ID = '" + str(id) + "'"
#     n = cursor.execute(sql)
#     for row in cursor.fetchall():
#         groupid = row[0]

#     _have = 0
#     sql = "select 1 from fileservers where FileServer_Group_ID = '" + str(groupid) + "'"
#     n = cursor.execute(sql)
#     for row in cursor.fetchall():
#         _have = row[0]

#     if _have == 0:
#         sql = "select a.media_id from medias a, mediadetails b where a.media_serialno=b.Media_SerialNo and a.Media_IsReserved4='" + str(groupid) + "'"
#         n = cursor.execute(sql)
#         for row in cursor.fetchall():
#             sp_deletemedia( mediaid=row[0], media_name='')

#     cursor.close()

def sp_deletefileserver(**kwargs):
    id = kwargs['rid']
    ipaddress = kwargs['ipaddress']

    if id=='' and ipaddress=='':
        return 1

    cursor = conn.cursor()
    if id=='' and ipaddress!='':
        sql = "select FileServer_ID from fileservers where FileServer_IpAddress='" + ipaddress + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            id = row[0]
    if id=='':
        return 2

    sql = "delete from MediaFiles where MediaFile_ServerID = " + str(id)
    sp_execute(sql)

    sql = "delete from FileServerConnectionInfo where FileServer_ID ='" + str(id) + "'"
    sp_execute(sql)

    sql = "delete from FileServers where FileServer_ID = '"+ str(id) + "' and FileServer_IpAddress ='" + ipaddress + "'"
    sp_execute(sql)

    groupid = 0
    sql = "select FileServer_Group_ID from fileservers where FileServer_ID = '" + str(id) + "'"
    print 111
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        groupid = row[0]

    _have = 0
    sql = "select 1 from fileservers where FileServer_Group_ID = '" + str(groupid) + "'"
    print 222
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        _have = row[0]

    if _have == 0 or _have==None:
        sql = "select a.media_id from medias a, mediadetails b where a.media_serialno=b.Media_SerialNo and a.Media_IsReserved4='" + str(groupid) + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            sp_deletemedia( mediaid=row[0], media_name='')

    cursor.close()
    return 0

def sp_check_by_address(address):
    cursor = conn.cursor()
    sql="select FileServer_Group_ID from FileServers where FileServer_IpAddress ='"+str(address)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    groupsid=4
    for row in cursor.fetchall():
        groupsid=row[0]
        print 'xxxgroupsidxxxxx'
    
    if sp_check_only_fileserver(groupsid)==1:
        
        return sp_check_is_have_media(groupsid)
    else:
        print 'xxxrowxx','ssssssssssssss'
        cursor.close()
        return False


def sp_check_is_have_media(groupsid):
    cursor = conn.cursor()
    ishave=0
    sql="SELECT * FROM medias WHERE Media_IsReserved4 ='"+str(groupsid)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    for row in cursor.fetchall():
        print 'xxxrowxx',row
        ishave=1
    cursor.close()
    if ishave==1:
        return True
    else:
        return False

def sp_check_only_fileserver(groupid):
    cursor = conn.cursor()
    sql="select count(*) from FileServers where FileServer_Group_ID ='"+str(groupid) +"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    count=0
    for row in cursor.fetchall():
        count=row[0]
    cursor.close()
    return count
        
    

def sp_lookupktvservers(**kwargs):
    id = kwargs['id']
    ipaddress = kwargs['ipaddress']
    cursor = conn.cursor()
    if id!='' and int(id) > 0:
        sql = "select FileServer_IpAddress from FileServers where FileServer_ID ='" + str(id) + "' and FileServer_IsMainGroup = 1"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            ipaddress = row[0]
    else:
        sql = "select FileServer_ID from FileServers where FileServer_IpAddress ='" + ipaddress + "' and FileServer_IsMainGroup = 1"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            id = row[0]
    if id=='':
        sql = "select FileServer_IpAddress from fileservers"
    else:
        sql = "select FileServer_IpAddress from fileservers where FileServer_ID = '" + str(id) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        print(row)

    cursor.close()

def set_mian_group(group_id):

    cursor = conn.cursor()
    sql="update fileservers set FileServer_IsMainGroup= 0 where FileServer_IsValid=1"
    n = cursor.execute(sql)
    sql="update fileservers set FileServer_IsMainGroup='1' where FileServer_Group_ID="+str(group_id)
    n = cursor.execute(sql)
    # sql = "update systemsettinginfo set SettingInfo_Value = dateadd(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    # cursor.execute(sql)
    cursor.close()

    return 0



def sp_lookupfileservers(**kwargs):
    id  = kwargs['id']
    ipaddress = kwargs['ipaddress']
    group_id = kwargs['group_id']
    group_name = kwargs['group_name']
    cursor = conn.cursor()
    if id!='' and int(id) > 0:
        sql = "select FileServer_IpAddress from FileServers where FileServer_ID = '" + str(id) + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            ipaddress = row[0]
    else:
        sql = "select FileServer_ID from FileServers where FileServer_IpAddress = '" + ipaddress + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            id = row[0]
    if group_id!='' and int(group_id) > 0:
        sql = "select ServerGroup_Name into  @group_name from ServerGroups where ServerGroup_ID = '" + group_id + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            group_name = row[0]
    else:
        sql = "select ServerGroup_ID from ServerGroups where ServerGroup_Name = '" + group_name + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            group_id = row[0]
    if id=='' or group_id=='':
        sql = "select * from FileServers"
    elif id=='':
        sql = "select * from FileServers where FileServer_Group_ID = '" + str(group_id) + "'"
    else:
        sql = "select * from FileServers where FileServer_ID = '" + str(id) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        print(row)

    cursor.close()

#一定需要回滚的操作
def sp_roomktvservermapping():
    try:
        cursor = conn.cursor()
        sql = "delete from RoomKTVServers";
        n = cursor.execute(sql)
        sql = "CREATE TEMPORARY table IF NOT EXISTS v2_temp(Room_ID int, KtvServer_ID int, KtvServer_Priority int)"
        cursor.execute(sql)
    
        sql = "delete from v2_temp"
        cursor.execute(sql)
    
        sql = "insert into v2_temp select room_id,fileserver_id,0 from rooms, fileservers order by room_id"
        cursor.execute(sql)
    
        icount = 0
        sql = "select count(*) FROM fileservers"
        cursor.execute(sql)
        for row in cursor.fetchall():
            icount = row[0]
        roomids=[]
        sql = "select Room_ID from rooms order by Room_ID";
        cursor.execute(sql)
        for row in cursor.fetchall():
            roomids.append(row[0])
    
        #print(roomids)
        #print(icount)
        i = 1
        roomid = 0
        while i<=icount:
    
            for roomid in roomids:
                ktvids="-1"
                sql = "select ktvserver_id from v2_temp where Room_ID = " + str(roomid) +" and KTVSERVER_PRIORITY > 0"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ktvids += ","
                    ktvids += str(row[0]);
    
                sql = "select ktvserver_id from v2_temp where KTVSERVER_PRIORITY = 0 and ktvserver_id not in ("
                sql+= ktvids
                sql+=")"
                sql+= "group by ktvserver_id order by count(*) desc limit 0,1"
                cursor.execute(sql)
                ktv_server_id = 1
                for item in cursor.fetchall():
                    ktv_server_id = item[0]
    
                sql = "UPDATE v2_temp SET KTVSERVER_PRIORITY = " + str(i) +" WHERE Room_ID = " + str(roomid) + " AND KtvServer_ID = " + str(ktv_server_id)
                cursor.execute(sql)
            i = i + 1
    
        sql = "insert into RoomKTVServers select * from v2_temp"
        cursor.execute(sql)
        sql = "delete from v2_temp"
        cursor.execute(sql)
        cursor.close()
        #必须添加回滚
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.rollback()
        print("traceback.format_exc()",traceback.format_exc()) 
#         

def sp_addroom(kwargs):
    room_id=kwargs['room_id']
    room_serialno = kwargs['room_serialno']
    room_name = kwargs['room_name']
    room_ipaddress = kwargs['room_ipaddress']
    room_description = kwargs['room_description']
    room_class = kwargs['room_class']
    room_class_name = kwargs['room_class_name']
    manufactory_id = kwargs['manufactory_id']
    manufactory_name = kwargs['manufactory_name']
    discount = kwargs['discount']
    mediaordertype = kwargs['mediaordertype']
    room_PriceGroup_Name = kwargs['room_PriceGroup_Name']
    IsOrNo_SaveBill = kwargs['IsOrNo_SaveBill']
    FullNum = kwargs['FullNum']
    strFloor = kwargs['strFloor']
    Room_MAC1 = kwargs['Room_MAC1']
    Room_STBtype = kwargs['Room_STBtype']

    if room_serialno=='':
        return -1

    if room_name=='':
        room_name = room_serialno
    if room_description=='':
        room_description = 'UNKNOWN'

    cursor = conn.cursor()

    Room_Cost_Food=0
    sql = "select Cost_Food_LowerPrice from COSTS where Cost_ID = " + str(room_class)
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    for row in cursor.fetchall():
        Room_Cost_Food = row[0]

    tmpcnt = 0
    room_class_name=''
    cost_id = 0
    if int(room_class)>0:
        #sql = "select @room_class_name = RoomClass_Name, @cost_id = RoomClass_Cost_ID from RoomClasses where RoomClass_ID = @room_class
        sql = "select RoomClass_Name, RoomClass_Cost_ID from RoomClasses where RoomClass_ID = " + str(room_class)
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_class_name = row[0]
            cost_id = row[1]
            tmpcnt = 1

    if tmpcnt == 0 and room_class_name!='':
        #select @tmpcnt = @tmpcnt + 1, @room_class = RoomClass_ID, @cost_id = RoomClass_Cost_ID from RoomClasses where RoomClass_Name = @room_class_name
        sql = "select RoomClass_ID, RoomClass_Cost_ID from RoomClasses where RoomClass_Name = " + room_class_name
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_class = row[0]
            cost_id = row[1]
            tmpcnt = 1

    room_PriceGroup_ID = 0
    sql = "select PriceGroup_ID from PriceGroup where PriceGroup_Name='" + room_PriceGroup_Name + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        room_PriceGroup_ID = row[0]

    iBranchID=0
    strBranchName=''
    sql = "select RoomBranch_ID, RoomBranch_Name from Manufactories m, RoomClasses r, RoomBranches rb "
    sql+= "where r.RoomClass_Branch_ID = rb.RoomBranch_ID and rb.RoomBranch_Manufactory_ID = m.Manufactory_ID and "
    sql+= "r.RoomClass_ID = " + str(room_class) +" and r.RoomClass_Name ='" + room_class_name + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        iBranchID = row[0]
        strBranchName = row[1]

    tmpcnt = 0
    if int(manufactory_id) > 0:
        sql = "select Manufactory_Name from Manufactories where Manufactory_ID = " + str(manufactory_id)
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            manufactory_name = row[0]
            tmcnt = 1
    if tmcnt==0 and manufactory_name!='':
        sql = "select Manufactory_ID from Manufactories where Manufactory_Name = '" + manufactory_name + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            manufactory_id = row[0]
            tmcnt = 1

    if tmpcnt == 0:
        sql = "select m.Manufactory_ID, m.Manufactory_Name from Manufactories m, RoomClasses r, RoomBranches rb "
        sql+= "where r.RoomClass_Branch_ID = rb.RoomBranch_ID and rb.RoomBranch_Manufactory_ID = m.Manufactory_ID and "
        sql+= "r.RoomClass_ID = " + str(room_class) + " and r.RoomClass_Name = '" + room_class_name + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            manufactory_id = row[0]
            manufactory_name = row[1]

    tmpcnt = 0
    sql = "select Room_SerialNo from Rooms where Room_SerialNo = '" + str(room_serialno) + "' or Room_IpAddress = '" + str(room_ipaddress) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        tmpcnt = 1
    if tmpcnt==1:
        return -5

    if discount=='' or int(discount)<0 or int(discount)>1:
        discount = 1


    if mediaordertype=='' or int(mediaordertype)<0 or int(mediaordertype)>1:
        sql = "select Configure_Set17 from Configures where Configure_ID = 1"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            mediaordertype = row[0]

    room_id = sp_createuniqueid(table='Rooms', columname='Room')
    if room_id==0:
        room_id=1


    room_class = 1

    sql = "insert into Rooms(Room_ID, Room_SerialNo, Room_Name, Room_Class_ID, Room_IpAddress, Room_Description, Room_Manufactory_ID, Room_IsDiscount, Room_OrderType, Room_Cost_ID,Room_PriceGroup_ID,Room_SaveBill_IsOrNo,Room_FullNum,Room_Floor,"
    sql+= "Room_Class_Name, Room_Manufactory_Name, Room_PriceGroup_Name, Room_Branch_ID, Room_Branch_Name,Room_Cost_Food_LowerPrice,Room_PriceGroup_ID_Old,Room_PriceGroup_Name_Old,Room_MAC1,Room_STBtype) "
    sql+= "values ('" + str(room_id) + "','" + str(room_serialno) + "','" + room_name + "','" + str(room_class) + "','" + str(room_ipaddress) + "',"
    sql+= "'" + room_description + "','" + str(manufactory_id) + "','" + str(discount) + "','" + str(mediaordertype) + "','" + str(cost_id) + "',"
    sql+= "'" + str(room_PriceGroup_ID) + "','" + str(IsOrNo_SaveBill) + "','" + str(FullNum) + "','" + str(strFloor) + "',"
    sql+= "'" + room_class_name + "','" + manufactory_name + "','" + room_PriceGroup_Name + "','" + str(iBranchID) + "',"
    sql+= "'" + strBranchName + "','" + str(Room_Cost_Food) + "','" + str(room_PriceGroup_ID) + "','" + room_PriceGroup_Name + "',"
    sql+= "'"+ str(Room_MAC1) + "','" + str(Room_STBtype) + "')"
    n = cursor.execute(sql)
    conn.commit()

    cursor.close()
    return room_id

def sp_modifyroom(kwargs):
    room_id = kwargs['room_id']
    room_serialno = kwargs['room_serialno']
    room_ipaddress = kwargs['room_ipaddress']
    room_newserialno = kwargs['room_newserialno']
    room_newipaddress = kwargs['room_newipaddress']
    room_name = kwargs['room_name']
    room_description = kwargs['room_description']
    room_class_id = kwargs['room_class']
    room_class_name = kwargs['room_class_name']
    manufactory_id = kwargs['manufactory_id']
    manufactory_name = kwargs['manufactory_name']
    discount = kwargs['discount']
    mediaordertype = kwargs['mediaordertype']
    room_PriceGroup_Name = kwargs['room_PriceGroup_Name']
    RoomClassBranchName = kwargs['RoomClassBranchName']
    IsOrNo_SaveBill = kwargs['IsOrNo_SaveBill']
    FullNum = kwargs['FullNum']
    strFloor = kwargs['strFloor']
    Room_MAC1 = kwargs['Room_MAC1']
    Room_STBtype = kwargs['Room_STBtype']

    cursor = conn.cursor()
    tmpcnt = 0
    if room_class_id!='' and int(room_class_id) > 0:
        sql = "select RoomClass_Name from RoomClasses where RoomClass_ID = " + str(room_class_id)
        try:
            n = cursor.execute(sql)
        except:
            restartdb()
           
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_class_name = row[0]
            tmpcnt = 1
    if tmpcnt == 0 and room_class_name!='':
        sql = "select RoomClass_ID from RoomClasses a, RoomBranches b where a.RoomClass_Name = '" + room_class_name + "' "
        sql+= "and a.roomclass_cost_id=b.roombranch_id and b.roombranch_Name = '" + RoomClassBranchName + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_class_id = row[0]
            tmpcnt = 1

    tmpcnt = 0
    if tmpcnt == 0 and int(room_id) > 0:
        sql = "select Room_SerialNo, Room_IpAddress from Rooms where Room_ID = " + str(room_id)
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_serialno = row[0]
            room_ipaddress = row[1]
            tmpcnt = 1
    if tmpcnt == 0 and room_serialno!='':
        sql = "select Room_ID, Room_IpAddress from Rooms where Room_SerialNo = '" + str(room_serialno) + "'"
        try:
            n = cursor.execute(sql)
        except :
            restartdb()
            cursor = conn.cursor()
            n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_id = row[0]
            room_ipaddress = row[1]
            tmpcnt = 1
    if tmpcnt == 0 and room_ipaddress!='':
        sql = "select Room_ID, Room_SerialNo from Rooms where Room_IpAddress = '" + room_ipaddress + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            room_id = row[0]
            room_serialno = row[1]
            tmpcnt = 1
    if tmpcnt == 0:
        cursor.close()
        return 1

    tmpcnt = 0
    try:
        sql = "select BusinessLog_Room_ID from BusinessLogsOld where BusinessLog_Room_ID = " + str(room_id) + " and "
        sql+= "BusinessLog_Room_SerialNo = '" + str(room_serialno) + "' and BusinessLog_Room_IpAddress = '" + room_ipaddress + "' and "
        sql+= "BusinessLog_IsValid <> 1 and BusinessLog_IsValid <> 4"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            tmpcnt = 1
        if tmpcnt == 1:
            cursor.close()
            return 100
    except:
        tmpcnt=0
    tmpcnt = 0

    if tmpcnt == 0 and int(manufactory_id) > 0:
        sql = "select Manufactory_Name from Manufactories where Manufactory_ID = " + str(manufactory_id)
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            manufactory_name = row[0]
            tmpcnt = 1
    if tmpcnt == 0 and manufactory_name!='':
        sql = "select Manufactory_ID from Manufactories where Manufactory_Name = '" + manufactory_name + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            manufactory_id = row[0]
            tmpcnt = 1

    if tmpcnt == 0:
        sql = "select m.Manufactory_ID, m.Manufactory_Name "
        sql+= "from Manufactories m, RoomClasses r, RoomBranches rb "
        sql+= "where r.RoomClass_Branch_ID = rb.RoomBranch_ID and rb.RoomBranch_Manufactory_ID = m.Manufactory_ID and "
        sql+= "r.RoomClass_ID = " + str(room_class_id) + " and r.RoomClass_Name = '" + room_class_name + "'"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            manufactory_id = row[0]
            manufactory_name = row[1]

    if room_newipaddress=='':
        cursor.close()
        return 101
    tmpcnt = 0
    sql = "select Room_SerialNo from Rooms where (Room_SerialNo = '" + str(room_newserialno) + "' or Room_IpAddress = '" + str(room_newipaddress) + "') and "
    sql+= "Room_ID <> " + str(room_id) + " and Room_SerialNo <> '" + str(room_serialno) + "' and Room_IpAddress <> '" + str(room_ipaddress) + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        tmpcnt = 1

    if tmpcnt == 1:
        cursor.close()
        return 102

    if room_name=='':
        room_name = room_newserialno
    if discount=='' or int(discount)<0 or int(discount)>1:
        discount = 1
    if mediaordertype=='' or int(mediaordertype)<0 or int(mediaordertype)>1:
        sql = "select Configure_Set17 from Configures where Configure_ID = 1"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            mediaordertype = row[0]

    room_PriceGroup_ID=0
    sql = "select PriceGroup_ID from PriceGroup where PriceGroup_Name='" + room_PriceGroup_Name + "'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        room_PriceGroup_ID = row[0]
    
    
    sql = "update Rooms set "
    if room_newserialno!='':
        sql += "Room_SerialNo = '" + str(room_newserialno) + "',"
    if room_newipaddress!='':
        sql += "Room_IpAddress = '" + str(room_newipaddress) + "',"
    if room_class_id!='':
        sql += "Room_Class_ID = " + str(room_class_id) + ","
    if room_name!='':
        sql += "Room_Name ='" + str(room_name) +"',"
    if room_description!='':
        sql += "Room_Description = '" + room_description + "',"
    if manufactory_id!='':
        sql += "Room_Manufactory_ID = " + str(manufactory_id) + ","
    if discount!='':
        sql += "Room_IsDiscount = " + str(discount) + ","
    if mediaordertype!='':
        sql += "Room_OrderType = " + str(mediaordertype) + ","
    if room_PriceGroup_ID!='':
        sql += "Room_PriceGroup_ID=" + str(room_PriceGroup_ID) + ","
    sql += "Room_SaveBill_IsOrNo='" + str(IsOrNo_SaveBill) + "',"
    sql+= "Room_FullNum='" + str(FullNum) +"', Room_Floor='" + str(strFloor) + "',"
    sql+= "Room_Class_Name = '" + room_class_name + "',Room_Manufactory_Name = '" + manufactory_name + "',"
    sql+= "Room_PriceGroup_Name = '" + room_PriceGroup_Name + "',"
    if room_PriceGroup_ID!='':
        sql += "Room_PriceGroup_ID_Old='" + str(room_PriceGroup_ID) + "',"
    sql += "Room_PriceGroup_Name_Old = '" + room_PriceGroup_Name + "',"
    sql += "Room_MAC1 = '" + str(Room_MAC1) + "',Room_STBtype = '" + str(Room_STBtype) + "' "
    sql += "where Room_ID = '" + str(room_id) + "' and Room_SerialNo = '" + str(room_serialno) + "' and Room_IpAddress = '" + str(room_ipaddress) + "'"
    try:
        n = cursor.execute(sql)
        cursor.close()
        conn.commit()
    except:
        cursor.close()
        conn.rollback()
    return 0









def sp_delete_room(kwargs):
    room_id=kwargs['room_id']
    room_serialno=kwargs['room_serialno']
    room_ipaddress=kwargs['room_ipaddress']

    tmpcnt=0
    cursor = conn.cursor()

    sql="select Room_ID from Rooms where Room_SerialNo="+str(room_serialno)
    print 'sql',sql
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    for row in cursor.fetchall():
        room_id=str(row[0])
    if not  room_id:
        return 0
    sql="select Room_SerialNo ,Room_IpAddress from Rooms where Room_ID="+str(room_id)
    print 'xxxx',sql
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        print str(tmpcnt)
        tmpcnt=tmpcnt+1
        room_serialno=row[0]
        room_ipaddress=row[1]

    if tmpcnt>0:
        try:
            sql="delete from MediasMenu where MediaMenu_Room_ID ="+str(room_id)
            n = cursor.execute(sql)
            sql="delete from RoomKTVServers where Room_ID = "+str(room_id)
            n = cursor.execute(sql)
            sql="delete from skin where skin_room_id ="+str(room_id)
            n = cursor.execute(sql)
            sql="delete from Rooms where Room_ID ="+str(room_id) +" and Room_SerialNo="+str(room_serialno)
            print sql
            n = cursor.execute(sql)
            cursor.close()
            conn.commit()
        except Exception as e:
            cursor.close()
            conn.rollback()
            print("traceback.format_exc()",traceback.format_exc()) 
    return 0

def sp_add_theme(kwargs):
    theme_name=kwargs['theme_name']
    theme_charset=kwargs['theme_charset']
    font_facename=kwargs['font_facename']
    font_weight=kwargs['font_weight']
    pic_local_path=kwargs['pic_local_path']
    pic_http_path=kwargs['pic_http_path']
    font_local_name=kwargs['font_local_name']
    font_http_name=kwargs['font_http_name']
    font_color1=kwargs['font_color1']
    font_color2=kwargs['font_color2']
    font_color3=kwargs['font_color3']
    font_color4=kwargs['font_color3']
    font_color5=kwargs['font_color3']
    font_color6=kwargs['font_color6']
    font_color7=kwargs['font_color7']
    font_color8=kwargs['font_color8']

    theme_reserved1=kwargs['theme_reserved1']
    theme_reserved2=kwargs['theme_reserved2']
    theme_reserved3=kwargs['theme_reserved3']
    theme_reserved4=kwargs['theme_reserved4']
    theme_reserved5=kwargs['theme_reserved5']
    theme_reserved6=kwargs['theme_reserved6']

    theme_id = sp_createuniqueid (table='Theme', columname='Theme')
    cursor = conn.cursor()
    sql="insert into theme(theme_id, theme_name, theme_charset, font_facename, font_weight, pic_local_path, pic_http_path, font_local_name, font_http_name, font_color1, font_color2, font_color3, font_color4, font_color5, font_color6, font_color7, font_color8, theme_reserved1, theme_reserved2, theme_reserved3, theme_reserved4, theme_reserved5, theme_reserved6) "
    sql+="values ('"+str(theme_id)+"','"+str(theme_name)+"','"+str(theme_charset)+"','"+str(font_facename)+"','"+str(font_weight)
    sql+="','"+str(pic_local_path)+"','"+str(pic_http_path)+"','"+str(font_local_name)+"','"+str(font_http_name)+"','"+str(font_color1)+"','"+str(font_color2)
    sql+="','"+str(font_color3)+"','"+str(font_color4)+"','"+str(font_color5)+"','"+str(font_color6)+"','"+str(font_color7)
    sql+="','"+str(font_color8)+"','"+str(theme_reserved1)+"','"+str(theme_reserved2)+"','"+str(theme_reserved3)+"','"+str(theme_reserved4)
    sql+="','"+str(theme_reserved5)+"','"+str(theme_reserved6)+ "')"
    print sql
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)

    sql = "update systemsettinginfo set SettingInfo_Value = date_add(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    print('5: '+ sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return 0

def sp_find_theme_by_name(themename):
    cursor = conn.cursor()
    sql="select * from theme where theme_name='"+str(themename)+"'"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        return 0
    cursor.close()
    return 1
    

def sp_modify_theme(kwargs):
    theme_id=kwargs['theme_id']
    theme_name=kwargs['theme_name']
    theme_charset=kwargs['theme_charset']
    font_facename=kwargs['font_facename']
    font_weight=kwargs['font_weight']
    pic_local_path=kwargs['pic_local_path']
    pic_http_path=kwargs['pic_http_path']
    font_local_name=kwargs['font_local_name']
    font_http_name=kwargs['font_http_name']
    font_color1=kwargs['font_color1']
    font_color2=kwargs['font_color2']
    font_color3=kwargs['font_color3']
    font_color4=kwargs['font_color3']
    font_color5=kwargs['font_color3']
    font_color6=kwargs['font_color6']
    font_color7=kwargs['font_color7']
    font_color8=kwargs['font_color8']

    theme_reserved1=kwargs['theme_reserved1']
    theme_reserved2=kwargs['theme_reserved2']
    theme_reserved3=kwargs['theme_reserved3']
    theme_reserved4=kwargs['theme_reserved4']
    theme_reserved5=kwargs['theme_reserved5']
    theme_reserved6=kwargs['theme_reserved6']

    cursor = conn.cursor()
    sql="update theme set theme_charset ='"+str(theme_charset)+"',font_facename ='"+str(font_facename)+"',font_weight='"+str(font_weight)+"',pic_local_path='"+str(pic_local_path)
    sql+="',pic_http_path='"+str(pic_http_path)+"',font_local_name='"+str(font_local_name)+"',font_http_name='"+str(font_http_name)+"',font_color1='"+str(font_color1)
    sql+="',font_color2='"+str(font_color2)+"',font_color3='"+str(font_color3)+"',font_color4='"+str(font_color4)+"',font_color5='"+str(font_color5)
    sql+="',font_color6='"+str(font_color6)+"',font_color7='"+str(font_color7)+"',font_color8='"+str(font_color8)+"',theme_reserved1='"+str(theme_reserved1)
    sql+="',theme_reserved2='"+str(theme_reserved2)+"',theme_reserved3='"+str(theme_reserved3)+"',theme_reserved4='"+str(theme_reserved4)+"',theme_reserved5='"+str(theme_reserved5)
    sql+="',theme_reserved6='"+str(theme_reserved6)
    sql+="' where theme_name = '"+str(theme_name) +"' and theme_id ="+str(theme_id)
    print sql
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)

    sql = "update systemsettinginfo set SettingInfo_Value = date_add(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"

    cursor.execute(sql);
    conn.commit()
    cursor.close()
    return 0

def sp_delete_theme(kwargs):

    cursor = conn.cursor()
    theme_id=kwargs['theme_id']
    theme_name=kwargs['theme_name']
    sql="delete from theme where theme_name ='"+str(theme_name) +"' and theme_id='"+str(theme_id)+ "'"
    print sql
    try:
        n = cursor.execute(sql)
    except :
        cursor = conn.cursor()
        restartdb()
        n = cursor.execute(sql)
    sql = "update systemsettinginfo set SettingInfo_Value = date_add(now(), interval -1 DAY) where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"

    cursor.execute(sql);
    conn.commit()
    cursor.close()
    return 0

def get_all_fileservers(isMain):
    ret = None
    res = _mysql.fileservers.get_by_all(isMain)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
    return ret

def sp_AutoMac():
    
    RoomCount = 0
    cursor = conn.cursor()
    sql = "update Rooms set Room_mac1 = 0 , Room_STBtype = ifnull(Room_STBtype, 0)"
    try:
        n = cursor.execute(sql)
    except :
        
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    sql = "select count(*) from Rooms where Room_STBtype = 0"
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        RoomCount = row[0]
    if RoomCount<2:
        cursor.close()
        return
    
    i = 0
    Reg = (100-1) / (RoomCount-1)
    Cost = (100-1) % (RoomCount-1)
    
    while(i<RoomCount):
        roomid = 0
        sql = "select MIN(Room_ID) from Rooms where Room_mac1 = 0 and Room_STBtype = 0"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            roomid = row[0]
        if roomid==0:
            break
        if i==0:
            sql = "update Rooms set Room_mac1 = 1 where Room_id = " + str(roomid)
        elif Cost >= i:# --在余数范围内 值+1
            sql = "update Rooms set Room_mac1 = " + str(i * Reg + 1 + i) + " where Room_id = " + str(roomid)
        else:
            sql = "update Rooms set Room_mac1 = " + str(i * Reg + 1 + Cost) + " where Room_id = " + str(roomid)
        cursor.execute(sql)
        conn.commit()
        i = i + 1
    
    if RoomCount <= 100:
        cursor.close()
        return
    
    Reg = 100 / (RoomCount-100)
    Cost = 100 % (RoomCount-100)
    i = 1
    while (i <= RoomCount-99):
        roomid = 0
        sql = "select MIN(Room_ID) from Rooms where Room_mac1 = 0 and Room_STBtype = 0"
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            roomid = row[0]
        if not roomid:
            break
        if roomid==0:
            break
        if Cost >= i:# --在余数范围内 值+1
            sql = "update Rooms set Room_mac1 = "+ str(i * Reg + 100 + i) + " where Room_id = " + str(roomid)
        else:
            sql = "update Rooms set Room_mac1 = " + str(i * Reg + 100 + Cost) + " where Room_id = " + str(roomid)
        print('xxxxxxxxxxxx',sql)
        cursor.execute(sql)
        
        conn.commit()
 
        i =i + 1

    cursor.close()
    
#0 播放广告，1 播放电影 2 播放歌曲排行榜。 下拉选项
def  sp_modifyadvertisementstatus(**kwargs):
    typeid = kwargs['typeid']
    cursor = conn.cursor()
    if typeid>=3 and typeid<=14:
        sql = "UPDATE configures SET  Configure_Set01 = " + str(typeid) + "where Configure_ID = 1"
        cursor.execute(sql)
        cursor.close()
        return

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
    sql = "update Configures set Configure_Set01 = '" + typeid + "' where Configure_ID = 1"
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

def sp_modifygapbetweenmedias(second):
    cursor = conn.cursor()
    sql = "update Configures set Configure_Set02 = " + str(second) + " where Configure_ID = 1"
    n = cursor.execute(sql)
    sql = "update SystemsettingInfo set SettingInfo_Value = DATE_ADD(now(),INTERVAL -1 DAY)  where SettingInfo_Name = 'MeidasIndexCreateTime' and SettingInfo_Value<>''"
    n = cursor.execute(sql)
    cursor.close()

def sp_findthunder_ini():
    cursor = conn.cursor()
    sql="select value from twm_config where name='config.ini'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    content=''
    for row in cursor.fetchall():
        cursor = conn.cursor()
        tcontent = row[0]
        content=tcontent.replace('******', '\n')
        
    cursor.close()    
    return content
    
def sp_updatathunder_init(content):
    cursor = conn.cursor()
    content = content.replace('\n', '******')
    sql="update twm_config set value='"+(content)+"' where name='config.ini'"
    print sql
    n = cursor.execute(sql)
    conn.commit()
    cursor.close()

def sp_favourable_add(kwargs):
    filename=kwargs['filename']
    path=kwargs['path']
    cursor = conn.cursor()
    sql="select * from YouHuiPictureInfos where YouHuiPictureInfo_FileName='"+str(filename)+"'"
    
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        return -1
    
    sql="insert into YouHuiPictureInfos(YouHuiPictureInfo_FileName,YouHuiPictureInfo_Path) values ('"+str(filename)+"','"+str(path)+"' )"
    n = cursor.execute(sql)
    conn.commit()
    cursor.close()
    return 0
    
def sp_favourable_delect(filename):
    cursor = conn.cursor()
    sql="delete from YouHuiPictureInfos where YouHuiPictureInfo_FileName='"+str(filename)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    conn.commit()
    cursor.close()
    
def sp_add_systhunder(kwargs):
    serverid=sp_createuniqueid(table='thundersyn', columname='server')
    server_ip=(kwargs['server_ip'])
    server_type=(kwargs['server_type'])
    cursor = conn.cursor()
    sql="insert into thundersyn(server_id,server_ip,server_type) values ('"+serverid+"','"+str(server_ip)+"','"+str(server_type)+"')"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    conn.commit()
    cursor.close()
    
def sp_delete_synthunder(ipaddress):
    server_ip=ipaddress
    cursor = conn.cursor()
    sql="delete from thundersyn where server_ip='"+str(ipaddress)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    conn.commit()
    cursor.close()

def sp_updata_synthunder(kwargs):
    server_ip=(kwargs['server_ip'])
    server_type=(kwargs['server_type'])
    cursor = conn.cursor()
    sql="update thundersyn set server_type= '"+str(server_type)+"' where server_ip='"+str(ipaddress)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    conn.commit()
    cursor.close()

def sp_find_synthunder(ipaddress):
    server_ip=ipaddress
    cursor = conn.cursor()
    tjson={}
    sql="SELECT * FROM  thundersyn where server_ip ='"+ str(server_ip)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    for row in cursor.fetchall():
        tjson=row
        cursor.close()
        return  tjson

def find_room_by_ser_no(no):
    cursor = conn.cursor()
    sql="SELECT Room_Id from rooms where Room_SerialNo='"+str(no)+"'"
    try:
        n = cursor.execute(sql)
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
    room_id=None
    for row in cursor.fetchall():
        room_id=row[0]
    return room_id    
def set_room_stbtype_no(no,type):
    cursor = conn.cursor()
    sql="update rooms set Room_STBtype='"+str(type)+"' where Room_SerialNo='"+str(no)+"'"
    try:
        n = cursor.execute(sql)
        conn.commit()
    except :
        restartdb()
        cursor = conn.cursor()
        n = cursor.execute(sql)
        cursor.close()
        conn.commit()
  
    
    
    
    




if __name__=='__main__':
    #addSong(server='192.100.110.1')
    opendb()
    #sp_AddActor(actor_name='张学友XXX',actor_no='0',actor_typename='男',actor_photo='',actor_jianpin='ZXY',actor_pinyin='ZXY')
    #sp_ImportMaterial(serverIp='192.100.110.252', mid='1', no='0', version='1', date='2016-07-28')
    #sp_addmediatype(curid='102', name='XYZ', description='HRU', typeid='1')

    #sp_addmedias(serialno='22233', iname='iname', lname='lname', type1 = 'type1', type2='type2',  \
	#	jianpin= 'jianpin', pinyin= 'pinyin', sname1= 'sname1', sname2= 'sname2', sname3= 'sname3', \
	#	sname4= 'sname4', ltype= '1', volume= '9', stroke= '5', bihua= 'bihua', \
	#	videoformat= 'videoformat', audioformat= 'audioformat', videotype= '1', \
	#	ztrack= '2', ytrack= '3', isnew= '1', groupid= '1', filename= '/nnt/ss/0000.mp4', \
	#	lyric= 'lyric'
    #sp_deletefileserver(rid='270166', ipaddress='192.168.0.1')
    #n = sp_addfileserver(name='abc',ipaddress='10.0.165.58', os='os', isvalid='1', group_id='1', group_name='' )
    #print('sp_addfileserver: ' + str(n))
    #n = spm_getserialno(media_name='media_name', media_actor_name1 = 'media_actor_name1', media_actor_name2 = 'media_actor_name2', \
    #                media_actor_name3 = 'media_actor_name3', media_actor_name4 = 'media_actor_name4', \
    #                media_type_name1 = 'media_type_name1', media_type_name2 = 'media_type_name2', media_type_name3 = 'media_type_name3', \
    #                typeid =  '0', group_id =  '1', fileserver_id =  '', isMenpai =  '0')
    #print("spm_getserialno: ", str(n))
    sp_updatathunder_init('xxxx')
    closedb()
