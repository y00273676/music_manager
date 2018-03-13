#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import commands
import threading
import logging
import traceback
import ConfigParser
import codecs
import chardet
import sys
import MySQLdb
from MySQLdb import cursors



MYSQL = {
    'host': 'localhost',
    'user': '',
    'pass': '',
    'port': 3306,
    'db': 'karaok'
}

class IniConfig(ConfigParser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s=%s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = "=".join((key, str(value).replace('\n', '\n\t')))
                fp.write("%s\n" % (key))
            fp.write("\n")

def read_path_ini():
    mydata={}
    cf = ConfigParser.ConfigParser()
    cf.read('/opt/thunder/twm/path.ini')
    str_a = cf.get("sec_a", "systemparh")
    mydata['systemparh']=str_a
    str_b = cf.get("sec_a", "odbcpath")
    mydata['odbcpath']=str_b
    str_c = cf.get("sec_a", "odbcinstpath")
    mydata['odbcinstpath']=str_c
    return mydata

def get_all_thunder_ini():
    
    f = open(read_path_ini()['systemparh'],"r")
    data = f.read()
    chardet.detect(data)
    return read_all_setting(read_path_ini()['systemparh'],'utf8')

def read_all_setting(filename,strcode):
    datajson={}
    cf = IniConfig()
    # cf.read(filename)
    cf.readfp(codecs.open(filename, "r", strcode))
    sections = cf.sections()
    mainserver=cf.items("MainServer")
    erpserver=cf.items("ErpServer")
    misc=cf.items("Misc")
    ktv=cf.items("KTV")
    erp=cf.items("ERP")

    _mjson={}
    _mprjson={}
    _mmijson={}
    _mktvjson={}
    _merpjson={}

    for colum in mainserver:
        _mjson[colum[0]]=colum[1]
    for columone in erpserver:
        _mprjson[columone[0]]=columone[1]

    for columtwo in misc:
        _mmijson[columtwo[0]]=columtwo[1]
    for columtwo in ktv:
        _mktvjson[columtwo[0]]=columtwo[1]
    for columtwo in erp:
        _merpjson[columtwo[0]]=columtwo[1]


    datajson['mainserver']=_mjson
    datajson['erpserver']=_mprjson
    datajson['misc']=_mmijson
    datajson['erp']=_merpjson
    datajson['ktv']=_mktvjson
    
    return datajson

def set_main_server(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    f = open(read_path_ini()['systemparh'],"r")
    data = f.read()
    

    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("MainServer", "DataBaseServerName", item['DataBaseServerName'])
    cf.set("MainServer", "DataBaseServerIp", item['DataBaseServerIp'])
    cf.set("MainServer", "UserName", item['UserName'])
    cf.set("MainServer", "Password", item['Password'])
    
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))
    #
    set_odbc_ini(mypath['odbcpath'],jsondata,strcode)
    set_my_sql(mypath['odbcinstpath'],jsondata,strcode)
    
def set_main_ip_odbc(jsondata):
    mypath=read_path_ini()
    set_odbc_ini(mypath['odbcpath'],jsondata,'utf8')
    set_my_sql(mypath['odbcinstpath'],jsondata,'utf8')
    
    
def set_main_server_first(jsondata,strcode):
    
    try:
        item=jsondata;
        mypath=read_path_ini()
        cf = IniConfig()
    
        cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
        cf.set("MainServer", "DataBaseServerIp", item['DataBaseServerIp'])
        cf.set("MainServer", "UserName", item['UserName'])
        cf.set("MainServer", "Password", item['Password'])
        cf.set("MainServer", "FileServerIP", item['FileServerIP'])
        #获取本机ip的地址
    #     cf.set("MainServer", "FileServerIP", item['FileServerIp'])
        cf.write(codecs.open(mypath['systemparh'], "w", strcode))
        set_odbc_ini(mypath['odbcpath'],jsondata,strcode)
        set_my_sql(mypath['odbcinstpath'],jsondata,strcode)
        return 0
    except:
        return 1
    

