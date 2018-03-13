'''
Created on 2017年4月17日

@author: yeyinlin
'''
from modules.jobmanager.NO2oadinfo import no2oadinfo
from _io import StringIO
from modules.socketservice.Ktv_tvadinfoAccess import Ktv_tvadinfoAccess
'''
Created on 2017年4月27日

@author: baizhiyu
'''

import time
from modules.socketservice.interfaceBase import interfaceBase
from modules.model.o2oad_action import *
import os

from modules.jobmanager.roomclassinfo import roomclassinfo


from modules.socketservice.localCachManage import *
from modules.socketservice.publicFunc import *
from modules.model.ktv_tvadinfo import *

class tvadinfo(object):
    __singleton = None
    @staticmethod
    def get_instance():
        if tvadinfo.__singleton is None:
            tvadinfo.__singleton = tvadinfo()
        return tvadinfo.__singleton
    def __init__(self):
        self.interface=interfaceBase()
        
        
        
#     /// <summary>
#     /// 获取广告列表
#     /// </summary>
#     /// <param name="_strValue"></param>
#     /// <param name="_socketClient"></param>
    def STBTVADINFOLIST(self,_strValue,_socketClient):
        try:
            if len(localCachManage.Ktv_tvadinfoCach)==0:
                _socketClient.request.sendall(0)
                return
            ms = StringIO.StringIO('python')
            count = 0
            
            for info in localCachManage.GetKtv_tvadinfo():
                if info != None:
                    logger.debug('中转服务器给机顶盒发送广告内容')
                    _info = self.ConvertByinfos(info)
                    infos = bytes(_info)
                    ms.write(infos)
                    count+=1
            data = ms.tolist()
            ms.close()
            _socketClient.request.sendall(count)
            if count>0:
                _socketClient.request.sendall(data)
        except:
            logger.error('ktv_tvadinfoService.STBTVADINFOLIST')
            _socketClient.request.sendall(0)
            
#     /// <summary>
#     /// 记录广告播放记录
#     /// </summary>
#     /// <param name="_strValue"></param>
#     /// <param name="_socketClient"></param>
    def STBTVADSHOWTIME(self,_strValue,_socketClient):
        pf=PublicFunc()
        objParam = {}
        pf.GetStrValue(_strValue,objParam)
        try:
            ip=objParam[0]
            adid=objParam[1]
            roomstatus=objParam[2]
            ad = ktv_tvad_log()
            ad.ad_id = adid
            ad.roomip = ip
            ad.roomstatus = roomstatus
            ad.time = time.gettime()
            info = localCachManage.GetKtv_tvadinfoByID(adid)
            if info != None:
                ad.ad_name = info.ad_name
            
            Ktv_tvadinfoAccess.Ins().Addktv_tvadlog()
            _count = ktv_tvad_count()
            _count.ad_id = adid
            _count.ad_name = ad.ad_name
            _count.roomstatus = ad.roomstatus
            Ktv_tvadinfoAccess.Ins().AddKtv_tvadTimes()
            _socketClient.request.sendall(1)
        except:
            logger.error('ktv_tvadinfoService.STBTVADSHOWTIME捕获异常')
            _socketClient.request.sendall(0)
            
#     /// <summary>
#     /// 获取广告列表
#     /// </summary>
#     /// <param name="_strValue"></param>
#     /// <param name="_socketClient"></param>        
    def geto2oadvideolist(self,_strValue,_socketClient):
        try:
            objParam = {}
            pf=PublicFunc()
            pf.GetStrValue(_strValue,objParam)
            roomstate = objParam[0]
            logger.info('geto2oadvideolist-gtad'+str(roomstate))
            res_json = self.geto2opos(roomstate)
            self.interface.SendListToStb(_strValue, _socketClient, res_json)
        except:
            logger.error('ktv_tvadinfoService.geto2oadvideolist')
            self.interface.SendListToStb(_strValue, _socketClient, 0)
            
            
    
#     /// <summary>
#     /// 获取广告播放间隔
#     /// </summary>
#     /// <param name="_strValue"></param>
#     /// <param name="_socketClient"></param>
    def GETTVADININTERVAL(self,_strValue,_socketClient):
        try:
            _socketClient.request.sendall(localCachManage.tvadinintervalCach)
        except:
            logger.error('ktv_tvadinfoService.GETTVADININTERVAL捕获异常')
            _socketClient.request.sendall(0)
            
    
                
    
    def ConvertByinfos(self,info):
        infos = ktv_tvadinfo()
        infos.ad_bigurl = info['ad_bigurl']
        infos.ad_bigx = info['ad_bigx']
        infos.ad_bigy = info['ad_bigy']
        infos.ad_id = info['ad_id']
        infos.ad_playtime = info['ad_playtime']
        infos.ad_showtime = info['ad_showtime']
        infos.ad_smallurl = info['ad_smallurl']
        infos.ad_smallx = info['ad_smallx']
        infos.ad_smally = info['ad_smally']
        return infos
            
        

        
        
        
        
        
        
        
        
