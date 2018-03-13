#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, NVARCHAR, \
        TIMESTAMP, DATE, DATETIME, CHAR, DOUBLE, FLOAT, TINYINT, BIGINT, DECIMAL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.expression import func

class Model(object):

    #id = Column(INTEGER, primary_key=True)

    @declared_attr
    def __table_args__(cls):
        return {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8'
        }

Base = declarative_base(cls=Model)

class M_MediaDetails(Base):
    __tablename__ = 'mediadetails'

    Media_ID = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    Media_Name = Column(VARCHAR(200), nullable=True)
    Media_SerialNo = Column(VARCHAR(10), nullable=True)
    Nation_Name = Column(VARCHAR(200), nullable=True)
    Language_Name = Column(VARCHAR(200), nullable=True)
    Actor_Name1 = Column(VARCHAR(200), nullable=True)
    Actor_Name2 = Column(VARCHAR(200), nullable=True)
    Actor_Name3 = Column(VARCHAR(200), nullable=True)
    Actor_Name4 = Column(VARCHAR(200), nullable=True)
    Director_Name1 = Column(VARCHAR(200), nullable=True)
    Director_Name2 = Column(VARCHAR(200), nullable=True)
    MediaType_Name1 = Column(VARCHAR(200), nullable=True)
    MediaType_Name2 = Column(VARCHAR(200), nullable=True)
    MediaType_Name3 = Column(VARCHAR(200), nullable=True)
    Carrier_Name = Column(VARCHAR(200), nullable=True)
    Audio_Name = Column(VARCHAR(200), nullable=True)
    MediaManage_OrderCount = Column(INTEGER(11), nullable=True)


class M_MediaType(Base):
    __tablename__ = 'mediatypes'

    MediaType_ID = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    MediaType_Name = Column(VARCHAR(200), nullable=True)
    MediaType_Description = Column(VARCHAR(255), nullable=True)
    MediaType_IsMovie = Column(INTEGER(11), nullable=True)
    MediaType_IsKaraok = Column(INTEGER(11), nullable=True)
    MediaType_IsAds = Column(INTEGER(11), nullable=True)
    MediaType_NewTypeID = Column(INTEGER(11), nullable=True)



class M_ActorType(Base):
    __tablename__ = 'actortypes'

    actortype_id = Column(INTEGER, primary_key=True, index=True, autoincrement=True, doc='主键，自增量')
    actortype_name = Column(VARCHAR(200), nullable=False, doc='歌星类型名称')
    actortype_des = Column(VARCHAR(255), nullable=True, doc='描述说明')
    actortype_ismovie = Column(INTEGER(11), nullable=False, doc='是否影星类型')
    actortype_iskaraok = Column(INTEGER(11), nullable=False, doc='是否歌星类型')


class M_Actors(Base):
    __tablename__ = 'actors'

    actor_no = Column(INTEGER(11), primary_key=True, index=True, nullable=False, doc='歌星编号，雷石给每个个歌星都有一个唯一编号')
    actor_name = Column(VARCHAR(128), nullable=False, doc='歌星名字')
    actor_des = Column(VARCHAR(255), nullable=False, doc='歌星的描述性说明')
    actor_typeid = Column(INTEGER, nullable=False, doc='歌星类型ID')
    actor_type = Column(VARCHAR(64), nullable=False, doc='歌星类型')
    actor_py = Column(VARCHAR(128), nullable=False, doc='歌星名字的全拼')
    actor_jp = Column(VARCHAR(64), nullable=False, doc='歌星名字的拼音首字母')
    actor_click = Column(INTEGER(11), nullable=False, server_default = '0', doc='总点击量')
    actor_clickw = Column(INTEGER(11), nullable=False, server_default = '0', doc='最近一周点击量')
    actor_clickm = Column(INTEGER(11), nullable=False, server_default = '0', doc='最近一个月点击量')

