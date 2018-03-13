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

_DEVEL_OPT = True

devel_opt = {
        'dev_mysql': {
            'host': 'localhost',
            'user': 'root',
            'pass': 'Thunder#123',
            },
        'dev_redis': {
            'host': '127.0.0.1',
            },
        'dev_memcache': ['127.0.0.1:11211'],
        }

_MYSQL = {
    'master': {
        'host': '10.9.65.123',
        'user': 'tvapp',
        'pass': 'hello@tvapp',
        'port': 3306
    },
    'slaves': [],
    'dbs': ['karaok']
}
if _DEVEL_OPT:
    _MYSQL['master']['host'] = devel_opt['dev_mysql']['host']
    _MYSQL['master']['user'] = devel_opt['dev_mysql']['user']
    _MYSQL['master']['pass'] = devel_opt['dev_mysql']['pass']
    MYSQL = _MYSQL
else:
    MYSQL = _MYSQL

_REDIS = {
    'host' : '10.9.74.25',
    'port' : 6379,
    'db' : 0
}
if _DEVEL_OPT:
    _REDIS['host'] = devel_opt['dev_redis']['host']
    REDIS = _REDIS
else:
    REDIS = _REDIS

#Session configuration(implemented on REDIS)
session_conf = {
    'cookie_secret': "e346976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
    'session_secret': "4cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
    'session_timeout': 1200,
    'store_options': REDIS,
    }


# allow IP addresses for 'PrivateMethod'
_allowips = '103.237.90.115|103.237.90.114|61.135.173.43|114.112.91.13[0-9]|127.0.0.1|10.0.3\.\d{1,3}|192.168.0\.\d{1,3}|172.17.0.[1-254]|172.17.42.1'

app_conf = {  # 'db': _db,
        'allowips': _allowips,
        'appkey': '6f9c625e6b9c11e3bb1b94de806d865',
        'template_path': os.path.join(os.path.dirname(__file__), "tpl"),
        'static_path': os.path.join(os.path.dirname(__file__), "static")
        }

if _DEVEL_OPT:
    #this is for dev use: PLEASE use internat IP for online deploy.
    #use to get song name from songno
    KCLOUD_SERVER_URL = "http://kcloud.v2.service.ktvdaren.com"
else:
    #We should use the internat IP address for online server
    KCLOUD_SERVER_URL = "http://10.9.35.235:9005"

if _DEVEL_OPT:
    MEMCACHE_SERVERS = devel_opt['dev_memcache']
else:
    MEMCACHE_SERVERS = ['10.9.66.43:11211','10.9.73.48:11211']

_cloudStorage = {
        'imagePath': "cloud/img",
        'themePath': "cloud/theme",
        'videoPath': "cloud/video",
        'apkPath': "cloud/apk",
        'AK': "T7l3oEkEcmpk4Z5rKBiv",
        'SK': "vAdSzvuWdFje/EDKqNHiQ/qM3oBjz3EPT+5du81t",
        #if in test, please use this bucket:
        #'bucketName': "wstest",
        #For final release please use this bucket
        'bucketName': "kcloud2",
        }
if _DEVEL_OPT:
    #if in test, please use this bucket:
    _cloudStorage['bucketName'] = "wstest"
    cloudStorage = _cloudStorage
else:
    #TODO: remove this after final release
    _cloudStorage['bucketName'] = "wstest"
    ## REMOVE THIS
    #
    cloudStorage = _cloudStorage


if _DEVEL_OPT:
    #use for login authentication
    OpenApiURL = "http://open.ktv.api.ktvdaren.com"
else:
    OpenApiURL = "http://10.9.52.87:8005"


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
    
    
    
    
 
    
    
    
    
    
    






conn = MySQLdb.connect(host=get_all_thunder_ini()['mainserver']['DataBaseServerIp'], port=MYSQL['master']["port"], user=get_all_thunder_ini()['mainserver']['UserName'], passwd=get_all_thunder_ini()['mainserver']['Password'], db=MYSQL['dbs'][0],charset='UTF8')


