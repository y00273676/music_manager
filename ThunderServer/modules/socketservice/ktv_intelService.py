#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import json
import socket
import hashlib
import threading
import traceback
import datetime
import codecs
import struct
import urllib
import urllib.request
import urllib.parse
import StringIO
from inteldevice import *
from localCachManage import *
from common.DownImageUtil import *
from common.DownFileUtil import *
from modules.model.Roominfo import *
from config.appConfig import *
from modules.socketservice.publicFunc import *

logger = logging.getLogger(__name__)


def dicToObject(dic,obj):
    for k in dic:
        if hasattr(obj,k):
            setattr(obj,k,dic[k])
    return obj


"""
/// <summary>
/// 智能设备
/// </summary>
"""
class ktv_intelService():
    
    apachFileDownPath = AppSet.ApachFileDownPath
    
    """
    /// <summary>
    /// 获取设备信息
    /// </summary>
    """
    def INTEL_GETDEVICEINFO(_strValue,_socketClient):
        objParam={}
        GetStrValue(_strValue,objParam)
        try:
            ip=objParam[0]
            name=objParam[1]
            module=objParam[2]
            key=localCachManage()
            count_key=getINTEL_GETDEVICEINFO_Count_Key(name,module)
            data_key=getINTEL_GETDEVICEINFO_Data_Key(name,module)
            flag = False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            ms = StringIO.StringIO('python')
            list = getinteldevicebyname(name,module)
            count = 0
            if list != None and len(list) > 0:
                for i in range(len(list)):
                    vice = list[i]
                    vice['intel_logo'] = DownImageUtil.DownPicSync(vice['intel_logo'])
                    vice = dicToObject(vice,Intel_Device())
                    tinfo = bytes(vice)