def set_erpserver(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("ErpServer", "DataBaseServerName", item['DataBaseServerName'])
    cf.set("ErpServer", "DataBaseServerIp", item['DataBaseServerIp'])
    cf.set("ErpServer", "UserName", item['UserName'])
    cf.set("ErpServer", "Password", item['Password'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))


def set_erp(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("ERP", "DataBaseName", item['DataBaseName'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))

def set_ktv(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("KTV", "Version", item['Version'])
    cf.set("KTV", "DataBaseName", item['DataBaseName'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))

def set_misc(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))

    cf.set("Misc", "Salutatory", item['Salutatory'])
    cf.set("Misc", "StayTime", item['StayTime'])

    cf.set("Misc", "LoginPhoto", item['LoginPhoto'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))


def set_video_server(jsondata,strcode):
    item=jsondata;
    mypath=read_path_ini()
    cf = IniConfig()
    cf.readfp(codecs.open(mypath['systemparh'], "r", strcode))
    cf.set("VideoServer", "AssignMethod", item['AssignMethod'])
    cf.set("VideoServer", "LoadMethod", item['LoadMethod'])
    cf.set("VideoServer", "Hosttask", item['Hosttask'])
    cf.set("VideoServer", "RandPlayType", item['RandPlayType'])
    cf.write(codecs.open(mypath['systemparh'], "w", strcode))
    
def set_odbc_ini(filename,jsondata,strcode):
    item=jsondata;
    cf=IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("krok","SERVER",item['DataBaseServerIp'])
    cf.set("krok","USER",item['UserName'])
    cf.set("krok","PASSWORD",item['Password'])
    
    cf.set("mysql","SERVER",item['DataBaseServerIp'])
    cf.set("mysql","USER",item['UserName'])
    cf.write(codecs.open(filename, "w", strcode))
    
def set_my_sql(filename,jsondata,strcode):
    item=jsondata;
    cf=IniConfig()
    cf.readfp(codecs.open(filename, "r", strcode))
    cf.set("MYSQL","SERVER",item['DataBaseServerIp'])
    cf.set("MYSQL","USER",item['UserName'])
    cf.write(codecs.open(filename, "w", strcode))
    
def comp_by_ip(x,y):
    aa=int(x['Room_IpAddress'].split(".")[-1])
    bb=int(y['Room_IpAddress'].split(".")[-1])
    if aa<bb:
        return -1
    elif aa==bb:
        return 0
    else :
        return 1
    
conn = MySQLdb.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL["port"], user=get_all_thunder_ini()['mainserver']['UserName'], passwd=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['db'],charset='UTF8',cursorclass=cursors.DictCursor)


def initDataBase():
    errorSql={}
    def createSQLTabel(sql):
        errorSql["sql"]=sql
        cursor = conn.cursor()
        n = cursor.execute(sql)
        cursor.close()
    try:
        print("fix table columns")
        createSQLTabel("ALTER table Record_Meta add column if not exists newscore varchar(32); ")
        createSQLTabel("ALTER table ktvcloud_musicscore add column if not exists newscore varchar(32); ")
        
        createSQLTabel(" alter table ktvcloud_musicscore change id id int auto_increment; ")
        createSQLTabel(" alter table addmedia modify column AddMedia_Size bigint; ")
        createSQLTabel(" update karaokversions set KaraokVersion_ver='5.0.0.70'; ")
        createSQLTabel(" alter table medias add column if not exists media_light int not null default 0; ")
        createSQLTabel(" alter table rooms add column if not exists theme_id int ;")
        print("adding table usermedias...")
        #/* --自定义轮播 */
        createSQLTabel("""
create table if not exists usermedias (
        Media_no varchar(10),
        Room_SerialNo varchar(30),
        Allday int,
        Begintime varchar(20),
        Endtime varchar(20)
)
        """)
        print("adding table cloud_musicshadow...")
        #/*流水影*/
        createSQLTabel("""
Create Table if not exists cloud_musicshadow (
        id integer not null auto_increment,
        Shadow_no integer comment '流水影编号',
        savepath varchar(200) comment '流水影视频路径',
        music_type varchar(50) comment '流水影类型',
        CreateTime datetime default CURRENT_TIMESTAMP comment '创建时间',
        primary key (id)
)
        """)


        cursor = conn.cursor()
        sql = "SELECT Carrier_Name FROM carriers"
        n = cursor.execute(sql)
        rows = cursor.fetchall()
        carriers = []
        for row in rows:
            carriers.append(row['Carrier_Name'])
        cursor.close()

        print("adding new media carriers...")
        createSQLTabel(" alter table carriers change Carrier_ID Carrier_ID integer not null AUTO_INCREMENT ")

        if 'WAV' not in carriers:
            createSQLTabel(" insert into carriers(Carrier_Name, Carrier_Description) values('WAV','WAV') ")
        if 'LS' not in carriers:
            createSQLTabel(" insert into carriers(Carrier_Name, Carrier_Description) values('LS','LS') ")
        if 'LSS' not in carriers:
            createSQLTabel(" insert into carriers(Carrier_Name, Carrier_Description) values('LSS','LSS') ")
        print("updating procedure sp_SetMediaIndex...")
        createSQLTabel(" drop PROCEDURE if exists `sp_SetMediaIndex`")
        createSQLTabel("""
CREATE PROCEDURE `sp_SetMediaIndex`()
proc:BEGIN
    declare result int;
    declare id int;
    declare _err int default 0;  
    declare continue handler for sqlexception set _err=1;  	
    
    
    SET @STMT := CONCAT("select SettingInfo_Value into @changetime from systemsettinginfo where SettingInfo_Name = 'MeidasIndexCreateTime'");
    PREPARE STMT FROM @STMT;
    EXECUTE STMT;
    DEALLOCATE PREPARE STMT;

    IF @changetime is null THEN		
            call sp_createuniqueid('SystemSettingInfo','SettingInfo', @id);
            SET @STMT := CONCAT("INSERT	INTO	systemsettinginfo(SettingInfo_ID,SettingInfo_Name,SettingInfo_Value) VALUES (CAST(@id, VARCHAR),'MeidasIndexCreateTime',now())");
            PREPARE STMT FROM @STMT;
            EXECUTE STMT;
            DEALLOCATE PREPARE STMT;
            IF _err<>0 THEN
                    set result = 1;
            END IF;
    ELSE
            SET @STMT := CONCAT("SELECT DATEDIFF(@changetime, now()) into @dtc");
            PREPARE STMT FROM @STMT;
            EXECUTE STMT;
            DEALLOCATE PREPARE STMT;
            
            IF @dtc <=0 THEN
                    SET @STMT := CONCAT("select count(*) into @icount from meidasindex");
                    PREPARE STMT FROM @STMT;
                    EXECUTE STMT;
                    DEALLOCATE PREPARE STMT;
                    
                    IF @icount <> 0
                    THEN
                            set result = 2;
                    ELSE 
                            SET @STMT := CONCAT("update systemsettinginfo set SettingInfo_Value = now() where SettingInfo_Name = 'MeidasIndexCreateTime'");
                            PREPARE STMT FROM @STMT;
                            EXECUTE STMT;
                            DEALLOCATE PREPARE STMT;
                            
                            IF _err <> 0 THEN
                                            set result = 3;
                            END IF;
                    END IF;
            ELSE
                    SET @STMT := CONCAT("update systemsettinginfo set SettingInfo_Value = @nowtime where SettingInfo_Name = 'MeidasIndexCreateTime'");
                    PREPARE STMT FROM @STMT;
                    EXECUTE STMT;
                    DEALLOCATE PREPARE STMT;
                    if _err<>0 THEN
                            set result = 4;
                    END IF;
            END IF;
    END IF;

    SET @STMT := CONCAT("delete from meidasindex");
    PREPARE STMT FROM @STMT;
    EXECUTE STMT;
    DEALLOCATE PREPARE STMT;
    COMMIT;
    
    SET @STMT := CONCAT("ALTER TABLE meidasindex AUTO_INCREMENT =1");
    PREPARE STMT FROM @STMT;
    EXECUTE STMT;
    DEALLOCATE PREPARE STMT;
    COMMIT;
    
    SET @STMT := CONCAT("INSERT INTO meidasindex(MeidasIndex_Media_ID) SELECT Media_ID FROM medias1 ",
                    "where  Media_Name not like '%[0-9][A-B][0-9]%' ",
                    "order by MediaManage_OrderCount desc,media_Name_length,Media_IsReserved5,Media_HeaderSoundSequence,Media_Name,Media_Sequence");
    
    PREPARE STMT FROM @STMT;
    EXECUTE STMT;
    DEALLOCATE PREPARE STMT;
    if _err<>0 THEN
            set result = 6;
    END IF;
END
        """)
        print("updating procedure SP_ClearMediasMenuAndRecord...")
        createSQLTabel(" drop PROCEDURE if exists `SP_ClearMediasMenuAndRecord`")
        createSQLTabel("""
CREATE PROCEDURE `SP_ClearMediasMenuAndRecord`(in RoomId int, in croom_ip varchar(20))
proc:BEGIN
    IF croom_ip <>'' THEN
	SET @STMT := CONCAT("select room_id into @RoomId from rooms where room_ipaddress = '",croom_ip,"'");
	PREPARE STMT FROM @STMT;
	EXECUTE STMT;
	DEALLOCATE PREPARE STMT;

	IF @RoomId  <>'' THEN		
	    SET @STMT := CONCAT("delete from MediasMenu where MediaMenu_Room_ID = ",@RoomId);
	    PREPARE STMT FROM @STMT;
	    EXECUTE STMT;
	    DEALLOCATE PREPARE STMT;
	END IF;

	SET @STMT := CONCAT("delete from Record where Record_IP = '",croom_ip,"'");
	PREPARE STMT FROM @STMT;
	EXECUTE STMT;
	DEALLOCATE PREPARE STMT;
    END IF;
END

        """)

	#--云端信息表
        createSQLTabel("""
CREATE TABLE if not exists cloud_musicinfo (
   music_no int not null primary key COMMENT '歌曲编号唯一',
   music_name varchar(128) COMMENT '歌曲名称',
   music_singer varchar(256) COMMENT '歌星',
   music_3d1 varchar(20) COMMENT '3d分类',
   music_3d2 varchar(20) COMMENT '3d分类2',
   music_downloadcount int COMMENT '歌曲线上下载次数',
   music_ishd tinyint COMMENT '是否高清',
   music_isnew tinyint COMMENT '是否新歌',
   music_isoften tinyint COMMENT '是否常唱',
   music_isreplace tinyint COMMENT '是否替换',
   music_state tinyint COMMENT '是否使用',
   music_lastver varchar(20) COMMENT '版本号',
   music_lang varchar(20) COMMENT '语言',
   music_type1 varchar(20) COMMENT '普通分类',
   music_type2 varchar(20) COMMENT '普通分类2',
   music_status int COMMENT '歌曲状态 0：未下载 1：替换 2：已下载 3：待添加', 
   music_lastverdate datetime COMMENT '更新时间',
   music_unixtime bigint COMMENT '更新时间戳',
   index cloud_musicinfo_music_no (music_no)
) ;
	""")
	#下载列表
        createSQLTabel("""
CREATE TABLE if not exists cloud_downlog(
    down_id integer primary key not null auto_increment COMMENT 'id',   
    down_gid varchar(32) comment '下载任务gid',
    music_no varchar(20) COMMENT '歌曲编号', 
    music_caption varchar(256) COMMENT '歌曲名称', 
    music_singer varchar(256) COMMENT '歌星',  
    music_lang varchar(16) COMMENT '语言',  
    music_theme varchar(16) COMMENT '分类',       
    music_ver float COMMENT '版本',         
    music_verdate datetime COMMENT '版本最后更新时间',     
    down_path varchar(256) COMMENT '下载路径',  
    down_url varchar(256) COMMENT '下载url',       
    file_size bigint COMMENT '文件大小',   
    down_stime datetime COMMENT '添加下载列表时间',        
    down_etime datetime COMMENT '下载完成时间',       
    down_status tinyint comment '下载状态, 下载完成状态:0-正在下载，1-下载完成，2-已暂停，3-下载失败',
    music_addtime datetime COMMENT '成功加歌时间',        
    music_hot varchar(50) COMMENT '热度',       
    music_replace tinyint COMMENT '是否替换',           
    music_type varchar(32) COMMENT '歌曲类型',           
    down_type tinyint COMMENT '歌曲下载触发类型, 0:实时下载,1:云端强推,2:手动下载,',           
    file_md5 varchar(50) COMMENT '',
    file_type varchar(10) COMMENT '文件类型',
    movie_type tinyint COMMENT '电影类型 0 片花 1 正片'
  ) ;
	""")
	#云端配置表
        createSQLTabel("""
CREATE TABLE if not exists cloud_appsetting (
	setting_id int(11)  not null auto_increment COMMENT 'ID',
	setting_name  varchar(100) COMMENT '配置名称',
	setting_value varchar(256) COMMENT '配置内容',
	PRIMARY KEY (setting_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
	""")
        cursor = conn.cursor()
        sql = "SELECT setting_name FROM cloud_appsetting"
        n = cursor.execute(sql)
        rows = cursor.fetchall()
        setting_name = []
        for row in rows:
            setting_name.append(row['setting_name'])
        cursor.close()
        if u'云服务器内网IP' not in setting_name:
            createSQLTabel("insert into cloud_appsetting(setting_name, setting_value) values('云服务器内网IP', '')")

        cursor = conn.cursor()
        sql = "SELECT SettingInfo_Name FROM systemsettinginfo"
        n = cursor.execute(sql)
        rows = cursor.fetchall()
        setting_name = []
        for row in rows:
            setting_name.append(row['SettingInfo_Name'])
        cursor.close()


        if 'CloudMusic_uname' not in setting_name:
            createSQLTabel("insert into systemsettinginfo values(96, 'CloudMusic_uname', '')")
        if 'CloudMusic_passwd' not in setting_name:
            createSQLTabel(" insert into systemsettinginfo values(97, 'CloudMusic_passwd', '')")
        if 'CloudMusic_realdown' not in setting_name:
            createSQLTabel(" insert into systemsettinginfo values(98, 'CloudMusic_realdown', '1')")

        createSQLTabel(""" create table if not exists record_info(
id integer NOT NULL AUTO_INCREMENT,
name varchar(128) NOT NULL DEFAULT '' COMMENT '录音歌曲名字',
room_ip varchar(32) NOT NULL DEFAULT '' COMMENT '房间IP',
media_no varchar(32) NOT NULL DEFAULT '' COMMENT '歌曲编号',
score varchar(32) NOT NULL DEFAULT '' COMMENT '录音评分',
calorie varchar(32) NOT NULL DEFAULT '' COMMENT '录音评分',
create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 """)

        createSQLTabel("""create table if not exists room(
id integer NOT NULL AUTO_INCREMENT,
ip varchar(32) NOT NULL DEFAULT '' COMMENT '房间IP',
state tinyint(1) NOT NULL DEFAULT '0' COMMENT '房间状态 0: 关台, 1: 开台',
create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 """)

        print '创建表完成'

        return True
    except Exception as ex:
        print(traceback.format_exc())
        print '创建表失败: %s' % str(ex)
        print errorSql["sql"]
    return False

if __name__ == '__main__':
    #init logging
    ret = initDataBase()
    if ret:
        sys.exit(0)
    else:
        sys.exit(2)
