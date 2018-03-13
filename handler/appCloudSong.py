#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import json
import urllib
import logging
import traceback
import threading

from setting import TMPDIR, DOWNLOADDIR
from common.yhttp import yhttp
from common.fileutils import fileUtils
#from modules.bll.SettingBll import SettingBll
from lib.types import try_to_int
from control.mediaimport import clean_musicinfo, load_musicinfo_bysource, load_musicinfo_fromfile 
from control.configs import update_setconfig, get_all_config, get_config
from control.medias import medias_set_newsong
#from modules.bll.MediaNewSongBLL import MediaNewSongBLL
from handler.tsTask import tsServiceTask,tsTask

logger = logging.getLogger(__name__)

class _appCloudSong(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    #_interval = 10
    _lastrun = 0

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('initialize newSong singleton instance')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appCloudSong, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self, name='appCloudSong'):
        self.name = name
        self.fu = fileUtils(self.name)
        self.ktvid = None
        self.dogname = ''
        self.tempDir = os.path.join(TMPDIR, self.name)

        self._common_init(self.name)

        self.setting = get_all_config()
        self.lasttime = 0
        if 'CloudMusic_Update' in self.setting.keys():
            cfg = self.setting.get('CloudMusic_Update')
            if cfg:
                self.lasttime = try_to_int(cfg.get('config_value'), 0)

        self.cm_type = 2
        if 'CloudMusic_type' in self.setting.keys():
            cfg = self.setting.get('CloudMusic_type')
            self.cm_type = try_to_int(cfg.get('config_value'), 2)

        #self.dbhelper=Thunder().Ins().Karaokdbhelper
        self.remain = 0
        
    def do_run(self):
        self.dogname = tsServiceTask.get_dogname()
        self.ktvid = tsServiceTask.get_ktvid()
        if not self.ktvid or not self.dogname:
            self._lastmsg = "Falied to get ktvinfo."
            logger.debug(self.lastmsg)
            return False
        print ("NewSong module********************")

        #self.do_get_new_song()
        self.do_get_cloud_song()

    def do_get_new_song(self):
        try:
            self._lastmsg = '获取新歌信息'
            nos_list = self.getNewSongList(self.lasttime)
            logger.debug("new songs, list: %s" % nos_list)
            if not nos_list:
                self._lastmsg = '没有获取到新歌信息'
                if self.lastime <= int(time.time()) - 20*3600*24:
                    self.bll.ResetSort()
                return
            else:
                nlist = nos_list.split("\r\n")
                logger.debug("new song list is : %s" % nlist)
                nos = []
                for no in nlist:
                    nos.append(try_to_int(no, 0))
                if nlist and len(nlist)>0:
                    total = medias_set_newsong(nos)
                    logging.debug(u'import newsong, total %s songs' % total)
            
        except Exception as e:
            logger.error("Failed: ktvmoduleservice.updatenewsong()",e)
            logger.error(traceback.format_exc())

    def getNewSongList(self, lasttime):
        self.dogname = tsServiceTask.get_dogname()
        if not self.dogname:
            logger.debug("Falied to get dogname.")
            return False

        url = "%s/ModuleService.aspx?op=getnewsongdatabyjson&dogname=%s"\
                "&storeId=%s&time=%s" % ( self.songlist, 
                        urllib.quote(tsServiceTask.get_dogname()), 
                        str(tsServiceTask.get_ktvid()),str(lasttime))
        logger.debug(url)

        dataTypeMsg = yhttp().get_y(url)
        resdata = json.loads(dataTypeMsg)
        logger.debug("getnewsonglist: " % resdata)
        if resdata and int(resdata['code']) == 1:
            if resdata['result']:
                res = resdata['result']
                obj_items = res['matches']
                if len(obj_items) > 0:
                    item_dict = obj_items[0]
                    return yhttp().get_y(item_dict['TypeUrl'],30,ct='utf-8-sig')

        return ""

    def do_get_cloud_song(self):
        try:
            if time.time() - self.lasttime > 15 * 3600 * 24:
                return self.getCloudFile(self.ktvid, self.dogname, self.lasttime)
            else:
                return self.getCloudList(self.ktvid, self.dogname, self.lasttime)
        except Exception as ex:
            logger.error(traceback.format_exc())
            return False

    def getCloudList(self, ktvid, dogname, lasttime):
        #http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?appid=ebf0694982384de46e363e74f2c623ed&op=getsyncmusic&type=1&depot=0&size=1&time=1332171942&storeid=12
        size = 200
        remain = size
        total = -1
        url = "%s/MusicService.aspx?op=getsyncmusic&appid=%s"\
                "&type=%d&depot=0&badtype=6&size=%d&time=%d&storeid=%d" % \
                (self.kcloud_v2, self.cm_appid, self.cm_type, \
                size, self.lasttime, ktvid)
        dfile = "/tmp/cloud_music.%d.tmp" % (int(time.time()))
        
        logger.debug("call url: %s" % url)
        try:
            i = 0
            dfp = open(dfile, "w+")
            dfp.truncate(0)
            lasttime = self.lasttime
            while(i < 5000 and remain > 0):
                dataTypeMsg = yhttp().get_y(url)
                logger.debug("Get new musicinfo list, url: %s, return: %s" % (url, dataTypeMsg))
                resdata = json.loads(dataTypeMsg)
                #logger.debug("getcloudsonglist: " % resdata)
                if not resdata or int(resdata['code']) != 1:
                    break
                if resdata['result']:
                    #每次减掉请求的数量，remain会减少, 最后一次请求时remain可能成为负值。
                    remain = remain - size
                    if resdata['result']['total'] == 0:
                        break
                    if total == -1:
                        #只有第一次请求会拿到全部的数量：total
                        #后续的请求，total = size
                        total = resdata['result']['total']
                        #如果第一次拿到了真实的Total，给remain赋值，测试中可能这个total拿不到
                        remain = total - size
                    logger.debug("url: %s, get %d record of %d" % (url, size if size < resdata['result']['total'] else resdata['result']['total'], total))
                    if total > 5000:
                        logger.debug("TOOOOOOO MUCH music info to update, use full text load instead...")
                        #如果拿到的数据量超过5000,直接走全量导入
                        return self.getCloudFile(self.ktvid, self.dogname, lasttime)

                    items = resdata['result']['matches']
                    remain = total - size
                    for item in items:
                        dfp.write("replace into cloud_musicinfo(music_no, music_name, "\
                                "music_singer, music_3d1, music_3d2, music_downloadcount, music_ishd, "\
                                "music_isnew, music_isoften, music_isreplace, music_state, music_lastver, "\
                                "music_lang, music_type1, music_type2, music_status, music_lastverdate, music_unixtime) value ("\
                                "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\","
                                "\"%d\",\"%d\",\"%d\",\"%d\",\"%d\",\"%d\","
                                "\"%s\",\"%s\",\"%s\",\"%s\","
                                "\"%d\",\"%s\",\"%s\");\n" % (item['Music_No'], item['Music_Caption'], item['Music_Singer'],  item['Music_3d1'], item['Music_3d2'],
                                item['Music_DownLoadCount'], 1 if item['Music_IsHD'] else 0, 1 if item['Music_IsNew'] else 0, 
                                1 if item['Music_IsOften'] else 0, 1 if item['Music_IsReplace'] else 0, 1 if item['Music_State'] else 0, 
                                item['Music_LastVersion'], item['Music_Lname'], item['Music_Normal1'], item['Music_Normal2'], 
                                0, item['Music_LastVersionDate'], item['Music_Unixtime'])
                            )

                        if lasttime < item['Music_Unixtime']:
                            lasttime = item['Music_Unixtime']
                        i += 1
            dfp.close()
            logger.debug("get %d lines from cloud music info file, saved to file: %s" % (i, dfile))

            if i > 1:
                #load data into cloud_musicinfo, replace=True
                ret = load_musicinfo_bysource(dfile)
                if ret:
                    self.lasttime = lasttime
                    self.update_lasttime()
                    return True
                else:
                    logger.error('Failed to reload cloud_musicinfo from file: %s' % dfile)
                    return False
            else:
                logger.error('get empty cloud_musicinfo list from api: %s , all data updated' % url )
                return True
        except Exception as ex:
            logger.error(traceback.format_exc())

        finally:
            #if os.path.exists(dfile):
            #    os.remove(dfile)
            pass
        return False

    def getCloudFile(self, ktvid, dogname, lasttime):
        #kcloud.v2.service.ktvdaren.com/MusicService.aspx?appid=ebf0694982384de46e363e74f2c623ed&op=getansymusicfile&type=1&depot=0&badtype=0
        #parameter - type:  1: normal songs, 2: HD + TS(normal),  3: Leike's songs, 4: International songs
        startpath = self.kcloud_v2
        endpath = "/MusicService.aspx?"
        param = "op=getansymusicfile&appid=%s&type=%d"\
                "&depot=0&badtype=6&time=%d" % (self.cm_appid, self.cm_type, lasttime)
        
        logger.debug("call uri: %s" % startpath + endpath + param)
        dataTypeMsg = yhttp().get_y(startpath + endpath + param)
        logger.debug("uri: %s\n result:%s" % (startpath + endpath + param, dataTypeMsg))
        resdata = json.loads(dataTypeMsg)
        logger.debug("getcloudsonglist: " % resdata)
        if resdata and int(resdata['code'])==1:
            if resdata['result']:
                fname = os.path.join(TMPDIR, self.fu.filename(resdata['result']))
                if not os.path.exists(fname):
                    ret = self.fu.downfile(resdata['result'], fname, None, None)
                    if not ret:
                        logger.error("Failed to download cloud_musicinfo file")
                        return False
                if self.loadCloudMusic_All(fname):
                    #if os.path.exists(fname):
                    #    os.remove(fname)
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
                dfp.write("\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t"
                        "\"%d\"\t\"%d\"\t\"%d\"\t\"%d\"\t\"%d\"\t\"%d\"\t"
                        "\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t"
                        "\"%d\"\t\"%s\"\t\"%s\"\n" % (arr[10], arr[16], arr[17], arr[1], arr[2],
                            1 if arr[3]=='True' else 0, 1 if arr[4]=='True' else 0, 1 if arr[5]=='True' else 0, 
                            1 if arr[6]=='True' else 0, 1 if arr[7]=='True' else 0, 1 if arr[13]=='True' else 0,
                            arr[8], arr[9], arr[11], arr[12],
                            0, arr[15], arr[14])
                        )
                i += 1
            dfp.close()
            logger.debug("get %d lines from cloud music info file, saved to file: %s" % (i, dfile))

            #delete all from cloud_musicinfo
            #load data into cloud_musicinfo
            clean_musicinfo()
            ret = load_musicinfo_fromfile(dfile)
            if ret:
                self.lasttime = int(time.time())
                self.update_lasttime()
                return True
            else:
                logger.error('Failed to reload cloud_musicinfo from file: %s' % dfile)

        except Exception as ex:
            logger.error(traceback.format_exc())

        finally:
            #if os.path.exists(dfile):
            #    os.remove(dfile)
            pass
        return False

    def update_lasttime(self):
        return update_setconfig(dict(CloudMusic_Update=str(self.lasttime)))

appCloudSong = _appCloudSong()