#                     tinfo=struct.pack('i64s16s512s256s',vice['intel_id'],vice['intel_name'],vice['intel_model'],vice['intel_desc'],vice['intel_logo'])
                    if tinfo != None:
                        ms.write(tinfo);
                        count+=1
                        
            datas = ms.tolist()
            ms.close()
            ms.dispose()
            _socketClient.request.sendall(count)
            if count > 0:
                _socketClient.request.sendall(datas)
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETDEVICEINFO')
    
    """
    /// <summary>
    /// 获取房间调试信息
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>  
    """
    def INTEL_GETROOMDEBUGINFO(_strValue,_socketClient):
        objParam=[]
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            key = LocalCachManage.getINTEL_GETROOMDEBUGINFO_Key()
            count_key = LocalCachManage.getINTEL_GETROOMDEBUGINFO_Count_Key(ip)
            data_key = LocalCachManage.getINTEL_GETROOMDEBUGINFO_Data_Key(ip)
            flag = False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            ms = StringIO.StringIO('python')
            infoList = getroomdebuginfo(ip)
            count = 0
            if infoList != None and len(infoList) > 0:
                debug = infoList[0]
                if roomclassinfo.room_dict != None and ip in roomclassinfo.room_dict:
                    debug['room_name']=roomclassinfo.room_dict[ip][roomName]
                    debug['room_model']=roomclassinfo.room_dict[ip][room_className]
                debug = dicToObject(debug,Intel_DebugInfo())
                info = bytes(debug)
                if info != None:
                    ms.write(info)
                    count = 1
            datas = ms.tolist()
            ms.close()
            _socketClient.request.sendall(count)
            if count > 0:
                _socketClient.request.sendall(datas)
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETROOMDEBUGINFO')
            _socketClient.request.sendall(0)
    """
    /// <summary>
    /// 获取包房最近调试记录
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_GETROOMPLANLIST(_strValue,_socketClient):
        objParam=[]
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            name = str(objParam[1])
            module = str(objParam[2])
            count = 0
            key = LocalCachManage.getINTEL_GETROOMDEBUGINFO_Key()
            count_key = LocalCachManage.getINTEL_GETROOMDEBUGINFO_Count_Key(ip)
            data_key = LocalCachManage.getINTEL_GETROOMDEBUGINFO_Data_Key(ip)
            file_Key = LocalCachManage.getINTEL_GETDEVICEPUBLICPLAN_File_Key(2)
            flag = False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            fileUrlDic={}
            ms = StringIO.StringIO('python')
            planList = getprivateplanlist(ip, name, module)
            if planList!=None and len(planList)>0:
                for plan in planList:
                    plan = dicToObject(plan,Intel_PlanList())
                    info = bytes(plan)
                    if info!=None:
                        ms.write(info)
                        count+=1
                        fileUrlDic[plan.plan_id]=plan.plan_url
            datas = ms.tolist()
            ms.close()
            _socketClient.request.sendall(count)
            if count > 0:
                _socketClient.request.sendall(datas)
            if file_Key in localCachManage.ktv_IntelCach:
                localCachManage.ktv_IntelCach.pop(file_Key)
            localCachManage.ktv_IntelCach[file_Key]=fileUrlDic
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETROOMPLANLIST')
            _socketClient.request.sendall(0)
            
    """
    /// <summary>
    /// 获取设备推荐方案
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_GETDEVICEPUBLICPLAN(_strValue,_socketClient):
        objpara={}
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            name = str(objParam[1])
            module = str(objParam[2])
            city = str(objParam[3])
            roomtype = str(objParam[4])
            if roomtype=='全部':
                roomtype=''
            if city=='全部':
                city=''
            key = localCachManage.getINTEL_GETDEVICEPUBLICPLAN_Key()
            count_key = localCachManage.getINTEL_GETDEVICEPUBLICPLAN_Count_Key(name, module, roomtype, city)
            data_key = localCachManage.getINTEL_GETDEVICEPUBLICPLAN_Data_Key(name, module, roomtype, city)
            file_Key = localCachManage.getINTEL_GETDEVICEPUBLICPLAN_File_Key(1)
            flag = False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            fileUrlDic = {}
            ms = StringIO.StringIO('python')
            pubList = getpubplanlist(name, module, roomtype, city)
            count = 0
            if pubList!=None and len(pubList)>0:
                for pub in pubList:
                    pub = dicToObject(pub,Intel_PubPlanList())
                    info = bytes(pub)
                    ms.write(info)
                    count+=1
                    fileUrlDic[pub.plan_id]=pub.plan_url
                    logger.debug('INTEL_GETDEVICEPUBLICPLAN')
                    
            datas = ms.tolist(); 
            ms.close()
            _socketClient.request.sendall(count)
            if count>0:
                _socketClient.request.sendall(datas)
            if file_Key in localCachManage.ktv_IntelCach:
                localCachManage.ktv_IntelCach.pop(file_Key)
            localCachManage.ktv_IntelCach[file_Key]=fileUrlDic
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETDEVICEPUBLICPLAN')
            _socketClient.request.sendall(0)
    """          
    /// <summary>
    /// 根据方案ID获取使用该方案的KTV列表
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_GETPLANUSEKTVLIST(_strValue,_socketClient):
        objpara={}
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            id = int(objParam[1])
            islocal = int(objParam[2])
            key = localCachManage.getINTEL_GETPLANUSEKTVLIST_Key()
            count_key = localCachManage.getINTEL_GETPLANUSEKTVLIST_Count_Key(id, islocal)
            data_key = localCachManage.getINTEL_GETPLANUSEKTVLIST_Data_Key(id, islocal)
            flag = False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            ms = StringIO.StringIO('python')
            ktvList = getplanusektv(id, islocal)
            count = 0
            if ktvList!=None and len(ktvList)>0:
                for ktv in ktvList:
                    ktv = dicToObject(ktv,Intel_PlanKTV())
                    info = bytes(ktv)
                    ms.write(info)
                    count+=1
            datas = ms.tolist()
            ms.close()
            _socketClient.request.sendall(count)
            if count>0:
                _socketClient.request.sendall(datas)
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETPLANUSEKTVLIST')
            _socketClient.request.sendall(0)
                    
    """
    /// <summary>
    /// 获取房型列表
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_GETROOMMODEL(_strValue,_socketClient):
        try:
            key = localCachManage.getINTEL_GETROOMMODEL_Key()
            count_key = localCachManage.getINTEL_GETROOMMODEL_Count_Key()
            data_key = localCachManage.getINTEL_GETROOMMODEL_Data_Key();
            flag = False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            roomList = getroommodel()
            ms = StringIO.StringIO('python')
            count=0
            if roomList != None:
                for room in roomList:
                    room = dicToObject(room,Intel_RoomModel())
                    info = bytes(room)
                    ms.write(info);
                    count+=1
            data = ms.tolist()
            ms.close()
            _socketClient.request.sendall(count)
            if count>0:
                _socketClient.request.sendall(data)
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETROOMMODEL')
            _socketClient.request.sendall(0)

    """
    /// <summary>
    /// 删除本地方案
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_DELROOMPLANINFO(_strValue,_socketClient):
        objpara={}
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            id = int(objParam[1])
            key = localCachManage.getINTEL_GETROOMPLANLIST_Key()
            result = delprivateplan(id)
            data=struct.pack('i',result)
            if result>=0:
                _socketClient.request.sendall(1)
                _socketClient.request.sendall(data)
                localCachManage.ktv_IntelCach.pop(key)
            else:
                _socketClient.request.sendall(0)
        except:
            logger.error('ktv_intelService.INTEL_DELROOMPLANINFO')
            _socketClient.Sock.Send(PublicFunc.IntToIntPtr(0), 4, SocketFlags.None);
    """
    /// <summary>
    /// 更新包房设备更换次数
    /// </summary>
    """
    def INTEL_SAVEROOMDEVICETIME(_strValue,_socketClient):
        objpara={}
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            result = updatedevicetime(ip)
            data=struct.pack('i',result)
            if result>=0:
                _socketClient.request.sendall(1)
                _socketClient.request.sendall(data)
                localCachManage.ktv_IntelCach.pop(localCachManage.getINTEL_GETROOMDEBUGINFO_Key())
            else:
                _socketClient.request.sendall(0)
        except:
            logger.error('ktv_intelService.INTEL_DELROOMPLANINFO')
            _socketClient.request.sendall(0)

    """
    /// <summary>
    /// 提交保存本地方案
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_SAVEROOMPLANINFO(_strValue,_socketClient):
        objPara={}
        GetStrValue(_strValue,objParam)
        try:
            ip = str(objParam[0])
            name = str(objParam[1])
            module = str(objParam[2])
            filePath = str(objParam[3])
            id = int(objParam[4])
            _localPlan = {}
            _localPlan['plan_id'] = id
            _localPlan['plan_intelmodel'] = module
            _localPlan['plan_intelname'] = name
            _localPlan['plan_name'] = "本地设备调试"
            if id>0:
                _localPlan['plan_name'] = "公开方案调试"
            _localPlan['plan_roomip'] = ip
            if roomclassinfo.room_dict != None and ip in roomclassinfo.room_dict:
                _localPlan['plan_roomtype'] = roomclassinfo.room_dict[ip][room_className]
            downFile = {}
            downFile['filePath'] = filePath
            downFile['localPlan'] = _localPlan
            downFile['socketClient'] = _socketClient
            pool = ThreadPool(5)  
            requests = threadpool.makeRequests(DownFile, downFile)    
            [pool.putRequest(req) for req in requests] 
            pool.wait()
        except:
            logger.error('ktv_intelService.INTEL_SAVEROOMPLANINFO')
            _socketClient.Sock.Send(PublicFunc.IntToIntPtr(0), 4, SocketFlags.None);
    
    """
    /// <summary>
    /// 获取城市列表
    /// </summary>
    /// <param name="_strValue"></param>
    /// <param name="_socketClient"></param>
    """
    def INTEL_GETCITYLIST(_strValue,_socketClient):
        try:
            key = localCachManage.getINTEL_GETCITYLIST_Key()
            count_key = localCachManage.getINTEL_GETCITYLIST_Count_Key()
            data_key = localCachManage.getINTEL_GETCITYLIST_Data_Key()
            flag=False
            flag = localCachManage.SendCash(_socketClient,key,count_key,data_key)
            if flag:
                return
            citylist = getcitylist()
            ms = StringIO.StringIO('python')
            count=0
            if citylist != None:
                for room in citylist:
                    room = dicToObject(room,Intel_City())
                    info = bytes(room)
                    ms.write(info)
                    count+=1
            data = ms.tolist()
            ms.close()
            _socketClient.request.sendall(count)
            if count>0:
                _socketClient.request.sendall(data)
            localCachManage.AddCash(key, count_key, data_key, count, datas)
        except:
            logger.error('ktv_intelService.INTEL_GETROOMMODEL')
            _socketClient.request.sendall(0)

    def INTEL_GETFILEURL(_strValue,_socketClient):
        objpara={}
        GetStrValue(_strValue,objParam)
        try:
            plan_id = int(objParam[0])
            type = int(objParam[1])
            file_key = localCachManage.getINTEL_GETDEVICEPUBLICPLAN_File_Key(type)
            data = None
            if file_key in localCachManage.ktv_IntelCach:
                fileURLDic = localCachManage.ktv_IntelCach[file_key]
                if fileURLDic != None and len(fileURLDic) > 0 and plan_id in fileURLDic:
                    fileurl = fileURLDic[plan_id]
                    logger.debug('INTEL_GETFILEURL' + str(plan_id) + fileurl)
                    fileurl = DownFileUtil.DownFile(fileurl)
                    if not (fileurl==None or fileurl == ""):
                        data = fileurl.encode(encoding="utf-8")
            if data != None and len(data)>=0:
                _socketClient.request.sendall(len(data))
                _socketClient.request.sendall(data)
                localCachManage.ktv_IntelCach.pop(localCachManage.getINTEL_GETROOMDEBUGINFO_Key())
            else:
                logger.debug('INTEL_GETFILEURL' + str(plan_id) + "error")
                _socketClient.request.sendall(0)
        except:
            logger.error('ktv_intelService.INTEL_DELROOMPLANINFO')
            _socketClient.request.sendall(0)

        
    operate={}
    def DownFile(urlObj):
        try:
            downfile = urlObj
            if str(downfile['filePath']).strip()!="":
                url = "http://"+str(AppSet()._karaok.dbip)+"/"+str(downfile['filePath'].replace("\\", "/"))
                local_Path = apachFileDownPath+os.path.basename(url)
                if os.path.exists(local_Path):
                    os.remove(local_Path)
                DownFileUtil.DownPath(url,local_Path)
                logger.debug('方案文件'+local_Path+'下载完毕')