class M_Medias(Base):
    __tablename__ = 'medias'

    media_no = Column(INTEGER, primary_key=True, index=True, doc='歌曲编号')
    media_name = Column(VARCHAR(200), nullable=False, doc='歌曲名称')
    media_namelen = Column(TINYINT, nullable=False, doc='歌曲名称长度')
    media_langtype = Column(TINYINT(4), nullable=True, doc='(歌曲语言类型) 用于显示歌曲信息,字幕时选择字库文件.0: 中文,1韩文,2日文')
    media_langid = Column(INTEGER(11), nullable=True, doc='歌曲语言ID')
    media_lang = Column(VARCHAR(32), nullable=True, doc='歌曲语言')
    media_tag1 = Column(VARCHAR(128), nullable=True, doc='歌曲3D分类')
    media_tag2 = Column(VARCHAR(128), nullable=True, doc='歌曲3D分类')
    media_actname1 = Column(VARCHAR(128), nullable=True, doc='歌星信息（全部）')
    media_actname2 = Column(VARCHAR(128), nullable=True, doc='歌星信息（全部）')
    media_actname3 = Column(VARCHAR(128), nullable=True, doc='歌星信息（全部）')
    media_actname4 = Column(VARCHAR(128), nullable=True, doc='歌星信息（全部）')
    media_carria = Column(VARCHAR(32), nullable=True, doc='歌曲载体类型（DVD，MP3等）')
    media_yuan = Column(TINYINT, nullable=False, server_default='1', doc='原唱')
    media_ban = Column(TINYINT, nullable=False, server_default='2', doc='伴唱')
    media_svrgroup = Column(TINYINT, nullable=False, server_default='1', doc='文件所在服务器组：1-主组，2-从组')
    media_file = Column(VARCHAR(256), nullable=True, doc='文件路径（文件名）')
    media_style = Column(TINYINT, nullable=True, doc='视频风格类型: 0-MV 1-现场版 2-流水影')
    media_audio = Column(VARCHAR(32), nullable=True, doc='音频类型（mpeg）')
    media_volume = Column(TINYINT, nullable=True, doc='音量')
    media_jp = Column(VARCHAR(32), nullable=True, doc='简拼')
    media_py = Column(VARCHAR(256), nullable=True, doc='拼音')
    media_strok = Column(TINYINT, nullable=True, doc='笔画数')
    media_stroks = Column(VARCHAR(64), nullable=True, doc='笔划序列')
    media_lyric = Column(VARCHAR(512), nullable=True, doc='歌词,用于搜吧搜索')
    media_isnew = Column(TINYINT, nullable=True, doc='是否新歌')
    media_clickm = Column(INTEGER, nullable=False, server_default='0', doc='月点击量')
    media_clickw = Column(INTEGER, nullable=False, server_default='0', doc='周点击量')
    media_click = Column(INTEGER, nullable=False, server_default='0', doc='总点击量')
    media_type = Column(TINYINT, nullable=False, doc='类型，1: 歌曲|2: 广告|3: 电影')
    media_stars = Column(TINYINT(4), nullable=False, doc = 'star_level, 歌曲热度设定')
    media_actno1 = Column(INTEGER, nullable=True, doc='歌星1 编号')
    media_actno2 = Column(INTEGER, nullable=True, doc='歌星2 编号')
    media_actno3 = Column(INTEGER, nullable=True, doc='歌星3 编号')
    media_actno4 = Column(INTEGER, nullable=True, doc='歌星4 编号')
    media_dafen = Column(TINYINT, nullable=False, server_default='0', doc='该歌曲是否支持打分')
    media_climax = Column(TINYINT, nullable=False, server_default='0', doc='该歌曲是否有高潮信息')
    media_climaxinfo = Column(VARCHAR(256), nullable=True, doc='该歌曲的高潮信息')
    media_yinyi = Column(TINYINT, nullable=False, server_default='0', doc='该歌曲是否有音译信息')
    media_light = Column(INTEGER, nullable=False, server_default='0', doc='灯光设置')
    media_newadd = Column(TINYINT, nullable=False, server_default='0', doc='用于清除空纪录使用')

class M_MediaManage(Base):
    __tablename__ = 'mediasmanage'

    MediaManage_ID = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    MediaManage_Nation_ID = Column(INTEGER(11), nullable=True)
    MediaManage_Language_ID = Column(INTEGER(11), nullable=True)
    MediaManage_Carrier_ID = Column(INTEGER(11), nullable=True)
    MediaManage_Format_ID = Column(INTEGER(11), nullable=True)
    MediaManage_Audio_ID = Column(INTEGER(11), nullable=True)
    MediaManage_OrderCount = Column(INTEGER(11), nullable=True)
    MediaManage_IsNew = Column(INTEGER(11), nullable=True)
    MediaManage_IsValid = Column(INTEGER(11), nullable=True)
    MediaManage_OriginalTrack = Column(INTEGER(11), nullable=True)
    MediaManage_AccompanyTrack = Column(INTEGER(11), nullable=True)
    MediaManage_RegisterTime = Column(TIMESTAMP, nullable=True, server_default = func.now())

