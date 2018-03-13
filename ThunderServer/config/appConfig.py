#-*- coding:utf-8 -*-
import os
import sys
import logging
import traceback
import threading

import platform
from ctypes import *
from common.iniconfig import IniConfig
from common.tstypes import try_to_int

logger = logging.getLogger(__name__)

# 创建锁
Lock = threading.Lock()

#def singleton(cls, *args, **kw):  
#    instances = {}  
#    def _singleton():  
#        if cls not in instances:  
#            instances[cls] = cls(*args, **kw)  
#        return instances[cls]  
#    return _singleton 

### <summary>
### 数据库连接信息
### </summary>
class ServerConnstring(object):
    ### 服务器IP
    dbip = ''
    ### 用户名
    user = ''
    ### 密码
    pwd = ''
    ### 数据库名称
    db = ''
    ### 程序名称
    application = ''
    ### 连接字符串
    @property
    def connstring(self):
        return "Application Name={4};host={0};user={1};password={2};db={3};Pooling=true;Max Pool Size=2000".\
                format(self.dbip, self.user, self.pwd, self.db, self.application)
    ### 连接字符串
    @property
    def mysqlconnstring(self):
        return "host={0};user={1};password={2};db={3};Pooling=true;CharSet=utf8;port=3306".\
                format( self.dbip, self.user, self.pwd, self.db)


