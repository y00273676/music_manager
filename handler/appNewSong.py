#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import json
import shutil
import urllib
import logging
import datetime
import traceback
import threading

from setting import TMPDIR, DOWNLOADDIR
from common.yhttp import yhttp
from common.fileutils import fileUtils
from common.ZFile import extract
#from modules.bll.SettingBll import SettingBll
from lib.types import try_to_int
from control.configs import update_setconfig, get_all_config, get_config
from control.medias import medias_set_newsong
#from modules.bll.MediaNewSongBLL import MediaNewSongBLL
from handler.tsTask import tsServiceTask,tsTask
from control.mediaimport import loadCloudMusic_fromfile
from control.cloudmusic import get_musicinfo_bylist

logger = logging.getLogger(__name__)

class _appNewSong(tsTask):
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
                    cls.__instance = super(_appNewSong, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self, name='appNewSong'):
        self.name = name
        self.fu = fileUtils(self.name)
        self.ktvid = None
        self.dogname = ''
        self.tempDir = os.path.join(TMPDIR, self.name)
        self.downDir = os.path.join(DOWNLOADDIR, self.name)
        if not os.path.exists(self.downDir):
            os.makedirs(self.downDir)

        self._common_init(self.name)

        self.setting = get_all_config()
        self.lasttime = 0
        if 'NewSong_Update' in self.setting.keys():
            cfg = self.setting.get('NewSong_Update')
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
        self.do_get_empty_record()

    def do_get_new_song(self):
        try:
            cfg = get_config('cloudmusic_update')
            if cfg:
                self.lasttime = try_to_int(cfg.get('config_value'), 0)
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

    def getNewSongList(self,lasttime):
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

    def do_get_empty_record(self, size=100):
        try:
            if time.time() - self.lasttime > 15 * 3600 * 24:
                return self.getAllRecords(self.ktvid, self.dogname, self.lasttime)
            else:
                self.getRecords_byDay(self.lasttime)
        except Exception as ex:
            logger.error(traceback.format_exc())
            return False

    def getRecords_byDay(self, lasttime):
        now = int(time.time())
        today = time.strftime('%Y-%m-%d', time.localtime() )
        lastday = time.strftime('%Y-%m-%d', time.localtime(lasttime) )
        print(today, lastday)
        if lastday == today or lasttime > now:
            logger.info("already pull empty record for today")
            return True

        day = time.strftime('%Y-%m-%d', time.localtime(lasttime + 3600*24) )
        #http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?op=getpushmusiclist&time=2017-11-06&type=2&ismp3=0
        url = "%s/MusicService.aspx?op=getpushmusiclist&time=%s&type=2&ismp3=0"\
                % (self.kcloud_v2, day)
        try:
            dfile = os.path.join(TMPDIR, "medias_record.%s.tmp.%d" % (day, int(time.time())))
            dataTypeMsg = yhttp().get_y(url)
            logger.debug("uri: %s\n result:%s" % (url, dataTypeMsg))
            resdata = json.loads(dataTypeMsg)
            logger.debug("getcloudsonglist: " % resdata)
            i = 0
            j = 0
            if not resdata or int(resdata['code'])!=1:
                logger.error('Failed to get cloud_musicinfo from api: %s' % url)
                return False
            if resdata['result']:
                dfp = open(dfile, "w+")
                total = resdata['result']['total']
                items = resdata['result']['matches']
                result = []
                while(total - i > 0):
                    res = get_musicinfo_bylist(items[i:i+30])
                    if res:
                        result += res
                    i += 30

                    #字段详情：
                    #   1      2    3     4   5        6       7      8     9   10    11   12    13    14     15     16     17         18      19     20       21    22   23
                    #编号|歌曲名称|简拼|全拼|语言|歌曲格式|歌曲音频|音量|版本号|笔划|笔画|新歌|中文发|高清|语言类型|左声道|右声道|歌曲视频|替换内容|歌曲主题|3D主题|歌星|授权值
                    #4000072|空姐之歌|KJZG|kong_jie_zhi_ge|国语|DVD|MPEG|6|37.8|8|4541|0|0|0|0|2|1|2||流行歌曲|影视金曲|116122,佚名,大陆男歌星,YM,yi_ming|0
                    #   1      2        3           4       5    6   7   8  9   10  11 12          18    20       21      22                              23
                    #4100007|一帘好梦|YLHM|yi_lian_hao_meng|国语|DVD|MPEG|6|0|1|1451|0|0|0|0|2|1|2||流行歌曲|寂寞空灵|117395,胡云鹏,大陆男歌星,HYP,hu_yun_peng|0


                for item in result:
                    dfp.write("%s|%s|%s|%s|%s|"\
                            "%s|%s|%s|%s|%s|%s|"\
                            "%s|%s|%s|%s|%s|"\
                            "%s|%s|%s|%s|%s|"\
                            "%s|%s\n"\
                            % (item['Music_No'], item['Music_Caption'], item['Music_JianPin'], item['Music_PinYin'], item['Music_Language'],
                                item['Music_VideoFormat'], item['Music_AudioFormat'], item['Music_Volume'], 37.8, item['Music_Stroke'], item['Music_Bihua'],
                                1 if item['Music_IsNew'] else 0, 0, 1 if item['Music_IsHD'] else 0, item['Music_LanguageType'], item['Music_ZTrack'],
                                item['Music_YTrack'], item['Music_VideoType'], '', ','.join([item['Music_Normal1'], item['Music_Normal2']]).strip(','), \
                                        ','.join([item['Music_3d1'], item['Music_3d2']]).strip(','),
                                ';'.join(["%s,%s,%s,%s,%s" % (act['Singer_Id'],act['Singer_Name'],act['Singer_TypeName'],act['Singer_JianPin'],act['Singer_PinYin']) for act in item['Singers'] ]) if item['Singers'] else '', 0))
                    j += 1
                dfp.close()
                logger.debug("get %d lines from cloud music info file, saved to file: %s" % (j, dfile))

                if i < 1:
                    return True

                if loadCloudMusic_fromfile(dfile):
                    d = datetime.datetime.strptime('%s 23:59:59' % today, '%Y-%m-%d %H:%M:%S')
                    t = time.mktime(d.timetuple())
                    self.lasttime = int(t)
                    self.update_lasttime()
                    return True
                else:
                    logger.error('Failed to load cloud_musicinfo from file: %s' % dfile)
                    return False
            else:
                logger.info('get empty cloud_musicinfo from api: %s' % url)
                return False
        except Exception as ex:
            logger.error(traceback.format_exc())

        finally:
            '''
            if os.path.exists(dfile):
                os.remove(dfile)
            '''
            pass
        return False

    def getAllRecords(self, ktvid, dogname, lasttime):
        #http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?op=getallmusicfile&depot=0&musictype=7&linkzip=1
        url = "%s/MusicService.aspx?op=getallmusicfile&depot=0&musictype=7&linkzip=1" % self.kcloud_v2
        res = yhttp().get_y(url)
        logger.debug("call url: %s, result: %s" % (url, res))
        resdata = json.loads(res)
        if resdata and int(resdata['code'])==1:
            if resdata['result']:
                fname = os.path.join(self.downDir, self.fu.filename(resdata['result']))
                if not os.path.exists(fname):
                    ret = self.fu.downfile(resdata['result'], fname, None, None)
                    if not ret:
                        logger.error("Failed to download cloud_musicinfo file")
                        return False
                #extra
                txtname, _ = os.path.splitext(fname)
                extra_fname = '%s.txt' % os.path.join(self.downDir, txtname)
                if extract(fname, self.downDir):
                    pass
                else:
                    #if failed to extra, delete the zip file to download again
                    if os.path.exists(fname):
                        os.remove(fname)
                    if os.path.exists(extra_fname):
                        os.remove(extra_fname)
                logger.error("TODO: load music info into medias table......")

                if loadCloudMusic_fromfile(extra_fname):
                    if os.path.exists(fname):
                        os.remove(fname)
                    if os.path.exists(extra_fname):
                        os.remove(extra_fname)
                    self.lasttime = int(time.time())
                    self.update_lasttime()
                    return True
                else:
                    logger.error("Failed to load cloud_musicinfo file, fullfile update")
                    return False
        else:
            logger.error("Failed to get cloud_musicinfo from api")

        return False

    def update_lasttime(self):
        return update_setconfig(dict(NewSong_Update=str(self.lasttime)))

appNewSong = _appNewSong()