class M_MediaFile(Base):
    __tablename__ = 'mediafiles'

    media_no = Column(INTEGER(11), primary_key=True)
    media_svrgroup  = Column(TINYINT(4), nullable=False)
    media_file = Column(VARCHAR(256), nullable=True)

class M_Langs(Base):
    __tablename__ = 'langs'

    lang_id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    lang_name = Column(VARCHAR(200), nullable=True)
    lang_des = Column(VARCHAR(255), nullable=True)

class M_Audios(Base):
    __tablename__ = 'audios'

    Audio_ID = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    Audio_Name = Column(VARCHAR(200), nullable=True)
    Audio_Description = Column(VARCHAR(255), nullable=True)

class M_Carriers(Base):
    __tablename__ = 'carriers'

    carrier_id = Column(INTEGER(11), primary_key=True,  autoincrement=True)
    carrier_name = Column(VARCHAR(64), nullable=True)
    carrier_desc = Column(VARCHAR(256), nullable=True)

class M_AddMedia(Base):
    __tablename__ = 'addmedia'

    AddMedia_ID = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    AddMedia_Name = Column(VARCHAR(50), nullable=True)
    AddMedia_Path = Column(VARCHAR(200), nullable=True)
    AddMedia_Type = Column(VARCHAR(30), nullable=True)
    AddMedia_Size = Column(INTEGER(11), nullable=True)
    AddMedia_CreateDate = Column(DATETIME, nullable=True)
    AddMedia_UpdateDate = Column(DATETIME, nullable=True)
    AddMedia_State = Column(INTEGER(11), nullable=True)
    AddMedia_SerialNo = Column(VARCHAR(10), nullable=True)

class M_MediaUserSet(Base):
    __tablename__ = 'mediauserset'
    MediaUserSet_Id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    MediaUserSet_MediaId = Column(VARCHAR(20), nullable=True)
    MediaUserSet_Shunxu = Column(INTEGER(11), nullable=True)

class M_AutoPlay(Base):
    __tablename__ = 'autoplay'
    media_no = Column(INTEGER, primary_key=True)
    media_svrgrp  = Column(INTEGER, nullable=True)
    media_file = Column(VARCHAR(256), nullable=True)

class M_FileServers(Base):
    __tablename__ = 'fileservers'
    FileServer_ID = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    FileServer_Name = Column(VARCHAR(200), nullable=True)
    FileServer_IpAddress = Column(VARCHAR(15), nullable=True)
    FileServer_OS = Column(VARCHAR(200), nullable=True)
    FileServer_CreateDate = Column(TIMESTAMP, nullable=True, server_default = func.now())
    FileServer_ModifyDate = Column(TIMESTAMP, nullable=True, server_default = func.now())
    FileServer_ExpireDate = Column(TIMESTAMP, nullable=True, server_default = func.now())
    FileServer_IsValid = Column(INTEGER(11), nullable=True)
    FileServer_Group_ID = Column(INTEGER(11), nullable=True)
    FileServer_IsMainGroup = Column(INTEGER(11), nullable=True)


class M_Servers(Base):
    __tablename__ = 'servers'
    server_id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    server_grpid = Column(TINYINT, nullable=False, server_default='9')
    server_name = Column(VARCHAR(64), nullable=False)
    server_ip = Column(VARCHAR(16), nullable=False)
    server_weight = Column(TINYINT, nullable=False, server_default='9')
    server_addtime = Column(TIMESTAMP, nullable=False, server_default = func.now())

class M_BoxSetting(Base):
    __tablename__='BoxSetting'

    id = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, autoincrement=True,)
    ktvid = Column(INTEGER(unsigned=True),doc='ktv id')
    name = Column(VARCHAR(512), nullable=False, doc='description for name')
    appvalue = Column(VARCHAR(512), nullable=False, doc='appvalue')
    boxtype = Column(INTEGER(unsigned=True),  doc='box type')
    result = Column(VARCHAR(512), nullable=False, doc='result')
    typename = Column(VARCHAR(512), nullable=False, doc='type name')
    optionid=Column(INTEGER(unsigned=True),doc='option id')
    optionname = Column(VARCHAR(512), nullable=False, doc='option name')