### 读取thunder.init 和 cloudktvsong.ini 配置
#@singleton
class AppSet(object):
    if platform.system().lower() == 'windows':
        cloudktvsong_ini = r"c:\thunder\cloudktvsong.ini"
        thunder_ini = r"c:\thunder\Thunder.ini"
    #elif platform.system().lower() == 'linux':
    else:
        cloudktvsong_ini = "/opt/thunder/cloudktvsong.ini"
        thunder_ini = "/opt/thunder/thunder.ini"
    #需要知道当前的地址
    if platform.system().lower() == 'windows':
        LocalDataPath = os.path.join(r"c:\thunder","thunderserivce")
        server_localpath = r"c:\thunder\ktvservice\ktv_o2oadinfo"
        ApachPath = r"c:\thunder\Apache"
        _trandownpath = r"c:\thunder\Apache\htdocs"
        BaseDirectory = r"c:\thunder"
        tempDir = r"c:\thunder"
    else:
        #elif platform.system().lower() == 'linux':
        LocalDataPath = os.path.join("/opt/thunder","thunderserivce")
        server_localpath = "/opt/thunder/ktvservice/ktv_o2oadinfo"
        ApachPath = "/opt/thunder/www"
        #a temp folder to save download files
        _trandownpath = "/data/download"
        BaseDirectory = "/opt/thunder"
        tempDir = "/data/tmp"

 
    ApachFileDownPath = os.path.join(_trandownpath,'ktvservice')


    #sqlconnpatt = "Application Name=cloudktvsong;Data Source={0};User ID={1};Password={2};Initial Catalog={3};Pooling=true"
    #mysqlconnpatt = "Data Source={0};User ID={1};Password={2};Initial Catalog={3};Pooling=true;CharSet=utf8;port=3306"
    ### 移动练歌房伴奏域名
    #MobileKtvBzHost = "http://bzmusic.ktvdaren.com"
    ### 移动练歌房v3域名
    #MobileKtvApiHost = "http://v3.service.ktvdaren.com"
    _ins = None
    ### 加密用Key
    SKey = "6f9c625e6b9c11e3bb1b94de806d865"
    ### 是否启用HTTP代理
    TProxy = 3
    ### 当前程序请求UA
    UserAgent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1;ThunderStone; CloudKtvSong)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
    ### 检测工具请求UA
    UserAgent_Doctor = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1;ThunderStone; CloudKtvDoctor)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
    ### Apache 文档缓存大小
    _apacheCacheSize = 0
    # TestModel 0:默认 1:sleep模式
    _testModel = 0
    ### 收到大便的最多数量后就自动切歌
    _shitmaxcount = 0
    ### 已点列表数量
    _songListLimit = 0
    _karaok = None
    _erp = None
    thunderini = None
    cloudktvini = None
    #下载升级
    #serviceUrl =    "http://ktv.api.ktvdaren.com/"
    Ktv90 =        "http://v1.ktv.api.ktvdaren.com"
    KtvApi =        "http://ktv.api.ktvdaren.com"
    songlist =      "http://ktv.api.ktvdaren.com"
    O2OAPI = "http://api.ktvsky.com"
    O2OAPI1 = "http://api.stage.ktvsky.com"
    kcloud_v2 = "http://kcloud.v2.service.ktvdaren.com"
    #cloudmusic appid
    cm_appid = 'ebf0694982384de46e363e74f2c623ed'
    ### 支付宝2.0RSA私钥路径
    #AlipayRSAPrivateKey = thunderini.ReadString("Cloudktvsong", "AlipayRSAPrivateKey", "")
    ### 支付宝分配给开发者的应用ID
    #AlipayAppid = thunderini.ReadString("Cloudktvsong", "AlipayAppid", "")
    ### 支付宝商户门店编号
    #AliStoreId = thunderini.ReadString("Cloudktvsong", "store_id", "")
    ### 卖家支付宝用户ID
    #AliSellerId = thunderini.ReadString("Cloudktvsong", "seller_id", "")
    #DLL 句柄，用来打开加密狗动态库，读取加密狗信息
    libdog = None
    # 定义静态变量实例
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('appConfig.py/AppSet singleton is not exists')
            try:
                # 锁定
                Lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(AppSet, cls).__new__(cls, *args, **kwargs)
                    cls.__instance.init()
            finally:
                # 锁释放
                Lock.release()
        else:
            #print('appConfig.py/AppSet singleton is exists')
            pass
        return cls.__instance

    def init(self):
        self.thunderini = IniConfig(self.thunder_ini)
        self.cloudktvini = IniConfig(self.cloudktvsong_ini)
        self._karaok = ServerConnstring()
        self._karaok.dbip = self.thunderini.ReadString("MainServer", "DataBaseServerIp", "127.0.0.1")
        self._karaok.user = self.thunderini.ReadString("MainServer", "UserName", "sa")
        self._karaok.pwd = self.thunderini.ReadString("MainServer", "Password", "")
        self._karaok.application = "thunder_common"
        self._karaok.db = "karaok"
        self.TProxy = self.GetCloudKtvIniValue("Proxy", "3")
        if platform.system().lower() == 'windows':
            filename="lib\GetDogName.dll"
        else:
            filename="/opt/thunder/lib/libGetDogInfo.so"
        #从上面的代码得到dll的绝对路径之后下面的代码可以读取dll
        #TODO following code should be change when running on linux like system
        self.libdog = CDLL(filename)

    def get_LogLevel(self):
        '''
            get LogLevel
            0：debug 1:info 3:error
            default 1
        '''
        #if DEBUG
        #return 0
        #endif
        v = self.cloudktvini.ReadString("CloudKtvSong", "LogLevel", "info")
        v = v.lower()
        if v == 'debug':
            return 0
        elif v ==  "info":
            return 1
        elif v ==  "fail":
            return 2
        elif v ==  "error":
            return 3
        else:
            return 1

    def get_SongListLimit(self):
        '''
            获取已点列表数量
        '''
        try:
            if self._songListLimit == 0:
                listcount = self.GetCloudKtvIniValue("StbSongList", "50")
                listcount = try_to_int(listcount, 50)
                listcountlimit = 50
                listcountlimit = listcount if listcount <= 100 and listcount>=10 else 50
                self._songListLimit = listcountlimit
            return self._songListLimit
        except Exception as ex:
            logging.error(traceback.format_exc())
            self._songListLimit = 50
        return self._songListLimit

    def get_ShitMaxCount(self):
        '''
            收到大便的最多数量后就自动切歌
        '''
        try:
            if self._shitmaxcount == 0:
                scount = self.GetCloudKtvIniValue("MaxShit", "0")
                scount = try_to_int(scount, 0)
                if scount > 10:
                    listcountlimit = 10
                elif scount < 0:
                    listcountlimit = 0
                else:
                    listcountlimit = scount
                self._shitmaxcount = listcountlimit
            return self._shitmaxcount
        except Exception as ex:
            logging.error(traceback.format_exc())
            self._shitmaxcount = 5
        return self._shitmaxcount

    ### mqtt 相关url
    def get_MqttAPIURL(self):
        return self.GetCloudKtvIniValue("MqttAPIURL", "http://k.kdaren.com")
    ### 获取ffmpeg 目录
    def get_FFmpegPath(self):
        return self.GetCloudKtvIniValue("FFmpegPath", "C:\\thunder\\ffmpeg")
    def get_TestModel(self):
        '''
            获取TestModel 0:默认 1:sleep模式
        '''
        try:
            if self._testModel == None:
                self._testModel = self.GetCloudKtvIniValue("TestModel", "0")
                self._testModel = int(self._testModel)
        except:
            self._testModel = 0
        return self._testModel
    def get_TestInterface(self):
        return self.GetCloudKtvIniValue("TestInterface", "")
    def get_ApacheCacheSize(self):
        try:
            if self._apacheCacheSize == 0:
                size = self.GetCloudKtvIniValue("ApacheCacheSize", "1024")
                sizelimit = 1024
                if size > 4096:
                    sizelimit = 4096
                elif size < 256:
                    sizelimit = 256
                else:
                    sizelimit = size
                self._apacheCacheSize = sizelimit * 1024 * 1024
        except Exception as ex:
            #default value
            self._apacheCacheSize = 1024 * 1024 * 1024
        return self._apacheCacheSize
    def get_DBtype(self):
        '''
            获取Cloudktvsong连接的数据库
            1:sqlserver 2:mysql
        '''
        #return self.GetCloudKtvIniValue("DBtype", "1")
        #force for linux
        return 2
    #region 获取加密狗名称
    _dogname = None
    _dogserver = ''
    _maxuser = 0
    ### 调用C++dll 获取加密狗名称
    ### <param name="sb"></param>
    ### <returns></returns>
    #[DllImport("lib/GetDogName.dll")]
    #static extern int GetDogName(StringBuilder sb)
    ### <summary>
    ### 调用C++dll 获取插加密狗服务器的IP
    ### </summary>
    ### <param name="sb"></param>
    ### <returns></returns>
    #[DllImport("lib/GetDogName.dll")]
    #static extern int GetDogServerIP(StringBuilder sb)
    ### <summary>
    ### 调用C++dll 获取加密狗名称
    ### </summary>
    ### <param name="sb"></param>
    ### <returns></returns>
    #[DllImport("lib/GetDogName.dll")]
    #static extern int GetMaxUser(StringBuilder sb)
    #endregion
    ### 获取加密狗名称
    def get_DogName(self):
        #self._dogname = '惊艳Linux测试'
        #return self._dogname
        if not self._dogname:
            class ss(Structure):
                _fields_=[ ("name", c_byte*32), ]
            try:
                filename="/opt/thunder/lib/libGetDogInfo.so"
                lib = cdll.LoadLibrary(filename)
                t = ss()
                dog= lib.GetDogName(pointer(t))
                tt = create_string_buffer(33)
                memmove(tt, byref(t), 32)
                temp = tt.value.__str__()
                self._dogname = temp.strip().decode('gbk').encode('utf8')
            except Exception as ex:
                logging.error(traceback.format_exc())
                self._dogname = ''
     
            if self._dogname == "?":
                self._dogname = ''
        return self._dogname

    ### <summary>
    ### 获取karaok版本信息
    ### 参数1.szMajVersion：主版本号，2.szMinVersion：小版本号，3.dwErrorCodeInfo：错误码
    ### </summary>
    ### <param name="szmainver">主版本</param>
    ### <param name="szminver">小版本</param>
    ### <param name="snerrorinfo">错误信息</param>
    ### <returns>返回值：返回 -1：失败，返回1：成功</returns>
    #[DllImport("lib/TDUpdateStatue.dll")]
    #static extern int TDGetVersionINfo(StringBuilder szmainver, StringBuilder szminver, StringBuilder snerrorinfo)
    ### <summary>
    ### 获取机顶盒版本信息
    ### </summary>
    ### <param name="ktv_mver">大版本</param>
    ### <param name="ktv_sver">小版本</param>
    ### <returns></returns>
    def GetVersion(self):
        try:
            if platform.system().lower() == 'windows':
                filename = r'c:\thunder\lib\TDUpdateStatue.dll'
            #elif platform.system().lower() == 'linux':
            else:
                filename = r'/opt/thunder/lib/TDUpdateStatue.dll'
            szmainver = bytes(64)
            szminver = bytes(64)
            snerrorinfo = bytes(64)
            cwd=os.path.dirname(os.getcwd())
            lib = cdll.LoadLibrary(filename)
            try:
                res = lib.TDGetVersionINfo(szmainver, szminver, snerrorinfo)
                if res != 1:
                    return 0
            except Exception as ex:
                logging.error(traceback.format_exc())
            if not szmainver:
                szmainver = '0.0.0.0'
            if not szminver:
                szminver = '0.0.0.0'
            else:
                szminver = '0.0.0.' + szminver
            ktv_mver = szmainver
            ktv_sver = szminver
            return (ktv_mver, ktv_sver)
        except Exception as ex:
            logging.error(traceback.format_exc())
        return ('0.0.0.0', '0.0.0.0')

    ### 获取加密狗名称
    def get_DogServer(self):
        if not self._dogserver:
            sb = bytes(1024)
            try:
                x = self.libdog.GetDogServerIP(sb)
                self._dogserver = str(sb).strip()
                self._dogserver = self._dogserver.strip()
            except Exception as ex:
                logging.error(traceback.format_exc())
                self._dogserver = ''
        return self._dogserver

    ### 获取加密狗点数据
    def get_DogMaxUser(self):
        if self._maxuser <= 0:
            sb = bytes(1024)
            try:
                x = self.libdog.GetMaxUser(sb)
            except Exception as ex:
                logging.error(traceback.format_exc())
            self._maxuser = try_to_int(str(sb).strip(), 0)
            return self._maxuser

    ### 获取 cloudktvsong.ini 键 
    ### <param name="key"></param>
    ### <returns></returns>
    #def GetCloudKtvIniValue(key):
    #    return GetCloudKtvIniValue(key, null)
    ### 获取 cloudktvsong.ini 键 
    ### <param name="key"></param>
    ### <param name="d"></param>
    ### <returns></returns>
    def GetCloudKtvIniValue(self, key, d = ''):
        if self.cloudktvini:
            return self.cloudktvini.ReadString("CloudKtvSong", key, d)
        else:
            return None
    ### 设置 cloudktvsong.ini 键 
    def SetCloudKtvIniValue(self, key, value):
        if self.cloudktvini:
            return self.cloudktvini.WriteInteger("CloudKtvSong", key, value)
        else:
            return None
            
    ### 获取cloudktv 的临时目录
    def get_CloudKtvTemp(self):
        if platform.system().lower() == 'windows':
            tmpdir = "c:\\thunder\\cloudktvsong\\temp"
        elif platform.system().lower() == 'linux':
            tmpdir = "/data/tmp"
        else:
            tmpdir = '/data/tmp'
        try:
            if not os.path.exists(tmpdir):
                os.makedirs(tmpdir)
            return tmpdir
        except Exception as ex:
            logging.error(traceback.format_exc())
        return ''
    ### <summary>
    ### 获取连锁总店链接数据库字符串
    ### </summary>
    ### <param name="Branch_IP">IP</param>
    ### <param name="Branch_Database">数据库名称</param>
    ### <param name="Branch_DatabaseUser">数据库用户名</param>
    ### <param name="Branch_DatabasePwd">数据库密码</param>
    ### <returns></returns>
