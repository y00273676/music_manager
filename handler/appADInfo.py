#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging
import platform
import traceback
import threading

from common.utils import md5
from common.fileutils import fileUtils
from lib.http import request_json

from handler.tsTask import tsServiceTask,tsTask
from setting import TMPDIR, DOWNLOADDIR, HTDOCDIR

logger = logging.getLogger(__name__)

class _appADInfo(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('_appADInfo singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appADInfo, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('_appADInfo singleton is exists')
        return cls.__instance

    def __init__(self, name = 'appADInfo'):
        self.name = name
        self._common_init(self.name)
        #文件下载的地址
        self._localsavepath = os.path.join(DOWNLOADDIR, self.name)
        if not os.path.exists(self._localsavepath):
            os.mkdir(self._localsavepath)
        #o2o 下载广告的地址
        self._localdatapath = os.path.join(HTDOCDIR, "data", "o2o")

        #验证文件夹是否存在
        if not os.path.exists(self._localdatapath):
            os.makedirs(self._localdatapath)
        #广告的地址
        self.ad_data = os.path.join(self._localdatapath, "ad.json")
        self.ad_del = os.path.join(self._localdatapath, "ad_del.json")

        self.fu = fileUtils(self.name)
        self._down_dict = {}

        self.server_localpath = "/opt/thunder/ktvservice/ktv_o2oadinfo"
        if not os.path.exists(self.server_localpath):
            os.makedirs(self.server_localpath)

        self.res_adcaption = None

    #获取字幕
    def geto2oadcaption(self):
        url = '%s/ad/caption/%s' % (AppSet().O2OAPI, tsServiceTask.get_ktvid())
        #url = "http://api.stage.ktvsky.com/ad/caption/1";
        jsonres = request_json(url, timeout=10, method='GET')
        logger.debug("get o2o ad caption, url:%s result: %s" % ( url, jsonres))
        if "errcode" in jsonres and jsonres['errcode'] == 200:
            return jsonres
        return None

    def parseo2oaction(self, action_dict):
        _action = None
        if action_dict:
            _action = o2oad_action()
            _action['action'] = action_dict["action"]
            _action['adlist'] = action_dict["ad"]
            _action['fullplay'] = action_dict["fullplay"]
            if 'pos' in action_dict.keys():
                _action.pos = action_dict['pos']
            if 'interval' in action_dict.keys():
                mtime = action_dict['interval'].split(",")
                if len(mtime):
                    _action['offset'] = mtime[0]
                    _action['interval'] = mtime[1]
                    _action['listinterval'] = mtime[2]
        return _action

    def geto2oadinfolist(self):
        url = "%s/ad/policy/%s" % (self.O2OAPI1, tsServiceTask.get_ktvid())
        jsonres = request_json(url, timeout=10, method='GET')
        logger.debug("geto2oadinfolist: url:%s \nresult:%s\n" % (url, jsonres))
        ad = self.o2oad()
        if jsonres and 'errcode' in jsonres and jsonres['errcode']==200:
            if "ad_pos" in jsonres.keys():
                ad_pos = jsonres['ad_pos']
                if "start" in ad_pos.keys():
                    ad['start_action'] = self.parseo2oaction(ad_pos["start"])
                if "mv" in ad_pos.keys():
                    ad['mv_action'] = self.parseo2oaction(ad_pos["mv"])
                if "end" in ad_pos.keys():
                    ad['end_action'] = self.parseo2oaction(ad_pos["end"])
                if "no_song" in ad_pos.keys():
                    ad['nosong_action'] = self.parseo2oaction(ad_pos["no_song"])
                if "horizon_lock_screen" in ad_pos.keys():
                    ad['horizon_action'] = self.parseo2oaction(ad_pos["horizon_lock_screen"])
                if "verticle_lock_screen" in ad_pos.keys():
                    ad['verticle_action'] = self.parseo2oaction(ad_pos["verticle_lock_screen"])
                if "redpack" in ad_pos.keys():
                    ad['redpack_action'] = self.parseo2oaction(ad_pos["redpack"])
                if "7000plus" in ad_pos.keys():
                    ad['redpack_action'] = self.parseo2oaction(ad_pos["7000plus"])
            if  "ad_info" in jsonres.keys():
                ad_info = jsonres["ad_info"]
                if ad_info:
                    for  item in ad_info:
                        mo2oad = self.o2oad_tvinfo()
                        mo2oad['id'] = item['ad']
                        mo2oad['url'] = item['url']
                        mo2oad['url2'] = item['url2']
                        mo2oad['url2'] = item['url2']
                        if item["type"].lower() == 'video':
                            mo2oad['type'] = 0
                        elif item["type"].lower() == 'gif':
                            mo2oad['type'] = 1
                        else:
                            mo2oad['type'] = 2
                        mo2oad['typestr'] = item["type"]
                        mo2oad['time'] = item['time']
                        mo2oad['monitor_url'] = []
                        mo2oad['md5'] = item['md5']
                        for mstr in item["monitor_url"]:
                            mo2oad['monitor_url'].append(mstr)
                        ad['ad_dict'].append(mo2oad)
            return ad

    def o2oad(self):
        #         /// 开台时 广告播放规则
        #         public o2oad_action start_action;
        #         /// 播放MV的时候 广告播放规则 
        #         public o2oad_action mv_action;
        #         /// 关台或没有歌曲播放时 广告播放规则
        #         public o2oad_action end_action;
        #         /// 无歌曲播放时
        #         public o2oad_action nosong_action;
        #         /// 横屏
        #         public o2oad_action horizon_action;
        #         /// 竖屏
        #         public o2oad_action verticle_action;
        #         /// 红包广告位
        #         public o2oad_action redpack_action;
        #         public List<o2oad_tvinfo> ad_dict;
        ad['start_action'] = None
        ad['mv_action'] = None
        ad['end_action'] = None
        ad['nosong_action'] = None
        ad['horizon_action'] = None
        ad['verticle_action'] = None
        ad['redpack_action'] = None
        ad['ad_dict'] = []


    def o2oad_action(self):
        #         /// 一组广告播放方式：循环轮播，随机播一个  random  cycle
        #         public string action;
        #         /// 该位置可以播放的广告id列表                   
        #         public List<object> adlist;
        #         /// 是否强制完整播放该广告，1是，0不
        #         public int fullplay;
        #         /// 横竖坐标  x,y
        #         public string pos;
        #         /// 开始位置（毫秒）
        #         public long offset;
        #         ///  播放间隔 (毫秒)
        #         public long interval;
        #         ///  组播放间隔 (毫秒)
        #         public long listinterval;
    
        ac = {}
        ac['action'] = None
        ac['adlist'] = None
        ac['fullplay'] = None
        ac['pos'] = None
        ac['offset'] = None
        ac['interval'] = None
        ac['listinterval'] = None
        return ac
 

    def o2oad_tvinfo(self):
        #         /// 广告ID
        #         public int id;
        #         /// 广告素材地址
        #         public string url;
        #         /// 广告素材地址
        #         public string url2;
        #         /// 类型  0: video  1: gif 2: image
        #         public int type;
        #         /// 类型  video  gif  image
        #         public string typestr;
        #         /// 时长 秒
        #         public int time;
        #         /// 本地保存目录 
        #         public string localpath;
        #         /// 本地保存目录 
        #         public string localpath2;
        # 
        #         public int trytime;
        #         public long last_exectime;
        # 
        #         /// 监播地址 
        #         public List<string> monitor_url;
        #         public string md5;
        ad = {}
        ad["id"] = None
        ad["url"] = None
        ad["url2"] = None
        ad["type"] = None
        ad["typestr"] = None
        ad["time"] = None
        ad["localpath"] = None
        ad["localpath2"] = None
        ad["last_exectime"] = None
        ad["monitor_url"] = None
        ad["md5"] = None
        ad["trytime"] = 0
        return ad

    def do_run(self):
        try:
            #获取o2o 里面的信息 所有的信息
            self.res_adcaption = self.geto2oadcaption()
        except Exception as e:
            logger.error(traceback.format_exc())

        try:
            #获取o2o 里面的信息 所有的信息
            ad = self.geto2oadinfolist()
            if ad:
                for tv in ad['ad_dict']:
                    mitem = self.o2oad_tvinfo()
                    mitem['url'] = tv['url']
                    mitem['url2'] = tv['url2']
                    mitem['typestr'] = tv['typestr']
                    mitem['type'] = tv['type']
                    mitem['time'] = tv['time']
                    mitem['md5'] = tv['md5']
                    mitem['trytime'] = 0
                    mitem['last_exectime'] = 0
                    self._down_dict[tv['id']] = mitem
                #此处需要下载操作
                #以及加工操作
                #需要进行下载的操作
                for adid in self._down_dict.keys():
                    _down_tv = self._down_dict[adid]
                    #每一个都同步
                    res = self.syncadinfo(_down_tv)
                    #根据同步结果 进行下一步操作
        except Exception as e:
            logger.error(traceback.format_exc())
            
    def syncadinfo(self, tv, check=True):
        if check:
            url_suc = False
            _server_localpath = self.server_localpath if tv.type == 0 else os.path.join(HTDOCDIR,'gif')
            if tv.url:
                ext = os.path.splitext(tv['url'])[1]
                localpath = os.path.join(self._localsavepath, md5(tv['url']) + str(ext))
                logger.debug("download url:%s to file %s" % (tv['url'], localpath))
                #同步并下载文件
                if self.fu.downfile(tv['url'], localpath, None, None):
                    pass
                else:
                    #没有下载成功时的操作
                    logger.error("Failed to download url:%s to file %s" % (tv.url, localpath))

            if tv.url2:
                ext = os.path.splitext(tv['url2'])[1]
                localpath = os.path.join(self._localsavepath, md5(tv['url2'])+str(ext))
                logger.debug("download url2:%s to file %s" % (tv['url2'], localpath))
                #同步并下载文件
                if self.fu.downfile(tv['url2'], localpath, None, None):
                    pass
                else:
                    #没有下载成功时的操作
                    logger.error("Failed to download url2:%s to file %s" % (tv['url2'], localpath))
                    pass
        return True

    #删除广告文件 
    def deladinfo(self):
        if not self.del_dict or len(self.del_dict.keys()) == 0:
            return True
        for adid in self.del_dict.keys():
            try:
                tv = self.del_dict[adid]
                if tv['localpath'] and os.path.exists(tv['localpath']):
                    os.remove(tv['localpath'])
                if tv['localpath2'] and os.path.exists(tv['localpath2']):
                    os.remove(tv['localpath2'])
            except Exception as ex:
                logger.error(traceback.format_exc())

appADInfo = _appADInfo()

if __name__ == '__main__':
    pass
