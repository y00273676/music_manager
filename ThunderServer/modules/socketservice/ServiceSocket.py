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

import socketserver
import redis

sys.path.append("..")
from mylogger import MyLogger
from common.KtvInfo import KtvInfo
from jobmanager import *

logger=MyLogger('ServiceSocket')

"""
class o2oupload(Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.queque={}
        self.stopped = False
	
    def add(self, data):
        try:
            if isinstance(data,list):
                for item in data:
                    self.addsingle(item)
                
            else:
                self.addsingle(data)
        except:
            traceback.print_exc()
    def run(self):
        print("thread start")
        lastick = time.time()
        ntick = 0
        while not self.stopped:
            


    #add queue
    #upload
    List<Parameter> param = new List<Parameter>{
                new Parameter("ad_id",adid),
                new Parameter("ktv_id",KtvInfo.ktvid),
                new Parameter("room_id",roomid),
                new Parameter("room_info",roominfo),
                new Parameter("cnt",cnt),
                new Parameter("time",playtime),
                new Parameter("stt",stime),
                new Parameter("edt",etime),
                new Parameter("adp",adp),
                new Parameter("mac",mac)
            };
            ClassLoger.Info("Ktv_Tvadinfoapi.o2oplaystat", HttpUtils.Ins.ParamSign(param));
            string json_str = HttpUtils.Ins.GET(url, HttpUtils.Ins.ParamSign(param));
            Dictionary<string, object> res_dict = JsonHelper.DeserializeObject(json_str);
            if (res_dict != null && res_dict.Keys.Contains("errcode"))
            {
                return res_dict["errcode"].TryToInt();
            }
            return 0;
"""

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        rdb = redis.Redis();
        data = self.request.recv(1024)
        try:
            buffer = data.decode()
        except:
            buffer = ''
        bytes = None;
        inx = buffer.find(' ')
        if inx>0:
            rt = 0;
            action = buffer[0:inx]
            content = buffer[inx+1:]
            #print('content', content);
            values = self.getObjects(content)
            now = time.strftime("%Y-%m-%d", time.localtime());

            if action.startswith('Test')==True:
                pass;
            elif action.startswith('INTEL_GETDEVICEINFO')==True:
                INTEL_GETDEVICEINFO(values,self)
                pass;
            elif action.startswith('INTEL_GETROOMDEBUGINFO')==True:
                INTEL_GETROOMDEBUGINFO(values,self)
                pass;
            elif action.startswith('INTEL_GETROOMPLANLIST')==True:
                INTEL_GETROOMPLANLIST(values,self)
                pass;
            elif action.startswith('INTEL_GETDEVICEPUBLICPLAN')==True:
                INTEL_GETDEVICEPUBLICPLAN(values,self)
                pass;
            elif action.startswith('INTEL_GETPLANUSEKTVLIST')==True:
                INTEL_GETPLANUSEKTVLIST(values,self)
                pass;
            elif action.startswith('INTEL_GETROOMMODEL')==True:
                INTEL_GETROOMMODEL(values,self)
                pass;
            elif action.startswith('INTEL_DELROOMPLANINFO')==True:
                INTEL_DELROOMPLANINFO(values,self)
                pass;
            elif action.startswith('INTEL_SAVEROOMDEVICETIME')==True:
                INTEL_SAVEROOMDEVICETIME(values,self)
                pass;
            elif action.startswith('INTEL_SAVEROOMPLANINFO')==True:
                INTEL_SAVEROOMPLANINFO(values,self)
                pass;
            elif action.startswith('INTEL_GETCITYLIST')==True:
                INTEL_GETCITYLIST(values,self)
                pass;
            elif action.startswith('INTEL_GETFILEURL')==True:
                INTEL_GETFILEURL(values,self)
                pass;
            elif action == 'SaveOperateData':
                #ShowCount：展示次数
                #ModuleClickCount：模块点击次数
                #ModuleType：模块类型
                #ModuleID：模块ID
                #ModuleName：模块名称
                #RoomIP：房间IP
                print('----------------SaveOperateData'); 
                try:
                    
                    showcount =int(values[0]);
                    moduleclickcount = int(values[1]);
                    moduletype = int(values[2]);
                    moduleid = int(values[3]);
                    modulename = values[4];
                    roomip = values[5];
                    skintype = int(values[6]);
                    
                    result = {}
                    result['showcount'] = showcount;
                    result['moduleclickcount'] = moduleclickcount;
                    result['moduletype'] = moduletype;
                    result['moduleid'] = moduleid;
                    result['modulename'] = modulename;
                    result['roomip'] = roomip;
                    result['skintype']= skintype;
                    
                    r = json.dumps(result);

                    md5sum = hashlib.md5(r.encode()).hexdigest()
                    view_key = 'view:' + md5sum;
                    click_key = 'click:' + md5sum;
                    page_key = 'page:'+ now;
                    
                    rdb.set(page_key, result);
                    rdb.expire(page_key, 24*60*60);
                    
                    showcount += showcount;
                    moduleclickcount += moduleclickcount;
                    
                    if not rdb.exists(view_key):
                        if rdb.lpush(page_key, page_value) > 0:
                            rdb.expire(page_key, expire_time);
                    
                    if rdb.zincrby(view_key, "page", showcount):
                        rdb.expire(view_key, 60*12*12);
                    if rdb.zincrby(click_key, "click", moduleclickcount):
                        rdb.expire(click_key, expire_time);
                    
                    expire_time = 60*12*12;
                    if not rdb.exists(view_key):
                        if rdb.lpush(page_key, page_value) > 0:
                            rdb.expire(page_key, expire_time);

                    if rdb.zincrby(view_key, 'page', showcount):
                        rdb.expire(view_key, expire_time);

                    if rdb.zincrby(click_key, "click", moduleclickcount):
                        rdb.expire(click_key, expire_time);

                    rt = 1;
                except:
                    logger.dolog('SaveOperateData', True);
            elif action.startswith('SaveSongData'):
                #SerialNo：	歌曲编号
                #MediaName：	歌曲名称
                #Count：	 点歌次数
                #ModuleType：模块类型
                #ModuleName：模块名称
                #AppID：	 应用ID(触摸屏点歌为空)
                #SearchID：	搜索方式ID（搜霸搜索:1 拼音搜索:2 手写搜索:4 笔划搜索:8 语言搜索:16 字数搜索:32 歌星搜索:64），如果没有搜索为0
                #RoomIP：	 房间IP
                
                obj = self.getObjects(content)
                serilno = obj[0];
                medianame = obj[1];
                count =int(obj[2]);
                moduletype = int(obj[3]);
                modulename = obj[4];
                appid = obj[5];
                searchid = int(obj[6]);
                roomip = obj[7];
                skintype = int(obj[8]);
                self.request.sendall(rt)

                #点歌入口统计
                song = {}
                song['room_ip'] = roomip;
                song['search_type'] = searchid;
                song['entry_name'] = modulename;
                song['entry_type'] = moduletype;
                song['vod_no'] = count;
                song['room_name'] = '';
                song['ktv_id'] = 0;
                song['ktv_name'] = '';
                song['skintype'] = skintype;
                
                md5sum = hashlib.md5(moduletype + '_' + searchid + '_' + roomip + '_' + modulename).hexdigest()
                
                key = 'entry_' + md5sum;
                entry_key = 'entry:'+ now;
                if rdb.zincrby(entry_key, key, 1):
                    rdb.expire(entry_key, expire_time);
                if rdb.set(key, json.dump(song)):
                    rdb.expire(entry_key, expire_time);
                #歌曲点唱排行
                vod = {}
                vod['song_name'] = medianame;
                vod['appid'] = appid;
                vod['room_ip'] = roomip;
                vod['song_id'] = int(serilno);
                vod['vod_time'] = time.time();

                vod_key = 'vod:' + day;
                if rdb.lpush(vod_key, json.dump(vod)) > 0:
                    rdb.expire(vod_key, expire_time);

                if rdb.zincrby('usr_action',('action_' + roomip), 1):
                    rdb.expire(entry_key, expire_time);
                 
                _self.request.sendall(1)
            elif action.startswith('STBPAPERPLAYTIME'):
                """
                filemd5 = obj[0];
                bagtype = int(obj[3]);
                roomIp = obj[1];
                #0开台，1未开台
                roomstatus = int(obj[2]);
                string mac = "";//mac地址
                if len(obj)>4:
                    mac = obj[4];
                else:
                    mac = '';
                
                _socketClient.Sock.Send(PublicFunc.IntToIntPtr(1), 4, SocketFlags.None);
                
                key = '';
                int adid = 0;
                if bagtype == 0:
                    adp = 'horizon_lock_screen';
                else: 
                    adp = 'verticle_lock_screen';

                roomtype = '';
                time = 0;

                Dictionary<string, WallpaperInfo> dict = Wallpapers.Ins.wall_dict;
                if (dict.Keys.Contains(filemd5))
                {
                    adid = dict[filemd5].paper_id;
                }
                if (roomclassinfo.Ins.room_dict != null && roomclassinfo.Ins.room_dict.Keys.Contains(roomIp))
                    roomtype = roomclassinfo.Ins.room_dict[roomIp].room_className;
                long edt = Utils.GetUnixTime();
                long stt = edt - (time / 1000);
                ClassLoger.DEBUG("SaveStbWallpaperPlayTime", string.Format("广告:{0},房间:{1},时长:{2},位置:{3},开始:{4},结束:{5},MAC:{6}", adid.ToStr(), roomIp, time.ToStr(), adp, stt.ToStr(), edt.ToStr(), mac));
                ad_data = {}
                ad_data['adid'] = adid;
                ad_data['roomid'] = roomIp.Split('.')[3].TryToInt(0),
                ad_data['roominfo'] = roomtype;
                ad_data['cnt'] = 1;
                ad_data['playtime'] = time.time();
                ad_data['adp'] = adp;
                ad_data['stt'] = stt;
                ad_data['edt'] = edt;
                ad_data['mac'] = mac;
                
                o2o_adinfo.Ins.addplaylog(ad_data);#ADD TO QUEUE
                """
                pass
            elif action.startswith('GetThunderServiceServerState'):
                #GetThunderServiceServerState State:1 Ver:0 \r\n\r\n
                state = obj[0];#类型  1：获取轮播图片
                t = obj[1];#0 横版  1：竖版 
                if state == '1':
                    type = 1;
                    
                    wps = Wallpapers();
                    if wps.meta.has_key('use_looppic') or meta['use_looppic'] == 2:
                        type = 0;
                    else:
                        if t=='0' and (wps.getHStatus()==2 or len(wps.getHPapers())<1):
                            rt = 0;
                        elif t=='1' and (wps.getVStatus()==2 or len(wps.getVPapers())<1):
                            rt = 0;
                    bytes = struct.pack('i', type);
            elif action.startswith('GETNEWMODULELIST'):
                """
                ip = obj[0];
                bagtype = int(obj[1]);
                _isnew = int(obj[2]);
                int count = 0;
                MemoryStream ms = new MemoryStream();
                if (ktv_moduleonline.Ins.OnlineDict != null && ktv_moduleonline.Ins.OnlineDict.Keys.Contains(bagtype))
                {
                    List<onlinemodule> m_list = ktv_moduleonline.Ins.OnlineDict[bagtype];
                    foreach (var on_item in m_list)
                    {
                        if (_isnew == 0 && on_item.module_type != 27):
                            print('continue 1');
                        else:
                            item = {}
                            item['module_id'] = on_item.module_id;
                            item['module_name'] = on_item.module_name;
                            item['module_pic'] = on_item.module_pic;
                            item['module_bgpic'] = on_item.module_bgpic;
                            item['module_dataid'] = on_item.module_dataid;
                            item['module_datatype'] = on_item.module_datatype;
                            item['module_position'] = on_item.module_position;
                            item['module_type'] = on_item.module_type;
                        
                            if (item['module_type'] == 27 and item['module_datatype'] == 1 and on_item['module_movietype'] >= 2):
                                print('continue 2');
                            else:
                                item['module_pic'] = DownUtil.GetFilePath(item['module_pic'], true);
                                item['module_bgpic'] = DownUtil.GetFilePath(item['module_bgpic'], true);
                                byte[] tinfo = PublicFunc.StructToBytes(item);
                                if (tinfo != null)
                                {
                                    ms.Write(tinfo, 0, tinfo.Length);
                                    count++;
                                }
                            }
                
                _socketClient.Sock.Send(PublicFunc.IntToIntPtr(count), 4, SocketFlags.None);
                if (count > 0)
                {
                    byte[] data = ms.ToArray();
                    ms.Close();
                    ms.Dispose();
                    _socketClient.Sock.Send(data, 0, data.Length, SocketFlags.None);
                }
                """
                pass
            elif action.startswith('GETNEWMODULELIST_NewVersion'):
                pass
            elif action.startswith('STBTVADINFOLIST'):
                pass
            elif action.startswith('GETTVADININTERVAL'):
                pass
            elif action.startswith('STBTVADSHOWTIME'):
                pass
            elif action.startswith('GetADVideoList'):
                pass
            elif action.startswith('GetADGifList'):
                pass
            elif action.startswith('GetADCaptionInfo'):
                pass
            elif action.startswith('SaveOnlieAdData'):
                pass
            elif action.startswith('GetUniversalAdList'):
                pass
            else:
                pass

        #a='hello';
        #b='world!';
        #c=2;
        #d=45.123;
        #bytes=struct.pack('64s6sif',a.encode(),b.encode(),c,d);
        if bytes==None:
            bytes = struct.pack('i', 0);

        self.request.sendall(bytes)

    def getObjects(self, str):
        values = [];
        units = str.split(' ');
        for unit in units:
            unit = unit.strip();
            kv = unit.split(':');
            #print('------', kv);
            if len(kv)==1:
                v = kv[0].strip();
            else:
                v = kv[1].strip();
            if v!='':
                values.append(v);

        print('getObjects', str);
        print('---', values);
        return values;

    def stop(self):
        Flag = False
    
        
if __name__ == '__main__':
#     a='hello';
#     b='world!';
#     c=2;
#     d=45.123;
#     bytes=struct.pack('64s6sif',a.encode(),b.encode(),c,d);
#     print(bytes)
    
    
#     ips = socket.gethostbyname_ex(socket.gethostname())[-1]
#     ipo=''
#     for a in os.popen('route print').readlines():
#         if ' 0.0.0.0 ' in a:
#             ipo=a.split()[3]
#             break
#     for ip in ips:
#         if ip != ipo:
#             break;
#     
#     print('network ', ips, ip)
    try:
        server = socketserver.ThreadingTCPServer(('0.0.0.0', 11208),MyServer)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupted!")
        server.shutdown()
        server.server_close()
        logger.dolog('shutdown ....')
        logger.close()
        sys.exit(0)