def initDataBase():
    errorSql={}
    def createSQLTabel(sql):
        errorSql["sql"]=sql
        cursor = conn.cursor()
        n = cursor.execute(sql)
        cursor.close()
    try:
        createSQLTabel("""
        CREATE TABLE IF NOT EXISTS `addmedia` (
          `AddMedia_ID` int(11) NOT NULL AUTO_INCREMENT,
          `AddMedia_Name` varchar(50) DEFAULT NULL,
          `AddMedia_Path` varchar(200) DEFAULT NULL,
          `AddMedia_Type` varchar(30) DEFAULT NULL,
          `AddMedia_Size` int(11) DEFAULT NULL,
          `AddMedia_CreateDate` datetime DEFAULT NULL,
          `AddMedia_UpdateDate` datetime DEFAULT NULL,
          `AddMedia_State` int(11) DEFAULT NULL,
          `AddMedia_SerialNo` varchar(10) DEFAULT NULL,
          PRIMARY KEY (`AddMedia_ID`),
          KEY `index_Name` (`AddMedia_Name`),
          KEY `index_SerialNo` (`AddMedia_SerialNo`)
        )
        """)
        createSQLTabel("""
        CREATE TABLE IF NOT EXISTS `deletemedia` (
          `Media_ID` int(11) NOT NULL,
          `Media_NO` varchar(10) CHARACTER SET utf8 NOT NULL,
          PRIMARY KEY (`Media_ID`)
        )
        """)
        
        cursor = conn.cursor()
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'movie_library' AND COLUMN_NAME = 'ktvprice'"
        n = cursor.execute(sql)
        rows = cursor.fetchall()  
        COLUMN_NAME=None
        for row in rows:
            COLUMN_NAME = row[0]
        if COLUMN_NAME is None:
            createSQLTabel("""
                alter table movie_library add column( ktvprice  numeric(8,2) default 0.0);
            """)
        cursor.close()
        
        cursor = conn.cursor()
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'movie_library' AND COLUMN_NAME = 'infosource'"
        n = cursor.execute(sql)
        rows = cursor.fetchall()  
        COLUMN_NAME=None
        for row in rows:
            COLUMN_NAME = row[0]
        if COLUMN_NAME is None:
            createSQLTabel("""
                alter table movie_library add column( infosource  int);
            """)
        cursor.close()
          
        createSQLTabel("""
        alter table mediafiles modify column MediaFile_IsValid int default 1;
        """)
        createSQLTabel("""
        CREATE TABLE IF NOT EXISTS `logs` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `host` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
          `app` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
          `title` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
          `event` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
          `time` datetime DEFAULT NULL,
          `level` char(1) CHARACTER SET utf8 DEFAULT NULL,
          `flag` char(1) CHARACTER SET utf8 DEFAULT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """)
        createSQLTabel("""
            CREATE TABLE IF NOT EXISTS MenPaiAdSettings(
            MenPaiAdSetting_Id int auto_increment PRIMARY key,
            MenPaiAdSetting_SerialNo varchar(10) NULL ,
            MenPaiAdSetting_PlayCount int NULL DEFAULT 1 ,
            MenPaiType_ID int NULL DEFAULT 0 ,
            MenPaiAdSettings_RoomID int NULL DEFAULT 0
            )
        """)
        createSQLTabel("""
        alter table fileservers modify column FileServer_ModifyDate varchar(40) default NULL;
        """)
        createSQLTabel("""
        alter table fileservers modify column  FileServer_ExpireDate  varchar(40) default NULL;
        """)
        createSQLTabel("""
        CREATE TABLE IF NOT EXISTS mediafilesview(
          MediaFile_SerialNo int(10) NOT NULL PRIMARY key,
          MediaFile_Name varchar(255) DEFAULT NULL
        )
        """)
          
          
          
          
          
        createSQLTabel("""
            drop PROCEDURE if EXISTS sp_ReadAllKaraokVersions;
  
            create PROCEDURE sp_ReadAllKaraokVersions(in ReadType int)
            proc:BEGIN
                if ReadType = 1 THEN
                    select VersionHistory_Result from VersionHistory order by VersionHistory_ID desc limit 0,1;
                    leave proc;
                end if;
                  
                select  VersionHistory_Result into @TempResult from VersionHistory order by VersionHistory_ID desc limit 0, 1;
              
                select KaraokVersion_ver into @LastVersion from KaraokVersions order by KaraokVersion_ID desc limit 0, 1;
                  
                if @TempResult = 0 then
                    select @LastVersion as 'KaraokVersion';
                elseif @TempResult = 1 then
                    select  KaraokVersion_ver as 'KaraokVersion' from KaraokVersions where KaraokVersion_ver not like @LastVersion order by KaraokVersion_ID desc limit 0,1;
                elseif @TempResult is null then
                    select KaraokVersion_ver as 'KaraokVersion' from KaraokVersions where KaraokVersion_ver not like '0.0.0.0' order by KaraokVersion_ID desc limit 0, 1;
                end if;
            end;
  
        """)
        createSQLTabel("""
            drop PROCEDURE if EXISTS cloud_sp_modifymediainfo;
        
            CREATE   PROCEDURE  cloud_sp_modifymediainfo (in groupid int,  
            in serialno int,  
            in filepath nvarchar(256))
            proc:BEGIN
                declare s_id int;
                declare f_id int;
                declare done int;
                  
                declare cur_mediafiles cursor for select FileServer_ID, ServerGroup_ID from servergroups1 where FileServer_IsValid = 1; 
                DECLARE CONTINUE HANDLER  FOR  not FOUND SET done = true;
              
                SET @STMT := CONCAT("select COUNT(1) into @c_count from medias where Media_SerialNo=",serialno);
                PREPARE STMT FROM @STMT;
                EXECUTE STMT;
                DEALLOCATE PREPARE STMT;
                  
                if @c_count is null or @c_count<1 THEN
                    call sp_debug(concat("not found: groupid: ", groupid, ", serialno: ", serialno, ", filepath: ", filepath));
                    leave proc;
                END IF;
                  
                SET @STMT := CONCAT("delete from mediafiles where MediaFile_SerialNo=concat('",serialno,"','00')");
                PREPARE STMT FROM @STMT;
                EXECUTE STMT;
                DEALLOCATE PREPARE STMT;
                  
                SET @STMT := CONCAT("select Media_Manage_ID into @manageid from medias where Media_SerialNo=",serialno);
                PREPARE STMT FROM @STMT;
                EXECUTE STMT;
                DEALLOCATE PREPARE STMT;
                  
                SET @STMT := CONCAT("update medias set Media_IsReserved4 =",groupid," where Media_SerialNo =",serialno);
                PREPARE STMT FROM @STMT;
                EXECUTE STMT;
                DEALLOCATE PREPARE STMT;
                  
                SET @STMT := CONCAT("update mediadetails set ServerGroup_ID =",groupid," where Media_SerialNo =",serialno);
                PREPARE STMT FROM @STMT;
                EXECUTE STMT;
                DEALLOCATE PREPARE STMT;
                  
                OPEN cur_mediafiles;
                    cursor_loop:loop
                        FETCH cur_mediafiles INTO f_id, s_id;
                            if done then
                                    leave cursor_loop;
                            end if;
                              
                            if s_id =  groupid THEN    
                                SET @STMT := CONCAT("select '', 0 into @operation, @mediafile_id");
                                call sp_createuniqueid( 'mediafiles', 'MediaFile', @mediafile_id);
                                  
                                SET @STMT := CONCAT("insert into mediafiles(MediaFile_ID, MediaFile_MediaManage_ID, MediaFile_SerialNo,",
                                    "MediaFile_ServerID, MediaFile_Name, MediaFile_Sequence) values (",
                                    "@mediafile_id,",
                                    "@manageid,",
                                    "concat('", serialno, "','00'),'",s_id,"','", filepath ,"','1')");
                                PREPARE STMT FROM @STMT;
                                EXECUTE STMT;
                                DEALLOCATE PREPARE STMT;
                                  
                            END IF;
                    end loop cursor_loop;
                CLOSE cur_mediafiles;
            END
        """)

        
        

        print '创建表完成'
        return True
    except Exception as ex:
        #logging.error(traceback.format_exc())
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