class M_Boxsetting(Base):
    __tablename__='Boxsetting'

    id = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, autoincrement=True,)
    ShowName = Column(VARCHAR(512), nullable=False, doc='description for ShowName')
    AppValue = Column(VARCHAR(512), nullable=False, doc='appvalue')
    IsString=Column(INTEGER(unsigned=True),doc='IsString')
    result = Column(INTEGER(unsigned=True), doc='result')
    optionvalue = Column(VARCHAR(512), nullable=False, doc='optionvalue')
    optionname = Column(VARCHAR(512), nullable=False, doc='option name')
    addflag = Column(INTEGER(unsigned=True), doc='addflag')
    flag = Column(INTEGER(unsigned=True), doc='addflag')
class M_Boxip(Base):
    __tablename__='Boxip'

    id = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, autoincrement=True,)
    ipaddress = Column(VARCHAR(512), nullable=False, doc='description for ipaddress')
    subnetmask = Column(VARCHAR(512), nullable=False, doc='description for subnetmask')
    serviceip = Column(VARCHAR(512), nullable=False, doc='description for serviceip')
    devicetype = Column(VARCHAR(512), nullable=False, doc='description for devicetype')
    devicegraphics = Column(VARCHAR(512), nullable=False, doc='description for devicegraphics')
    iprecond = Column(VARCHAR(512), nullable=False, doc='description for iprecond')
    deviceoption = Column(VARCHAR(512), nullable=False, doc='description for deviceoption')
    graphicsoption = Column(VARCHAR(512), nullable=False, doc='description for graphicsoption')
    flag = Column(INTEGER(unsigned=True), doc='flag')

class M_Configs(Base):
    __tablename__='config'

    config_id = Column(INTEGER(unsigned=True),primary_key=True,autoincrement=True,doc='配置项的ID值,留做DBAss兼容')
    config_name = Column(VARCHAR(200), nullable=False, doc='设置项的名称,强烈要求使用英文命名方法,不要使用中文')
    config_value = Column(VARCHAR(255), nullable=False, doc='设置项的值')
    config_desc = Column(VARCHAR(255), nullable=False, doc='说明字段, 也可以把这个字段回显于WEB前端做设置项说明')

class M_SystemSettingInfo(Base):
    __tablename__='systemsettinginfo'

    SettingInfo_ID = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    SettingInfo_Name = Column(VARCHAR(200), nullable=False, doc='description for SettingInfo_Name')
    SettingInfo_Value = Column(VARCHAR(255), nullable=False, doc='description for SettingInfo_Value')


class M_Configures(Base):
    __tablename__='configures'

    Configure_ID = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    Configure_Set01=Column(INTEGER(unsigned=True),doc='Configure_Set01')
    Configure_Set02=Column(INTEGER(unsigned=True),doc='Configure_Set02')
    Configure_Set03=Column(INTEGER(unsigned=True),doc='Configure_Set03')
    Configure_Set04 = Column(VARCHAR(255), nullable=False, doc='description for Configure_Set04')
    Configure_Set05 = Column(VARCHAR(255), nullable=False, doc='description for Configure_Set05')
    Configure_Set06=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set07 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set08=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set09=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set10=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set11=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set12=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set13=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set14=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set15=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set16=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set17=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set18=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set19=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set20=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set21=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set22=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set23=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set24=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set25=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set26=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set27=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set28=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set29=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set30=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set31=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set32=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set33=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set34=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set35=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set36=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set37=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set38=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set39=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set40=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set41=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set42=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set43=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set44=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set45=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set46=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set47=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set48=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set49=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set50=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Set51 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set52 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set53= Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set54 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set55 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set56 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set57 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set58 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set59 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_Set60 = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_BookRemind=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_CloseDelay=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_MemberDiscActOn=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_IsMark=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_IsLeadSong=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_IsSpecialEffect=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_SongValidTime=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_Version = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_IsOnlyRead=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_TimeChangeRange=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_IsBoundRoom=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_RoomDisplayContent=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_MaxPayingTime=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_TestRoom=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_MaxTestTime=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_PresentPrice=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_OrderControl=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_SentTime=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_SentTimeBaseA=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_SentTimeSendA=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_SentTimeBaseB=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_SentTimeSendB=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_FingerBool=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_FingerIPAddress = Column(VARCHAR(200), nullable=False, doc='description for Configure_Set07')
    Configure_AutoPresent=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_PresentIsValidateWorker=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_DishIsValidateWorker=Column(INTEGER(unsigned=True),doc='Configure_Set06')
    Configure_ReturnIsValidateWorker=Column(INTEGER(unsigned=True),doc='Configure_Set06')


