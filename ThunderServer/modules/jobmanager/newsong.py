#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月6日
检测新歌
@author: yeyinlin
'''
import os
import json
from config.appConfig import AppSet
from common.yhttp import yhttp
from common.fileutils import fileUtils
from common.KtvInfo import hdl_ktvinfo
from modules.bll.SettingBll import SettingBll
from common.tstypes import try_to_int

from modules.bll.MediaNewSongBLL import MediaNewSongBLL
import time
import traceback
from common.Thunder import Thunder

import logging
logger = logging.getLogger(__name__)

class newsong(object):
    def __init__(self):
        self.lastime=int(time.time()) - 20*3600*24
        self.bll = MediaNewSongBLL()
        self.fu = fileUtils('cloudmusic')
        self.ktvid = None
        self.dogname = AppSet().get_DogName()

        self.setting = SettingBll()
        self.lasttime = try_to_int(self.setting.GetSettingInfo('CloudMusic_Update'), 0)
        self.cm_type = self.setting.GetSettingInfo('CloudMusic_type')
        if not self.lasttime:
            self.lasttime = 0
        if not self.cm_type:
            self.cm_type = 2
        else:
            self.cm_type = try_to_int(self.cm_type, 1)
        self.dbhelper=Thunder().Ins().Karaokdbhelper
        self.remain = 0
        
    def start(self,name):
        return True
    
    def updatenewsong(self):
        try:
            nos_list=self.getnewsonglist(self.lastime,0,1)
            logger.debug("new songs, list: %s" % nos_list)
            if not nos_list:
                if self.lastime <= int(time.time()) - 20*3600*24:
                    self.bll.ResetSort()
                return
            else:
                ytime=self.bll.GetSongValidtime()
                nlist=nos_list.split("\r\n")
                logger.debug("new song list is : %s" % nlist)
                if nlist and len(nlist)>0:
                    #状态重置     
                    self.bll.ResetSort()
                    no=1
                    for item in nlist:
                        #获取对应歌曲的编号
                        if int(item)>0:
                            media_ID=self.bll.GetMediaIdbySerialNo(item)
                            if media_ID>0:
                                self.bll.insertMediaNewsong(media_ID, ytime, no)
                                no=no+1
                            self.lastime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                            logging.debug(u'新歌导入完成')
            
        except Exception as e:
            logger.error("Failed: ktvmoduleservice.updatenewsong()",e)
            logger.error(traceback.format_exc())

    def getnewsonglist(self,lasttime,dogname,ktvid):
        startpath=AppSet().songlist
        endpath="/ModuleService.aspx?"
        param="op=getnewsongdatabyjson&dogname=" + yhttp().UrlEncode(str(AppSet()._dogname))+"&storeId="+str(ktvid)+"&time="+str(lasttime)
        print(startpath + endpath + param)
        dataTypeMsg=yhttp().get_y(startpath + endpath + param)
        resdata=json.loads(dataTypeMsg)
        logger.debug("getnewsonglist: " % resdata)
        if resdata and int(resdata['code'])==1:
            if resdata['result']:
                res=resdata['result']
                obj_items=res['matches']
                if len(obj_items)>0:
                    item_dict=obj_items[0]
                    return yhttp().get_y(item_dict['TypeUrl'],30,ct='utf-8-sig')

        return ""

    def getCloudSong(self, size=100):
        if not self.ktvid:
            ktvinfo = hdl_ktvinfo.get_ktvinfo()
            if ktvinfo:
                self.ktvid = ktvinfo.ktvid
            else:
                logger.debug("Falied to get ktvid.")
                return False

        if not self.dogname:
            logger.debug("Falied to get dogname.")
            return False

        try:
            if time.time() - self.lasttime > 15 * 3600 * 24:
                return self.getCloudFile(self.ktvid, self.dogname, self.lasttime)
            else:
                remain = 1
                while(remain > 0):
                    remain = self.getCloudList(self.ktvid, self.lasttime, size)
        except Exception as ex:
            logger.error(traceback.format_exc())
            return False

    def getCloudList(self, ktvid, lasttime, size):
        #http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?appid=ebf0694982384de46e363e74f2c623ed&op=getsyncmusic&type=1&depot=0&size=1&time=1332171942&storeid=12
        remain = -1
        startpath = AppSet().kcloud_v2
        endpath = "/MusicService.aspx?"
        param = "op=getsyncmusic&appid=%s&type=%d&depot=0&badtype=6&size=%d&time=%d&storeid=%d" % \
                (AppSet().cm_appid, self.cm_type, size, self.lasttime, ktvid)
        
        logger.debug("call uri: %s" % startpath + endpath + param)
        try:
            dfile = "/tmp/cloud_music.%d.tmp" % (int(time.time()))
            dataTypeMsg = yhttp().get_y(startpath + endpath + param)
            logger.debug("uri: %s\n result:%s" % (startpath + endpath + param, dataTypeMsg))
            resdata = json.loads(dataTypeMsg)
            logger.debug("getcloudsonglist: " % resdata)
            i = 0
            if resdata and int(resdata['code'])==1:
                dfp = open(dfile, "w+")
                if resdata['result']:
                    total = resdata['result']['total']
                    items = resdata['result']['matches']
                    remain = total - size
                    for item in items:
                        dfp.write("%s\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t"
                                "%d\t%d\t%d\t%d\t%d\t%d\t"
                                "\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t"
                                "%d\t\"%s\"\t%s\n" % (item['Music_No'], item['Music_Caption'], item['Music_Singer'],  item['Music_3d1'], item['Music_3d2'],
                                item['Music_DownLoadCount'], 1 if item['Music_IsHD'] else 0, 1 if item['Music_IsNew'] else 0, 
                                1 if item['Music_IsOften'] else 0, 1 if item['Music_IsReplace'] else 0, 1 if item['Music_State'] else 0, 
                                item['Music_LastVersion'], item['Music_Lname'], item['Music_Normal1'], item['Music_Normal2'], 
                                0, item['Music_LastVersionDate'], item['Music_Unixtime'])
                            )
                        self.lasttime =  item['Music_Unixtime']
                        i += 1
                dfp.close()
                logger.debug("get %d lines from cloud music info file, saved to file: %s" % (i, dfile))

                if i > 1:
                    #delete all from cloud_musicinfo
                    #load data into cloud_musicinfo
                    ret = self.load_musicinfo_fromfile(dfile)
                    if ret:
                        #os.remove(dfile)
                        self.update_lasttime()
                        return remain
                    else:
                        logger.error('Failed to reload cloud_musicinfo from file: %s' % dfile)
                else:
                    logger.error('get empty cloud_musicinfo list from api: %s , all data updated' % (startpath + endpath + param) )
                    return remain
            else:
                logger.error('Failed to get cloud_musicinfo from api: %s' % (startpath + endpath + param) )
                return remain

        except Exception as ex:
            logger.error(traceback.format_exc())

        finally:
            if os.path.exists(dfile):
                os.remove(dfile)
                pass
        return remain

        return False

    def getCloudFile(self, ktvid, dogname, lasttime):
        #kcloud.v2.service.ktvdaren.com/MusicService.aspx?appid=ebf0694982384de46e363e74f2c623ed&op=getansymusicfile&type=1&depot=0&badtype=0
        #parameter - type:  1: normal songs, 2: HD + TS(normal),  3: Leike's songs, 4: International songs
        startpath = AppSet().kcloud_v2
        endpath = "/MusicService.aspx?"
        param = "op=getansymusicfile&appid=%s&type=%d"\
                "&depot=0&badtype=6&time=%d" % (AppSet().cm_appid, self.cm_type, lasttime)
        
        logger.debug("call uri: %s" % startpath + endpath + param)
        dataTypeMsg = yhttp().get_y(startpath + endpath + param)
        logger.debug("uri: %s\n result:%s" % (startpath + endpath + param, dataTypeMsg))
        resdata = json.loads(dataTypeMsg)
        logger.debug("getcloudsonglist: " % resdata)
        if resdata and int(resdata['code'])==1:
            if resdata['result']:
                fname = os.path.join(AppSet().get_CloudKtvTemp(), self.fu.filename(resdata['result']))
                if not os.path.exists(fname):
                    ret = self.fu.downfile(resdata['result'], fname, None, None)
                    if not ret:
                        logger.error("Failed to download cloud_musicinfo file")
                        return False
                if self.loadCloudMusic_All(fname):
                    if os.path.exists(fname):
                        os.remove(fname)
                    return True
                else:
                    logger.error("Failed to load cloud_musicinfo file")
                    return False
        else:
            logger.error("Failed to get cloud_musicinfo from api")

        return False

    def loadCloudMusic_All(self, fname):
        if not os.path.exists(fname):
            return False
        try:
            dfile = "%s.%d" % (fname, int(time.time()))
            dfp = open(dfile, "w+")
            i = 0
            for line in open(fname):
                arr = line.strip().split('|')
                if len(arr) < 18:
                    continue
                #19222|心碎伤感||8|False|False|False|False|22.5|粤语|7420228|流行歌曲||True|1332169506|2012-03-19 15:05:05|新闻女郎|陈奕迅
                #线上编号|3d分类1|3d分类2|下载量|是否高清|是否新歌|是否常唱|是否替换|版本号|语言|歌曲编号|普通分类1|普通分类2|是否使用|更新时间戳|更新时间|歌曲名称|歌星
                dfp.write("%s\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t"
                        "%d\t%d\t%d\t%d\t%d\t%d\t"
                        "\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t"
                        "%d\t\"%s\"\t%s\n" % (arr[10], arr[16], arr[17], arr[1], arr[2],
                            1 if arr[3]=='True' else 0, 1 if arr[4]=='True' else 0, 1 if arr[5]=='True' else 0, 1 if arr[6]=='True' else 0, 1 if arr[7]=='True' else 0, 1 if arr[13]=='True' else 0,
                            arr[8], arr[9], arr[11], arr[12],
                            0, arr[15], arr[14])
                        )
                if i == 0:
                    self.lasttime = int(arr[14])
                i += 1
            dfp.close()
            logger.debug("get %d lines from cloud music info file, saved to file: %s" % (i, dfile))

            if i > 1000:
                #delete all from cloud_musicinfo
                #load data into cloud_musicinfo
                if self.clean_musicinfo():
                    ret = self.load_musicinfo_fromfile(dfile)
                    if ret:
                        #os.remove(dfile)
                        self.update_lasttime()
                        return True
                    else:
                        logger.error('Failed to reload cloud_musicinfo from file: %s' % dfile)

        except Exception as ex:
            logger.error(traceback.format_exc())

        finally:
            if os.path.exists(dfile):
                os.remove(dfile)
        return False

    def clean_musicinfo(self):
        try:
            sql = "delete from cloud_musicinfo"
            ret = self.dbhelper.ExecuteSql(sql)
            logger.debug("delete from cloud_musicinfo, return: %s" % ret)
            return ret
        except Exception as e:
            logger.error(traceback.format_exc())
        return False

    def load_musicinfo_fromfile(self, fname):
        try:
            #FIXME: remember to send the file to the machine which mysql runs on, at first!
            sql = "load data low_priority infile '%s' replace into table cloud_musicinfo character set utf8 fields terminated by '\\t' enclosed by '\"'" % (fname)
            ret = self.dbhelper.ExecuteSql(sql)
            logger.debug("load data into cloud_musicinfo, return: %s" % ret)
            return ret
        except Exception as e:
            logger.error(traceback.format_exc())
        return False

    def update_musicinfo_fromfile(self, fname):
        try:
            sql = "source %s" % (fname)
            ret = self.dbhelper.ExecuteSql(sql)
            logger.debug("update data into cloud_musicinfo, return: %s" % ret)
            return ret
        except Exception as e:
            logger.error(traceback.format_exc())
        return False


    def update_lasttime(self):
        self.lasttime = int(time.time())
        return self.setting.SetSettingInfo('CloudMusic_Update', str(self.lasttime))

if __name__ == '__main__':
    song=newsong()
    song.updatenewsong()