#                 filename = Utils.GetFileMD5(local_Path) + Path.GetExtension(local_Path);
#                 ks3save = KS3Access.GetKs3SavePath(filename);
#                 operate = new KS3Operate(ks3save.Ks3AccessKey);
#                 operate.BucketName = ks3save.Ks3BucketName;
                operate['LocalFile'] = local_Path
#                 operate.RemoteFile = ks3save.Ks3Key;
                operate['SocketClient'] = downfile
#                 operate.UploadProgressCompletedEvent += new KS3Operate.UploadProgressCompletedEventHandler(operate_UpLoadProgressCompleteEvent);
#                 operate.UploadProgressFailedEvent += new EventHandler<ErrorEventArgs>(operate_UploadProgressFailedEvent);
#                 operate.UploadPart();
                ClassLoger.DEBUG(string.Format("方案文件{0}开始上传云端", local_Path));
                logger.debug('方案文件'+str(plan_id)+'开始上传云端')
            else:
                result = addprivateplan(downfile['localPlan'])
                data=struct.pack('i',result)
                if result>=0:
                        downfile['socketClient'].request.sendall(1)
                        downfile['socketClient'].request.sendall(data)
                        localCachManage.ktv_IntelCach.pop(localCachManage.getINTEL_GETROOMPLANLIST_Key())
                        localCachManage.ktv_IntelCach.pop(localCachManage.getINTEL_GETDEVICEPUBLICPLAN_Key())
                else:
                        downfile['socketClient'].request.sendall(0)
        except:
            logger.error('ktv_intelService.DownFile')
                
    def operate_UpLoadProgressCompleteEvent(obj,filename):
        opers = obj
        if opers == None:
            return
