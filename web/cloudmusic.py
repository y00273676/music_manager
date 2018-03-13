#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from web.base import WebBaseHandler
from lib.types import try_to_int
from lib.mc import _defaultredis as redis_cli
from tornado import web, gen
import subprocess
import xmlrpclib
from control.cloudmusic import get_cloudmusic_list, get_musicinfo_bylist, \
        get_musicinfo_byno, get_cloud_session, search_cloudmusic_list, \
        get_music_downlog
from control.configs import get_config

logger = logging.getLogger(__name__)

def isAria2Installed():
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and 'aria2c' in os.listdir(cmdpath):
            return True

    return False

def isAria2rpcRunning():
    pgrep_process = subprocess.Popen('pgrep -l aria2', shell=True, stdout=subprocess.PIPE)

    if pgrep_process.stdout.readline() == b'':
        return False
    else:
        return True

def get_dljobs_map_key():
    return "aria2_gid_mapto_sno"

class CloudMusicHandler(WebBaseHandler):
    def get(self, op):
        _res = {'code':1, 'msg':'ok', 'result':None}
        if op == 'list':
            key = self.get_argument('key', '')
            offset = try_to_int(self.get_argument('offset', '0'))
            limit = try_to_int(self.get_argument('limit', '10'))
            result = search_cloudmusic_list(key, offset, limit)
            #result = get_cloudmusic_list(offset, limit)
            _res['result'] = result
            self.send_json(_res)
            return
        elif op == 'search':
            key = self.get_argument('key', '')
            offset = try_to_int(self.get_argument('offset', '0'))
            limit = try_to_int(self.get_argument('limit', '10'))
            result = search_cloudmusic_list(key, offset, limit)
            _res['result'] = result
            self.send_json(_res)
            return
        elif op == 'info':
            mnos = []
            nos = self.get_argument('nos', '')
            for n in nos.split(';'):
                if n.isdigit:
                    mnos.append(n)
            if not mnos:
                _res['code'] = 0
                _res['msg'] = '没有发现有效的歌曲编号!'
                self.send_json()
                return

            res = get_musicinfo_bylist(mnos)
            print res
            if res:
                _res['result'] = res
            self.send_json(_res)
            return
        elif op=='rtdl':
            #Read setting from db at first.
            rtdl = 0
            try:
                cfg = get_config('CloudMusic_realdown')
                if isinstance(cfg, dict):
                    rtdl = cfg['config_value']
            except:
                pass
            if str(rtdl).isdigit():
                rtdl = int(rtdl)
            else:
                rtdl = 0
            if rtdl == 0:
                _res['code'] = 1
                _res['msg'] = '系统设置中未开启实时下载！'
                _res['result'] = rtdl
                self.send_json(_res)
                return None

            #if enabled rtdl in db, continue to check the login status:
            ses = get_cloud_session()
            if not isinstance(ses, dict):
                _res['code'] = 0
                _res['msg'] = '云客户端未登录！'
                self.send_json(_res)
                return None
            if ses['mealtype'] == 0:
                _res['code'] = 1
                _res['msg'] = '云客户端已经登录！'
                _res['result'] = 1
                self.send_json(_res)
                return None
            else:
                _res['code'] = 1
                _res['msg'] = '云客户端已经登录！'
                _res['result'] = 1
                self.send_json(_res)
                return None
            _res['code'] = 0
            _res['msg'] = '出错啦！'
            self.send_json(_res)
            return None
        elif op=='dlog':
            offset = try_to_int(self.get_argument('offset', '0'))
            limit = try_to_int(self.get_argument('limit', '10'))
            res = get_music_downlog(offset, limit)
            if isinstance(res, dict):
                _res['code'] = 1
                _res['result'] = res
            self.send_json(_res)
            return None

        else:
            pass

    def post(self, op):
        pass