#     def GetDataBaseToHead(self, Branch_IP, Branch_Database, Branch_DatabaseUser, Branch_DatabasePwd):
#         return sqlconnpatt.formater(
#                 self.thunderini.ReadString("ErpServer", "DataBaseServerIp", Branch_IP), 
#                 self.thunderini.ReadString("ErpServer", "UserName", Branch_DatabaseUser), 
#                 self.thunderini.ReadString("ErpServer", "Password", Branch_DatabasePwd), 
#                 Branch_Database)

    @property
    def Karaok(self):
        return self._karaok

    @property
    def Erp(self):
        return self._erp

    @property
    def DBtype(self):
        '''
            获取Cloudktvsong连接的数据库
            1:sqlserver 2:mysql
        '''
        return self.get_DBtype()


if __name__ == '__main__':
#     cfghdl = AppSet()
#     print(" cfghdl.get_LogLevel:", cfghdl.get_LogLevel())
#     print(" cfghdl.get_SongListLimit:", cfghdl.get_SongListLimit())
#     print(" cfghdl.get_ShitMaxCount:", cfghdl.get_ShitMaxCount())
#     print(" cfghdl.get_MqttAPIURL:", cfghdl.get_MqttAPIURL())
#     print(" cfghdl.get_FFmpegPath:", cfghdl.get_FFmpegPath())
#     print(" cfghdl.get_TestModel:", cfghdl.get_TestModel())
#     print(" cfghdl.get_TestInterface:", cfghdl.get_TestInterface())
#     print(" cfghdl.get_ApacheCacheSize:", cfghdl.get_ApacheCacheSize())
#     print(" cfghdl.get_DBtype:", cfghdl.get_DBtype())
#     print(" cfghdl.get_DogName:", cfghdl.get_DogName())
#     print(" cfghdl.GetVersion:", cfghdl.GetVersion())
#     print(" cfghdl.get_DogServer: ", cfghdl.get_DogServer())
#     print("cfghdl.get_DogMaxUser:", cfghdl.get_DogMaxUser())

    conn=ServerConnstring()