class M_Themes_old(Base):
    __tablename__='theme'

    theme_id = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    theme_name = Column(VARCHAR(40), nullable=False, doc='description for theme_name')
    theme_charset = Column(VARCHAR(40), nullable=False, doc='description for theme_charset')
    font_facename = Column(VARCHAR(40), nullable=False, doc='description for font_facename')
    font_weight=Column(INTEGER(unsigned=True),doc='font_weight')
    pic_local_path = Column(VARCHAR(255), nullable=False, doc='description for pic_local_path')
    pic_http_path = Column(VARCHAR(255), nullable=False, doc='description for pic_local_path')
    font_local_name = Column(VARCHAR(100), nullable=False, doc='description for pic_local_path')
    font_http_name = Column(VARCHAR(100), nullable=False, doc='description for pic_local_path')
    font_color1 = Column(VARCHAR(20), nullable=False, doc='description for font_color1')
    font_color2 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    font_color3 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    font_color4 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    font_color5 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    font_color6 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    font_color7 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    font_color8 = Column(VARCHAR(20), nullable=False, doc='description for font_color2')
    theme_reserved1 = Column(VARCHAR(100), nullable=False, doc='description for theme_reserved1')
    theme_reserved2 = Column(VARCHAR(100), nullable=False, doc='description for theme_reserved2')
    theme_reserved3 = Column(VARCHAR(100), nullable=False, doc='description for theme_reserved3')
    theme_reserved4=Column(INTEGER(unsigned=True),doc='theme_reserved4')
    theme_reserved5=Column(INTEGER(unsigned=True),doc='theme_reserved5')
    theme_reserved6=Column(INTEGER(unsigned=True),doc='theme_reserved6')

class M_Skin(Base):
    __tablename__='skin'


    skin_id = Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True,autoincrement=True, )
    skin_room_id=Column(INTEGER(unsigned=True),doc='skin_room_id')
    skin_room_serialno = Column(VARCHAR(40), nullable=False, doc='description for skin_room_serialno')
    skin_theme_id=Column(INTEGER(unsigned=True),doc='skin_theme_id')
    skin_theme_name = Column(VARCHAR(40), nullable=False, doc='description for skin_theme_name')


class M_Rooms(Base):
    __tablename__='rooms'

    room_mac = Column(VARCHAR(32), primary_key=True, doc='房台MAC地址,全小写,主键')
    room_no = Column(VARCHAR(32), nullable=True, doc='房台编号')
    room_name = Column(VARCHAR(200), nullable=True, doc='房台名称')
    room_type = Column(TINYINT, nullable=False, server_default='0', doc='预留字段.房间类型,大小中包等')
    room_ip = Column(VARCHAR(16), nullable=True, doc='房台IP地址')
    room_mask = Column(VARCHAR(16), nullable=False, server_default='255.255.255.0', doc='房台网络子网掩码')
    room_gw = Column(VARCHAR(16), nullable=False, server_default='', doc='房台网关地址')
    room_dns = Column(VARCHAR(32), nullable=False, server_default='', doc='房台DNS地址, 最多可写两个')
    room_stbtype = Column(TINYINT, nullable=False, server_default='1', doc='机顶盒类型,1:主机顶盒,2:门牌机,3:从机顶盒')
    room_svr = Column(VARCHAR(16), nullable=False, server_default='', doc='房台连接到服务器IP地址')
    room_recordsvr = Column(VARCHAR(16), nullable=False, server_default='', doc='录音服务器IP地址')
    room_skin = Column(INTEGER, nullable=False, server_default='0', doc='房台皮肤的ID')
    room_theme = Column(INTEGER, nullable=False, server_default='0', doc='房台模板的ID')
    room_profile = Column(INTEGER, nullable=False, server_default='0', doc='DHCP INI中的其他设置项,放JSON格式数据在此')
    room_state = Column(TINYINT, nullable=False, server_default='0', doc='房台状态,0:关台,1:开台,2...')