#         /// <summary>
#         /// 获取广告字幕信息
#         /// </summary>
#         /// <param name="_strValue"></param>
#         /// <param name="_socketClient"></param>
    def geto2ocaptioninfo(self,_strValue,_socketClient):
        try:
            res_json={}
            res_json=no2oadinfo().Ins().res_adcaption()
            res_json['code']=200
            res_json['msg']='OK'
            self.interface.SendListToStb(_strValue, _socketClient, res_json)
        except Exception as e:
            self.interface.SendListToStb(_strValue, _socketClient, 0)
            print(e)
    
    def geto2oadgitlist(self,_strValue,_socketClient):
        try:
            res_json = self.geto2opos(-1)
            self.interface.SendListToStb(_strValue, _socketClient, res_json)
        except Exception as e:
            self.interface.SendListToStb(_strValue, _socketClient, 0)
            print(e)
    def geto2opos(self,type):
        res_json={}
        mAd=o2oad()
        mAd=no2oadinfo().Ins()._ad
        if mAd:
            res_json['code']=200
            res_json['msg']='OK'
            res_json['list']=[]
            _action=o2oad_action()
            if type==0:
                if mAd.start_action:
                    _action=mAd.start_action
            if type==1:
                if mAd.end_action:
                    _action=mAd.end_action
            if type==-1:
                if mAd.mv_action:
                    _action=mAd.mv_action
            if type==2:
                if mAd.nosong_action:
                    _action=mAd.nosong_action
            if type==5:
                if mAd.redpack_action:
                    _action=mAd.redpack_action
            
            if _action:
                x=0
                y=0
                pos=_action.pos.split(',')
                if len(pos)==2:
                    x=pos[0]
                    y=pos[1]
                if _action.adlist:
                    data_list=_action.adlist
                    if _action.action.lower()=='random':
                        #此处需要重新排列
                        pass
                    o2o_dict=mAd
                    for item in data_list:
                        
                        adid=item
                        if o2o_dict:
                            if adid in o2o_dict.keys():
                                tv=o2o_dict[adid]
                                l_path=tv.localpath
                                l_path2=tv.localpath2
                            if tv.typestr.lower()=='gif' or tv.typestr.lower()=='image':
                                l_path=os.path.basename(tv.localpath)
                                l_path2=os.path.basename(tv.localpath2)
                            ad_data={}
#                             nAdType = tv.type,    //0:视频 1:gif 
#                             nAdVideoNextType = _action.fullplay,          //是否可以切掉
#                             nAd_ID = tv.id,                                      //  广告id
#                             nAdTime = tv.time,                                  //时间 
#                             nStartTime = _action.offset,
#                             nIntervalTime = _action.interval,                 //
#                             nListIntervalTime = _action.listinterval,         //
#                             szAdUrl = l_path,                          //本地保存目录 
#                             szAdUrl_Small = l_path2,                          //本地保存目录 
#                             nAd_X = x,                                           //坐标
#                             nAd_Y = y,
#                             szAdType = tv.typestr,    //0:视频 1:gif
                            ad_data['nAdType']=tv.type
                            ad_data['nAdVideoNextType']=_action.fullplay
                            ad_data['nAd_ID']=tv.id
                            ad_data['nAdTime']=tv.time
                            ad_data['nStartTime']=_action.offset
                            ad_data['nIntervalTime']=_action.interval
                            ad_data['nListIntervalTime']=_action.listinterval
                            ad_data['szAdUrl']=tv.l_path
                            ad_data['szAdUrl_Small']=tv.l_path2
                            ad_data['nAd_X']=x
                            ad_data['nAd_Y']=y
                            ad_data['szAdType']=tv.typestr
                        res_json['list'].append(ad_data)
        
        return res_json
    
    def pusho2oadplaytime(self,_strValue,_socketClient):
        try:
            objParam = object[4];
            pf=PublicFunc()
            pf.GetStrValue(_strValue,objParam)
            adid=objParam[0]
            time=objParam[1]
            roomip=objParam[2]
            mac=''
            adp=''
            if len(objParam)==4:
                mac=objParam[3]
            if len(objParam)==5:
                mac=objParam[3]
                adp=objParam[4]
            roomtype=""
            roomins=roomclassinfo().get_instance()
            if roomins._room_dict:
                roomtype=roomins[roomip]['room_class_name']
            edt=str(int(time.time()))
            stt=edt-(time/1000)
            if adp=="0":
                adp="no_song"
            elif adp=="1":
                adp="start"
            elif adp=="2":
                adp="end"
            else:
                adp="mv"
            
            ad_data={}
            ad_data['adid']=adid
            ad_data['roomid']=roomip.split(',')[3]
            ad_data['roominfo']=roomtype
            ad_data['cnt']=1
            ad_data['playtime']=time
            ad_data['adp']=adp
            ad_data['stt']=stt
            ad_data['edt']=edt
            ad_data['mac']=mac
            
            no2oadinfo().Ins().addplaylog(ad_data)
            self.interface.SendListToStb(_strValue, _socketClient, ad_data)
        except Exception as e:
            self.interface.SendListToStb(_strValue, _socketClient, 0)
            print(e)
    def geto2oadrplist(self,_strValue,_socketClient):
        try:
            pf=PublicFunc()
            objParam = {}
            pf.GetStrValue(_strValue,objParam)
            roomstate=objParam[0]
            res_json=self.geto2opos(roomstate)
            self.interface.SendListToStb(_strValue, _socketClient, res_json)
        except Exception as e:
            print(e)
            self.interface.SendListToStb(_strValue, _socketClient, 0)
                        
if __name__ == '__main__':
    pass