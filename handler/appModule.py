#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import shutil
import urllib
import logging
import datetime
import traceback
import threading

from common.fileutils import fileUtils
from common.ZFile import extract
from lib.http import request_json

#from modules.model.Ktvmodule_theme import Ktvmodule_theme
#from modules.bll.KtvModuleVerBLL import KtvModuleVerBll

from control.ktvmodules import get_all_ktvmodules,add_ktvmodule,delete_ktvmodule,get_latest_ktvmodules
from control.configs import get_config, update_setconfig
from handler.tsTask import tsServiceTask,tsTask
from setting import TMPDIR, DOWNLOADDIR, HTDOCDIR

logger = logging.getLogger(__name__)

#下载任务和更新任务不同时进行
class _appModule(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()
    #_interval = 3600
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('_appModule singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appModule, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('_appModule singleton is exists')
        return cls.__instance

    def __init__(self, name='appModule'):
        self.name = name

        self.fu = fileUtils(self.name)

        self.store_path = os.path.join(DOWNLOADDIR, self.name)
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)

        self.topath = os.path.join(HTDOCDIR, self.name)
        
        self._common_init(self.name)
        #目前请求主模板的时候，ARM与X86都传同样的参数：lk=1 (2017-12-05）
        self.lk = 1

        #self.synutil = synchronousutils()
        
        #本地的字典数据
        self.local_dict = {}
        self.module_dict = {}
        self.error_dict = {}

        #parameters for callback()
        self.pending_module = None

        self.appver = '1.0.0.0'
        cfg = get_config('karaok_ver')
        if cfg:
            self.appver = cfg['config_value']

    def do_run(self):
        print('Updating modules **************')
        self.loadOnlineModule(1)
        self.cleanModules(1)
        self.loadOnlineModule(2)
        self.cleanModules(2)
        
 
    def getNewModule(self, m_ver, bagtype, appver):
        self.dogname = tsServiceTask.get_dogname()
        self.ktvid = tsServiceTask.get_ktvid()
        if not self.dogname or not self.ktvid:
            logger.error("Failed to get dogname or ktvinfo")
            return False
        
        logger.debug("getnewmodule")
        #获取模板信息
        if self.lk == 1 or self.lk == 2:
            url = "%s/module_verservice.aspx?op=getmoduleverjson&version=%s&"\
                    "dogname=%s&bagtype=%s&storeId=%s&type=v2&appver=%s&lk=%d"\
                    % (self.songlist, m_ver, urllib.quote(self.dogname), bagtype, self.ktvid, appver, self.lk)
        else:
            url = "%s/module_verservice.aspx?op=getmoduleverjson&version=%s&"\
                    "dogname=%s&bagtype=%s&storeId=%s&type=v2&appver=%s"\
                    % (self.songlist, m_ver, urllib.quote(self.dogname), bagtype, self.ktvid, appver)

        logger.debug(url)
        dic_res = request_json(url, timeout=10, method='GET')
        arrver=[]
        if dic_res and str(dic_res['code']) == '1':
            if isinstance(dic_res['result'], dict):
                mresult = dic_res['result']['matches']
                var = self.KtvModule_Ver()
                if len(mresult) > 0:
                    for item in mresult:
                        var['id'] = item['Id']
                        var['msgtime'] = item['MsgTime']
                        var['version'] = item['Version']
                        var['fileurl'] = item['FileUrl']
                        var['desc'] = item['Desc']
                        var['addtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        var['needun'] = 0
                        var['revision'] = item['ReVision']
                        var['bagtype'] = item['BagType']
                        var['unpath'] = ""
                        var['name'] = item['Name']
                        var['isshow'] = item['IsShow']
                        var['id'] = item['Id']
                        var['isuse'] = 1
                        var['vertype'] = item['VerType']
                        var['isdefault'] = item['IsDefault']
                        arrver.append(var)
                return arrver
        return arrver

    def KtvModule_Ver(self):
        mv = {}
        mv['id'] = 0
        mv['name'] = ""
        mv['addtime'] = ""
        mv['fileurl'] = ""
        mv['unpath'] = ""
        mv['version'] = ""
        mv['isuse'] = ""
        mv['needun'] = ""
        mv['desc'] = ""
        mv['msgtime'] = ""
        mv['isshow'] = ""
        mv['bagtype'] = -1
        mv['isdefault'] = ""
        mv['reversion'] = ""
        mv['vertype'] = ""
        return mv
 

    def getLocalModules(self, bagtype):
        #empty data
        ver_item = self.KtvModule_Ver()
        ver_item['bagtype'] = bagtype
        ver_item['version'] = "1.0.0.0"

        self.local_dict = {}
        #1，获取本地的模板 需要用来获取线上的
        res_list = get_all_ktvmodules()
        for itm in res_list:
            self.local_dict[itm.id] = itm

        max_id = max(self.local_dict)
        logger.info("local module: maxid:%d" % max_id)
        if max_id:
            return self.local_dict[max_id]

        return ver_item

    def cleanModules(self, bagtype):
        count = len(self.local_dict)
        if count > 15:
            for k in range(0, count-15):
                oldest = min(self.local_dict)
                del_itm = self.local_dict.pop(oldest)
                self.delModule(del_itm)
        return True

    def delModule(self, old_m):
        if old_m:
            KtvModuleVerBll().DeleteVer(old_m.mid)
            if os.path.exists(old_m['fileurl']):
                os.remove(old_m['fileurl'])
            if os.path.exists(old_m['unpath']):
                shutil.rmtree(old_m['unpath'])
        return False

    def loadOnlineModule(self, bagtype):
        try:
            self.pending_module = None
            res_list = None
            mlist = []
            ver_item = get_latest_ktvmodules(bagtype)
            if ver_item == None:
                return False
            #规范版本号    
            vers = ver_item['version'].split(',')
            if len(vers) == 2:
                ver_item['version'] = ver_item['version'] + '.0.0'
            if len(vers) == 3:
                ver_item['version'] = ver_item['version'] + '.0'

            ktvinfo = tsServiceTask.get_ktvinfo()
            print ktvinfo
            if not ktvinfo:
                return -2

            if ktvinfo['mtype'] != 3 and ktvinfo['mtype'] != ver_item['bagtype']:
                return True
            
            #查询出最新的模板   并且需要下载
            res_vers = self.getNewModule(ver_item['version'], bagtype, self.appver)

            #从线上拿到了数据
            if len(res_vers) == 0:
                return 0

            #for res_ver in resvers:
            res_ver = res_vers[0]

            #模板的下载地址
            filename = os.path.basename(res_ver['fileurl'])
            module_file = os.path.join(self.store_path, filename)
            #下载模板的文件
            if not os.path.exists(module_file):
                downres = self.fu.downfile(res_ver['fileurl'], module_file, None, None)
            else:
                downres = True
                
            if downres:
                #如果下载完成
                res_ver['unpath'] = os.path.join(self.topath, "90plus_" + os.path.splitext(filename)[0])
                #fix the fileurl(windows path) to real file path
                res_ver['fileurl'] = module_file
                
                #需要指定目标的地址 如果和本地不一致就添加模板
                if res_ver['version'] != ver_item['version']:
                    #设置成未使用
                    res_ver['isuse'] = 0
                    if res_ver['isshow'] and self._interactive:
                        #此处就需要添加一个对话框 出来 
                        #添加进全局的字典
                        self.pending_module = res_ver
                        self._confirm = True
                        self._lastmsg = res_ver['desc']
                        return True
                    else:
                        self.deployModule(res_ver)
            else:
                logger.error("Failed to download ktvModule: %s, %s" % (res_ver['name'], res_ver['fileurl']))
                        
        except Exception as e:
            logger.error(traceback.format_exc())

    def do_callback(self):
        if not self.pending_module:
            return False
        ret = self.deployModule(res_ver)
        if not ret:
            logger.error("Failed to deploy ktvModule in callback(): %s, %s" \
                    % (self.pending_module['name'], self.pending_module['fileurl']))
            
    def deployModule(self, ver):
        if not ver['fileurl']:
            return False
        if not os.path.exists(ver['fileurl']):
            return False
        try:
            #文件存在的地方
            filename = os.path.basename(ver['fileurl'])
            logger.info("(%s) (%s)" % (ver, filename))
            #解压的文件夹 
            module_file = os.path.join(self.store_path, filename)
            module_topath = os.path.join(self.topath, "90plus_" + os.path.splitext(filename)[0])
            logger.info("(%s) (%s) (%s)" % (filename, module_file, module_topath))
            if extract(module_file, module_topath):
                #ARM 服务器开始，DBAss没有加入解压库，所以下载模板时顺便解压
                self.extract_sub_package(module_topath)
                #解压完成后 同步本地文件 到目标文件 本地的文件夹 后面是目标的文件夹
                #添加到模板里面
                res = add_ktvmodule(ver)
                #添加到数据库当前最新使用的模板
                value = module_topath.replace(HTDOCDIR, '')
                if ver['bagtype'] == 1:
                    update_setconfig({"90横版-2.0": value})
                else:
                    update_setconfig({"90竖版-2.0": value})
                return True
            else:
                #incase we got a wrong file in download, just delete it
                if os.path.exists(module_file):
                    os.path.remove(module_file)
                if os.path.exists(module_topath):
                    shutil.rmtree(module_file)
                return False
        except Exception as e:
            logger.error(traceback.format_exc())
        return False

    def extract_sub_package(self, path):
        ret = True
        for f in os.listdir(path):
            if f.endswith(".zip") and os.path.isfile(os.path.join(path, f)):
                if not os.path.exists(os.path.join(path, f[:-4])):
                    os.mkdir(os.path.join(path, f[:-4]))
                    ret = False
                #just extract whatever the file exists
                if not extract(os.path.join(path, f), os.path.join(path, f[:-4])):
                    logger.error("Failed to extract file %s " % os.path.join(path, f))
                    ret = False
        return ret

appModule = _appModule()

if __name__ == '__main__':
    pass
