#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月17日

@author: yeyinlin
'''
from modules.model.common import *
class o2oad_action(Serializable):
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
    
    def __init__(self):
        self.action = None
        self.adlist = None
        self.fullplay = None
        self.pos = None
        self.offset = None
        self.interval = None
        self.listinterval = None
        
class o2oad(Serializable):
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
    def __init__(self):
        self.start_action = None
        self.mv_action = None
        self.end_action = None
        self.nosong_action = None
        self.horizon_action = None
        self.verticle_action = None
        self.redpack_action = None
        self.ad_dict = []

class o2oad_tvinfo(Serializable):
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
    def __init__(self):
        self.id = None
        self.url = None
        self.url2 = None
        self.type = None
        self.typestr = None
        self.time = None
        self.localpath = None
        self.localpath2 = None
        self.last_exectime = None
        self.monitor_url = None
        self.md5 = None
        self.trytime = 0

if __name__ == '__main__':
    pass
