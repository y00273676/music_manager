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

def read_is_setting():
    mydata={}
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "ishasset")
    mydata['ishasset']=str_a
    return mydata

def read_thunder_changecode():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "thunderini")
    return str_a


def read_dog_ip():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "dogip")
    return str_a

def read_dog_describe():
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    str_a = cf.get("initthunder", "dogdescribe")
    return str_a

def set_dog_info(dogip,dogdescribe):
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "dogip", dogip)
    cf.set("initthunder", "dogdescribe", dogdescribe)
    cf.write(open("initstart.ini", "w"))
    
def set_dog_info_ip(dogip):
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "dogip", dogip)
    cf.write(open("initstart.ini", "w"))
    
def set_thunder_changecode(codevision):
    cf = ConfigParser.ConfigParser()
    cf.read('initstart.ini')
    cf.set("initthunder", "thunderini", codevision)
    cf.write(open("initstart.ini", "w"))
    

def set_is_setting():
    cf = ConfigParser.ConfigParser()
    cf.read('/opt/thunder/twm/initstart.ini')
    cf.set("initthunder", "ishasset", "1")
    cf.write(open("initstart.ini", "w"))  

    
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