class M_ServersGroups(Base):
    __tablename__='servergroups'

    ServerGroup_ID=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, autoincrement=True)
    ServerGroup_Name = Column(VARCHAR(100), nullable=False, doc='description for ServerGroup_Name')
    ServerGroup_IsValid=Column(INTEGER(unsigned=True),doc='ServerGroup_IsValid')

class M_ServerConInfo(Base):
    __tablename__='fileserverconnectioninfo'

    Group_ID=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    FileServer_ID=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    Connection_Count=Column(INTEGER(unsigned=True),doc='Connection_Count')
    FileServer_IpAddress1 = Column(VARCHAR(100), nullable=False, doc='description for ServerGroup_Name')
    TotalConnection_Count=Column(INTEGER(unsigned=True),doc='TotalConnection_Count')

class M_KaraokVersions(Base):
    __tablename__='karaokversions'
    KaraokVersion_ID=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    KaraokVersion_ver = Column(VARCHAR(255), nullable=False,)

class M_MenPaiAdSettings(Base):
    __tablename__='menpaiadsettings'
    MenPaiAdSetting_Id=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, autoincrement=True,)
    MenPaiAdSetting_SerialNo = Column(VARCHAR(100), nullable=False, doc='')
    MenPaiAdSetting_PlayCount=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    MenPaiType_ID=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )
    MenPaiAdSettings_RoomID=Column(INTEGER(unsigned=True),primary_key=True,doc=' id',index=True, )


class M_CloudDownLog(Base):
    __tablename__ = 'cloud_downlog'
    down_id = Column(INTEGER(unsigned=True), primary_key=True, doc=' id',index=True, )
    down_gid = Column(VARCHAR(32), nullable=False, doc='task gid in aria2')
    music_no = Column(VARCHAR(16), nullable=False, doc='music number with file suffix')
    music_caption = Column(VARCHAR(256),doc='music name')
    music_singer = Column(VARCHAR(256), doc='singers')
    music_lang = Column(VARCHAR(16), doc='语言')
    music_theme = Column(VARCHAR(16), doc='分类')
    music_ver = Column(VARCHAR(16), doc='版本号')
    music_verdate = Column(DATETIME, doc='版本最后更新时间')
    down_path = Column(VARCHAR(256), doc='下载路径')
    down_url = Column(VARCHAR(256), doc='下载URL')
    down_stime = Column(DATETIME, doc='开始下载时间')
    down_etime = Column(DATETIME, doc='完成下载时间')
    down_status = Column(TINYINT, doc='下载完成状态:0-正在下载，1-下载完成，2-已暂停，3-下载失败')
    down_type = Column(TINYINT, doc='下载类型：0-实时；1-云端强推；2-手动下载')
    music_addtime = Column(DATETIME, doc='成功加歌时间')
    music_hot = Column(VARCHAR(50), doc='歌曲热度')
    music_replace = Column(TINYINT, doc='歌曲热度')
    music_type = Column(INTEGER, doc='歌曲类型')
    file_md5 = Column(VARCHAR(64), doc='歌曲文件MD5值')
    file_type = Column(VARCHAR(16), doc='歌曲文件类型')
    file_size = Column(BIGINT, doc='下载文件大小')
    movie_type = Column(TINYINT, doc='电影类型： 0-片花；1-正片')


