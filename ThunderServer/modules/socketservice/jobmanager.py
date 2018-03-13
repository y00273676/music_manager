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

sys.path.append("..")
from fileutils import *
#
class updatejobtime():
    def Ins(self):

        pass

class roomclassinfo():
    def Ins(self):
        pass

class CodeExec():
    def Ins(self):
        pass

class ktv_moduleonline():
    def Ins(self):
       pass

class moduleinfo():
    def Ins(self):
        pass

class UpModule_Theme():
    def Ins(self):
        pass

class o2o_adinfo():
    def Ins(self):
        pass

class Wallpapers():
    def __init__(self):
        self.name = 'Wallpapers';
        print(self.name, 'init');

        self.meta = {};
        self.hpapers = [];
        self.vpapers = [];
        self.loops = 0;
        self.hstatus = 0;
        self.vstatus = 0;
    
    def getMeta(self):
        return self.meta;
    
    def getHPapers(self):
        return self.hpapers;

    def getVPapers(self):
        return self.vpapers;

    def getHStatus(self):
        return self.hstatus;

    def getVStatus(self):
        return self.vstatus;

    def Ins(self, ktvid):
        self.meta['pay_model'] = 0;
        self.meta['use_looppic'] = 0;
        self.meta['use_live'] = 1;
        fu = fileUtils('wallpaper');
        
        url = 'http://open.ktv.api.ktvdaren.com/';
        param = 'ktvid=' + str(ktvid) + '&op=getktvmeta&time=' + str(int(time.time()));
        sign = hashlib.md5((param + '6f9c625e6b9c11e3bb1b94de806d865').encode()).hexdigest()
        url = 'http://open.ktv.api.ktvdaren.com/KtvService.aspx?'+param + '&sign=' + sign;
        try:
            req = urllib.request.urlopen(url)
            ret = req.read()
            data=urllib.parse.unquote(str(ret, "utf8", "strict"))
            jsonobj = json.loads(data)
            if jsonobj['msg']=='OK':
                #jsonobj['data']['storeid'];
                self.meta['pay_model'] = int(jsonobj['data']['pay_model']);
                self.meta['use_looppic'] = int(jsonobj['data']['use_looppic']);
                self.meta['use_live'] = int(jsonobj['data']['use_live']);
            else:
                self.meta['pay_model'] = 0;
                self.meta['use_looppic'] = 0;
                self.meta['use_live'] = 1;
        except:
            traceback.print_exc()
        
        print('meta', self.meta);
        
        hpapers = [];
        vpapers = [];
        
        try:
            url = "http://api.ktvsky.com/ad/policy/" + str(ktvid);
            req = urllib.request.urlopen(url)
            ret = req.read()
            print(self.name, 'url', url);
            print(self.name, 'ret', ret);
            
            data=urllib.parse.unquote(str(ret, "utf8", "strict"))
            jsonobj = json.loads(data)
            vads={};
            hads={};
            if jsonobj['errcode']==200 and jsonobj['ad_pos']!=None and jsonobj['ad_info']!=None:
                if 'horizon_lock_screen' in jsonobj['ad_pos'].keys():
                    for ad in jsonobj['ad_pos']['horizon_lock_screen']['ad']:
                        hads[ad]=ad
                        print('horizon_lock_screen', ad)
                if 'verticle_lock_screen' in jsonobj['ad_pos'].keys():
                    for ad in jsonobj['ad_pos']['verticle_lock_screen']['ad']:
                        vads[ad]=ad
                        print('verticle_lock_screen', ad)
                for adinfo in jsonobj['ad_info']:
                    if adinfo['ad'] in hads.keys():
                        type = 0;
                    elif adinfo['ad'] in vads.keys():
                        type = 1;
                    else:
                        type = 2;

                    if type==2:
                        pass
                    else:
                        paper = {};
                        paper['source']='o2o';
                        paper['paper_name'] = adinfo['md5'];
                        paper['paper_id'] = adinfo['ad'];
                        paper['paper_sort'] = adinfo['ad'];
                        paper['paper_bagtype'] = type;
                        paper['paper_url'] = adinfo['url'];
                        inx = paper['paper_url'].rindex('/');
                        filename = paper['paper_url'][inx+1:];
                        inx = filename.rindex('.');
                        md5sum = filename[0:inx];
                        filepath = 'c:/thunder/apache/htdocs/cloudktvsong/' + filename;
                        print('filepath', filepath, 'md5sum', md5sum);
                        #down file c:/thunder/apach/htdocs/cloudktvsong/
                        fu.downfile(paper['paper_url'], filepath, md5sum);
                        
                        paper['monitor_url'] = [];
                        for url in adinfo['monitor_url']:
                            paper['monitor_url'].append(url);
                        if type==0:
                            hpapers.append(paper);
                        else:
                            vpapers.append(paper);
        except:
            traceback.print_exc()
        
        try:
            param = 'ktvid=' + str(ktvid) + '&op=getktvwallpage&time=' + str(int(time.time()));
            sign = hashlib.md5((param + '').encode()).hexdigest()
            url = 'http://ktv.api.ktvdaren.com/ktv_config.aspx?'+param + '&sign=' + sign;
            print(self.name, 'url', url);
            req = urllib.request.urlopen(url)
            ret = req.read()
            print(self.name, 'ret', ret);
            data=urllib.parse.unquote(str(ret, "utf8", "strict"))
            jsonobj = json.loads(data)
            if jsonobj['msg']=='OK':
                for adinfo in jsonobj['result']['matches']:
                    type = adinfo["page_bagtype"];
                    paper = {};
                    paper['source']='dr';
                    paper['paper_name'] = adinfo["page_name"];
                    paper['paper_id'] = adinfo["page_id"];
                    paper['paper_sort'] = adinfo["page_sort"];
                    paper['paper_bagtype'] = adinfo["page_bagtype"];
                    paper['paper_invalidtime'] = adinfo["page_invalidtime"];
                    paper['paper_url'] = adinfo["page_url"];
                    paper['paper_time'] = adinfo["page_time"];
                    paper['paper_state'] = adinfo["page_state"];
                    if type==0:
                        hpapers.append(paper);
                    else:
                        vpapers.append(paper);
        except:
            traceback.print_exc()

        self.hpapers = hpapers;
        self.vpapers = vpapers;
        print('hpapper', self.hpapers);
        print('vpapers', self.vpapers);


class ClerCachFile():
    def Ins(self):
        pass

class DelModule():
    def Ins(self):
        pass

class LocalCachManageService():
    def Ins(self):
        pass

class NewSong():
    def Ins(self):
        pass

class UpLoadModuleDataType():
    def Ins(self):
        pass

class onlinetask():
    def Ins(self):
        pass

class upappver():
    def Ins(self):
        pass

class sentry_uplog():
    def Ins(self):
        pass

if __name__ == '__main__':
    wps = Wallpapers();
    wps.Ins(211);

