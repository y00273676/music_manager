#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月28日
更新模板
@author: yeyinlin
'''
#模板的更新操作 需要获取在线获取模板 以及导入模板
from modules.bll.SettingBll import SettingBll
from modules.jobmanager.control.synchronousutils import synchronousutils
from modules.bll.KtvModuleVerBLL import KtvModuleVerBll
from modules.model.KtvModule_Ver import KtvModule_Ver
from common.KtvInfo import hdl_ktvinfo
from modules.jobmanager.control.moduleapi import moduleapi
from modules.jobmanager.control.startcheck import startcheck
from config.appConfig import AppSet
import os
from common.fileutils import fileUtils
from common.ZFile import extract
import traceback
from modules.jobmanager.control.radisutils import radisutils
import json
import platform

import logging
logger = logging.getLogger(__name__)

class Moduleinfo():
    #单例模式
    _ins = None
    @staticmethod
    def Ins():
        if not Moduleinfo._ins:
            Moduleinfo._ins = Moduleinfo()
        return Moduleinfo._ins

    def __init__(self):
        self._setbll = SettingBll()
        self.synutil = synchronousutils()
        self.ktvinfo = hdl_ktvinfo._info
        self.excename = "Moduleinfo"
        self.modulename = "modules"
        self.store_path = os.path.join(AppSet()._trandownpath, self.modulename)
        if not os.path.exists(self.store_path):
            os.mkdir(self.store_path)
        self.topath = os.path.join(AppSet().ApachPath, 'modules')
        
        self.fu = fileUtils(self.excename)
        self.curmodule = {}
        self.redis = radisutils()
        self.firsttime = 0
        #本地的字典数据
        self.local_dict = {}
        self.module_dict = {}
        self.error_dict = {}
        self.appver = self._setbll.getKaraokVer()

    def getLocalModules(self, bagtype):
        #empty data
        ver_item = KtvModule_Ver()
        ver_item.bagtype = bagtype
        ver_item.version = "1.0.0.0"

        #需要判断本地是否含有字典
        if not self.local_dict or self.local_dict == {}:
            #1，获取本地的模板 需要用来获取线上的
            res_list = KtvModuleVerBll().GetModuleVer()
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
            if os.path.exists(old_m.fileurl):
                os.remove(old_m.fileurl)
            if os.path.exists(old_m.unpath):
                os.removedirs(old_m.fileurl)
        return False
        
    def loadonlinemodule(self, bagtype):
        try:
            res_list = None
            mlist = []
            ver_item = self.getLocalModules(bagtype)
            #规范版本号    
            vers = ver_item.version.split(',')
            if len(vers) == 2:
                ver_item.version=ver_item.version+'.0.0'
            if len(vers) == 3:
                ver_item.version = ver_item.version+'.0'
            if self.ktvinfo.mtype != 3 and self.ktvinfo.mtype != ver_item.bagtype:
                return -1
            
            #查询出最新的模板   并且需要下载
            res_ver = moduleapi().getnewmodule(ver_item.version, bagtype, self.appver)

            #从线上拿到了数据
            if res_ver:
                if len(res_ver)>0:
                    res_ver = res_ver[0]
                    #模板的下载地址
                    #下载到在c:\\thunder\\apache\\htdocs\\modules 目录下 
                    filename = os.path.basename(res_ver.fileurl)
                    module_file = os.path.join(self.store_path, filename)
                    #module_file = os.path.join(module_path, filename)
                    #下载模板的文件
                    if not os.path.exists(module_file):
                        downres = self.fu.downfile(res_ver.fileurl, module_file, None, None)
                    else:
                        downres = True
                        
                    if downres:
                        #如果下载完成
                        res_ver.unpath = os.path.join(self.topath, "90plus_" + os.path.splitext(filename)[0])
                        #fix the fileurl(windows path) to real file path
                        res_ver.fileurl = module_file
                        #添加进全局的字典
                        self.module_dict[res_ver.id] = res_ver
                        
                        #需要指定目标的地址 如果和本地不一致就添加模板
                        if res_ver.version != ver_item.version:
                            self.curmodule[bagtype] = res_ver
                            #设置成未使用
                            res_ver.isuse = 0
                            #此处就需要添加一个对话框 出来 
                            #将模板信息存入redis 中
                            redisdata = self.redis.getshortinfobyname(self.excename)
                            if redisdata:
                                redislist = json.loads(redisdata)
                                redislist.append(res_ver.to_dict())
                                self.redis.savedatabyshort(self.excename,json.dumps(redislist))
                            else:
                                redislist=[]
                                redislist.append(res_ver.to_dict())
                                self.redis.savedatabyshort(self.excename, json.dumps(redislist))
                    else:
                        #没有下载的处理 未下载
                        self.module_dict[res_ver.id] = res_ver
                        
        except Exception as e:
            logger.error(traceback.format_exc())
            
    #同步模板到服务器    这里需要出对话框
    def synimportmodule(self, ver):
        if not ver.fileurl:
            return
        try:
            #文件存在的地方
            filename = os.path.basename(ver.fileurl)
            logger.info("(%s) (%s)" % (ver, filename))
            #解压的文件夹 
            module_file = os.path.join(self.store_path, filename)
            module_topath = os.path.join(self.topath, "90plus_" + os.path.splitext(filename)[0])
            logger.info("(%s) (%s) (%s)" % (filename, module_file, module_topath))
            if extract(module_file, module_topath):
                #ARM 服务器开始，DBAss没有加入解压库，所以下载模板时顺便解压
                self.extract_sub_package(module_topath)
                #解压完成后 同步本地文件 到目标文件 本地的文件夹 后面是目标的文件夹
                #suc_status = self.synutil.synfiletoserver(module_topath, ver.unpath, 1)
                suc_status = 1
                
                if suc_status==1:
                    #添加到模板里面
                    res = KtvModuleVerBll().AddModule(ver)
                    #添加到数据库当前最新使用的模板
                    value = module_topath.replace(AppSet().ApachPath, '')
                    if ver.bagtype == 1:
                        self._setbll.SetSettingInfo("90横版-2.0", value)
                    else:
                        self._setbll.SetSettingInfo("90竖版-2.0", value)
                    #同步成功
                    self.local_dict[ver.id] = ver
                    
                    '''
                    #需要更改redis 里面的数据
                    redisdata = self.redis.getshortinfobyname(self.excename)
                    if redisdata:
                        redislist = json.loads(redisdata)
                        redislistcopy = []
                        for item in redislist:
                            if item['id'] == ver.id:
                                item['isuse'] = 1
                            redislistcopy.append(item)
                        #更改数据添加到redis
                        self.redis.savedatabyshort(self.excename,json.dumps(redislistcopy))
                    '''
                else:
                    logger.error("Failed to sync module files to other server")
                    #同步失败
                    pass
        except Exception as e:
            logger.error(traceback.format_exc())

    def extract_sub_package(self, path):
        for f in os.listdir(path):
            if f.endswith(".zip") and os.path.isfile(os.path.join(path, f)):
                if not os.path.exists(os.path.join(path, f[:-4])):
                    os.mkdir(os.path.join(path, f[:-4]))
                #just extract whatever the file exists
                if not extract(os.path.join(path, f), os.path.join(path, f[:-4])):
                    logger.error("Failed to extract file %s " % os.path.join(path, f))

    
    def startimport(self):
        isimport = True
        try:
            #需要判断当前状况是否可以运行
            h_ver = KtvModule_Ver()
            v_ver = KtvModule_Ver()
            logger.debug("module_dict: %s" % self.module_dict)
            
            if not self.module_dict == {}:
                for item in list(self.module_dict.values()):
                    if item.bagtype==1 and h_ver.id<item.id:
                        h_ver = item
                    elif item.bagtype==2 and v_ver.id<item.id:
                        v_ver = item
            #检测模板是提示、强制 还是等待更新
            h_import = self.getimportres(h_ver.id, h_ver.isshow)
            v_import = self.getimportres(v_ver.id, v_ver.isshow)
            
            #update module automatically
            if (h_import == 2):
                self.synimportmodule(h_ver)
            if (v_import == 2):
                self.synimportmodule(v_ver)
                
            showmsg = "";
            #TODO add an interact action on WebGUI, then customer can click the "start" button.
            #update module manually, but we do this auto at first ^_^
            if (h_import == 1):
                showmsg += "横板\r\n" + h_ver.desc + "\r\n"
                #需要弹出对话框    
                logger.info(showmsg)
                self.synimportmodule(h_ver)
            if (v_import == 1):
                showmsg += "竖板\r\n" + v_ver.desc
                #需要弹出对话框    
                logger.info(showmsg)
                self.synimportmodule(v_ver)
                
        except Exception as e:
            logger.error(traceback.format_exc())
            
            
    #需要和对话框匹配
    def getimportres(self,mid,isshow):
        if mid<0:
            return 0
        if isshow:
            return 1
        else:
            return 2
        return 2
            
if __name__ == '__main__':
    module=Moduleinfo()
    module.loadonlinemodule(1)
    module.loadonlinemodule(2)
    module.startimport()
   