class M_CloudMusicInfo(Base):
    __tablename__ = 'cloud_musicinfo'
    music_no = Column(INTEGER, primary_key=True, doc='歌曲编号')
    music_name = Column(VARCHAR(128), nullable=False, doc='歌曲名称')
    music_singer = Column(VARCHAR(256), doc='歌星')
    music_3d1 = Column(VARCHAR(20), doc='3D分类1')
    music_3d2 = Column(VARCHAR(20), doc='3D分类2')
    music_downloadcount = Column(INTEGER, doc='歌曲线上下载次数')
    music_ishd = Column(TINYINT, doc='是否高清')
    music_isnew = Column(TINYINT, doc='是否新歌')
    music_isoften = Column(TINYINT, doc='是否常唱')
    music_isreplace = Column(TINYINT, doc='是否替换')
    music_state = Column(TINYINT, doc='是否使用')
    music_lastver = Column(VARCHAR(20), doc='版本号')
    music_lang = Column(VARCHAR(20), doc='语言')
    music_type1 = Column(VARCHAR(20), doc='分类1')
    music_type2 = Column(VARCHAR(20), doc='分类2')
    music_status = Column(INTEGER, doc='歌曲状态 0：未下载 1：替换 2：已下载 3：待添加')
    music_lastverdate = Column(DATETIME, doc='版本最后更新时间')
    music_unixtime = Column(BIGINT, doc='更新时间')

class M_Skins(Base):
    __tablename__ = 'skins'
    skin_id = Column(INTEGER, primary_key=True, autoincrement=True, doc='歌曲编号')
    skin_name = Column(VARCHAR(128), nullable=False, doc='皮肤包名称')
    #skin_ver = Column(VARCHAR(32), nullable=False, doc='版本号')
    skin_desc = Column(VARCHAR(256), nullable=True, doc='皮肤包说明')
    skin_file = Column(VARCHAR(256), nullable=False, doc='皮肤包文件(下载到本地的路径)')
    skin_unpath = Column(VARCHAR(256), nullable=False, doc='解压后在服务器上的路径(机顶盒用的路径,Android版不需要了)')
    skin_time = Column(TIMESTAMP, nullable=True, server_default=func.now(), doc='添加时间')

class M_Themes(Base):
    __tablename__ = 'themes'
    theme_id = Column(INTEGER, primary_key=True, autoincrement=True, doc='模板编号')
    theme_name = Column(VARCHAR(128), nullable=False, doc='模板名称')
    #theme_ver = Column(VARCHAR(32), nullable=False, doc='')
    theme_desc = Column(VARCHAR(256), nullable=True, doc='模板描述')
    theme_path = Column(VARCHAR(256), nullable=False, doc='模板包文件(下载到本地的路径)')
    theme_unpath = Column(VARCHAR(256), nullable=False, doc='解压后在服务器上的路径')
    theme_type = Column(TINYINT, nullable=False, server_default='0', doc='模板类型 0：自由主题  1、特定主题 ')
    theme_date = Column(TIMESTAMP, nullable=True, server_default=func.now(), doc='添加时间')
    theme_author = Column(VARCHAR(32), nullable=False, doc='设计者')
    theme_state = Column(TINYINT, nullable=False, server_default='0', doc='模板状态')
    theme_bagtype = Column(TINYINT, nullable=False, server_default='0', doc='模板包类型 1：横版 2 竖版')

class M_KtvModuleVer(Base):
    __tablename__ = 'ktvmodule_ver'
    id = Column(INTEGER, primary_key=True, autoincrement=True, doc='模板编号')
    name = Column(VARCHAR(256), nullable=False, doc='模板名称')
    addtime = Column(TIMESTAMP, nullable=True, server_default=func.now(), doc='添加时间')
    fileurl = Column(VARCHAR(256), nullable=False, doc='模板包文件路径(或下载到本地的路径)')
    unpath = Column(VARCHAR(256), nullable=False, doc='解压后在服务器上的路径')
    version = Column(VARCHAR(32), nullable=False, doc='版本号')
    isuse = Column(INTEGER, nullable=False, server_default='0', doc='正在使用，1是，0否')
    needun = Column(INTEGER,  doc='状态 0：需要解压 1：解压成功 2：导入完成')
    desc = Column(VARCHAR(256), nullable=True, doc='模板描述')
    msgtime = Column(INTEGER, nullable=False, server_default='0', doc='提示间隔时间(分钟)')
    isshow = Column(INTEGER, nullable=False, server_default='0', doc='是否强制提示')
    bagtype = Column(TINYINT, nullable=False, server_default='1', doc='模板包类型 1：横版 2 竖版')
    isdefault = Column(INTEGER, nullable=False, server_default='0', doc='是否默认模板')
    revision = Column(DECIMAL(20, 0), nullable=False, doc='')
    vertype = Column(INTEGER, doc='版本类型 1、全部刷新 0、部分刷新')
    