#         opers.SetObjectACL(opers.BucketName, opers.RemoteFile, KS3Operate.ACL.Public_Read);
        logger.info('文件'+str(opers.LocalFile)+'上传成功，保存路径:'+str(filename))
        downfile = opers['SocketClient']
        downfile['localPlan']['plan_url'] = filename
        result = addprivateplan(downfile.localPlan)
        data=struct.pack('i',result)
        if result >= 0:
            downfile['socketClient'].request.sendall(1)
            downfile['socketClient'].request.sendall(data)
            localCachManage.ktv_IntelCach.pop(localCachManage.getINTEL_GETROOMPLANLIST_Key())
            localCachManage.ktv_IntelCach.pop(localCachManage.getINTEL_GETDEVICEPUBLICPLAN_Key())
        else:
            downfile['socketClient'].request.sendall(0)
        if os.path.exists(opers.LocalFile):
            os.remove(opers.LocalFile)
    
    def operate_UploadProgressFailedEvent(obj,e):
        opers = obj
        if opers==None:
            return
        downfile = opers['SocketClient']
        downfile['socketClient'].request.sendall(0)
        logger.error('ktv_intelService.operate_UploadProgressFailedEvent'+str("文件"+str(operate.LocalFile)+"上传金山失败"))
    
    
    
    
    
    
    
        
