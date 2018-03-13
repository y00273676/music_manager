#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import logging
from web.base import WebBaseHandler
from lib.types import try_to_int
from lib.mc import _defaultredis as redis_cli
from tornado import web, gen
import traceback
from control.cloudmusic import get_cloudmusic_url, get_cloud_session, \
        set_musictask_gid, get_musicinfo_bylist, get_musicinfo_byno,\
        get_dljobs_map_key, get_complete_task_key, aria2_mno2gid,\
        get_aria2_complete_task, set_mno_realtime_download,\
        get_download_limit, add_music_downlog

import subprocess
import xmlrpclib

logger = logging.getLogger(__name__)

SERVER_URI_FORMAT = 'http://{0}:{1}/rpc'

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

class Aria2Handler(WebBaseHandler):
    def get(self, op):
        server_uri = SERVER_URI_FORMAT.format('127.0.0.1', '6800')
        server = xmlrpclib.ServerProxy(server_uri, allow_none=True)
        options = None
        position = None
        _res = {'code':1, 'msg':'ok', 'result':None}
        if op == 'list':
            offset = try_to_int(self.get_argument('offset', '0'))
            limit = try_to_int(self.get_argument('limit', '10'))
            jobs = []
            ret1 = server.aria2.tellActive()
            if ret1:
                for r in ret1:
                    job = {}
                    job['gid'] = r['gid']
                    job['total'] = r['totalLength']
                    job['complete'] = r['completedLength']
                    job['status'] = r['status']
                    job['url'] = r['files'][0]['uris'][0]['uri']
                    job['fpath'] = r['files'][0]['path']
                    total = int(r['totalLength'])
                    done = int(r['completedLength'])
                    if not done == 0 and total > 0:
                        job['percent'] = round(float(done)/float(total) * 99, 2)
                    else:
                        job['percent'] = 0
                    jobs.append(job)

            ret2 = server.aria2.tellStopped(0, 50)
            if ret2:
                for r in ret2:
                    job = {}
                    job['gid'] = r['gid']
                    job['total'] = r['totalLength']
                    job['complete'] = r['completedLength']
                    job['status'] = r['status']
                    job['url'] = r['files'][0]['uris'][0]['uri']
                    job['fpath'] = r['files'][0]['path']
                    total = int(r['totalLength'])
                    done = int(r['completedLength'])
                    if not done == 0 and total > 0:
                        job['percent'] = round(float(done)/float(total) * 99, 2)
                    else:
                        job['percent'] = 0
                    jobs.append(job)

            ret3 = server.aria2.tellWaiting(0, 50)
            if ret3:
                for r in ret3:
                    job = {}
                    job['gid'] = r['gid']
                    job['total'] = r['totalLength']
                    job['complete'] = r['completedLength']
                    job['status'] = r['status']
                    job['url'] = r['files'][0]['uris'][0]['uri']
                    job['fpath'] = r['files'][0]['path']
                    total = int(r['totalLength'])
                    done = int(r['completedLength'])
                    if not done == 0 and total > 0:
                        job['percent'] = round(float(done)/float(total) * 99, 2)
                    else:
                        job['percent'] = 0
                    jobs.append(job)

            for job in jobs:
                sno = redis_cli.hget(get_dljobs_map_key(), job['gid'])
                job['musicno'] = sno
                if sno and sno.isdigit():
                    minfo = get_musicinfo_byno(sno)
                    if isinstance(minfo, dict):
                        job['music_name'] = minfo['Music_Caption']
                        job['music_singers'] = ','.join([minfo['Music_SingerName'],minfo['Music_SingerNameTwo'],\
                                minfo['Music_SingerNameThree'],minfo['Music_SingerNameFour']]).strip(',')
                        job['music_language'] = minfo['Music_Language']
                        job['music_type'] = minfo['Music_3d1']
                        pass
                    else:
                        job['music_name'] = ''
                        job['music_singers'] = ''
                        job['music_language'] = ''
                        job['music_type'] = ''
                        pass
                    pass

            _res['result'] = {'data': jobs[offset:(offset+limit)], 'total':len(jobs)}
            self.send_json(_res)
            return
        elif op == 'status':
            mno = self.get_argument('no', '')
            rt = try_to_int(self.get_argument('rt', '0'))
            if mno:
                gid = aria2_mno2gid(mno)
            else:
                gid = self.get_argument('gid', '')

            if not gid:
                #看是否有缓存信息，实时下载的请求可返回此信息
                if rt == 1:
                    tinfo = get_aria2_complete_task(mno)
                    if isinstance(tinfo, dict):
                        _res['result'] = tinfo
                        self.send_json(_res)
                        return
                _res['msg'] = '下载任务已经失效，请重新添加下载任务!'
                self.send_json(_res)
                return

            r = server.aria2.tellStatus(gid)
            if isinstance(r, dict):
                job = {}
                job['gid'] = r['gid']
                job['total'] = r['totalLength']
                job['complete'] = r['completedLength']
                job['status'] = r['status']
                job['url'] = r['files'][0]['uris'][0]['uri']
                job['fpath'] = r['files'][0]['path']
                total = int(r['totalLength'])
                done = int(r['completedLength'])
                if not done == 0 and total > 0:
                    job['percent'] = round(float(done)/float(total) * 99, 2)
                else:
                    job['percent'] = 0
            else:
                job = get_aria2_complete_task(mno)
                if isinstance(job, dict):
                    job['percent'] = 100
            if not isinstance(job, dict):
                _res['msg'] = '无此歌曲下载信息！'
                self.send_json(_res)
                return

            minfo = get_musicinfo_byno(mno)
            if isinstance(minfo, dict):
                job['music_name'] = minfo['Music_Caption']
                job['music_singers'] = ','.join([minfo['Music_SingerName'],minfo['Music_SingerNameTwo'],\
                        minfo['Music_SingerNameThree'],minfo['Music_SingerNameFour']]).strip(',')
                job['music_language'] = minfo['Music_Language']
                job['music_type'] = minfo['Music_3d1']
            else:
                job['music_name'] = ''
                job['music_singers'] = ''
                job['music_language'] = ''
                job['music_type'] = ''
            _res['result'] = job
            self.send_json(_res)
            return
        else:
            pass

    def post(self, op):
        server_uri = SERVER_URI_FORMAT.format('127.0.0.1', '6800')
        server = xmlrpclib.ServerProxy(server_uri, allow_none=True)
        options = None
        position = None
        _res = {'code':1, 'msg':'ok', 'result':None}

        if op == 'add':
            url = ''
            mno = self.get_argument('no', '')
            realtime = try_to_int(self.get_argument('rt', '0'))
            cl_sec = get_cloud_session()
            if not isinstance(cl_sec, dict) or 'validkey' not in cl_sec.keys():
                _res['code'] = 0
                _res['msg'] = '云端未登录！请先在系统设置页面设置云端登录的用户名和密码，重启服务后再试！'
                self.send_json(_res)
                return
            if cl_sec['Wpayment'] == 0:
                _res['code'] = 0
                _res['msg'] = cl_sec['paymentError']
                self.send_json(_res)
                return
            if  cl_sec['dcount'] == 0 and not cl_sec['mealtype'] == 0:
                _res['code'] = 0
                _res['msg'] = "套餐额度已经用完！"
                self.send_json(_res)
                return

            if self.check_task_exists(mno, realtime):
                if realtime == 1:
                    set_mno_realtime_download(mno)
                _res['msg'] = '已经添加了下载任务'
                self.send_json(_res)
                return

            url_info = get_cloudmusic_url(mno)
            if isinstance(url_info, dict) and 'Music_Link' in url_info.keys():
                url = url_info['Music_Link']
            #TODO: Convert songno to url here
            if not url:
                url = self.get_argument('url', '')

            minfo = get_musicinfo_byno(mno)

            if not url or not minfo:
                _res['code'] = 0
                _res['msg'] = '无法获得歌曲的下载链接！'
                self.send_json(_res)
                return

            speed_cfg = get_download_limit()
            down_limit = 0
            if speed_cfg:
                if realtime == 1:
                    down_limit = speed_cfg['always_speed']
                else:
                    down_limit = speed_cfg['normal_speed']

            base_dir = '/data/download/cloudmusic'
            if not os.path.exists(base_dir):
                os.makedirs(base_dir, mode=0755)
            options = {'dir': base_dir, 'max-download-limit': "%sK" % str(down_limit)}

            #gid = server.aria2.addUri([url], options, position)
            gid = server.aria2.addUri([url], options)
            if gid:
                if mno:
                    #need set the redis here
                    gret = set_musictask_gid(mno, gid, realtime)
                    if not gret:
                        logger.error("Failed to cache gid for %s, url: %s" % ( mno, url))
                    
                _res['result'] = gid
                _res['msg'] = '添加下载任务成功！'
                _res['code'] = 1
                dlinfo = {}
                dlinfo['down_gid'] = gid
                dlinfo['music_no'] = mno
                if minfo:
                    dlinfo['music_caption'] = minfo['Music_Caption']
                    if isinstance(minfo['Singers'], list):
                        dlinfo['music_singer'] = ','.join([s['Singer_Name'] for s in minfo['Singers']])
                    else:
                        dlinfo['music_singer'] = ''
                    dlinfo['music_lang'] = minfo['Music_Language']
                    dlinfo['music_ver'] = minfo['Music_LastVersion']
                    #"/Date(1332169506000)/"
                    #dlinfo['music_verdate'] = minfo['Music_LastVersionDate']
                    dlinfo['music_type'] = minfo['Music_Normal1']

                #dlinfo['down_path'] = gid
                #dlinfo['down_url'] = url
                dlinfo['down_stime'] = datetime.datetime.now()
                #dlinfo['down_etime'] = 
                dlinfo['down_status'] = 0
                dlinfo['down_type'] = realtime
                #dlinfo['music_addtime'] = gid
                #dlinfo['music_replace'] = gid
                #dlinfo['file_md5'] = gid
                #dlinfo['file_type'] = gid
                #dlinfo['file_size'] = gid
                dlinfo['movie_type'] = 1

                add_music_downlog(dlinfo)
            self.send_json(_res)
            return
        elif op == 'remove':
            mno = self.get_argument('no', '')
            if not mno:
                _res['code'] = 0
                _res['msg'] = '无效的歌曲编号!'
                self.send_json(_res)
                return
            gid = aria2_mno2gid(mno)
            if not gid:
                _res['code'] = 0
                _res['msg'] = '无此下载任务!'
                self.send_json(_res)
                return
            #gid = self.get_argument('gid', '')
            #TODO: Convert songno to url here
            #url = self.get_argument('url', '')
            ret = server.aria2.remove(gid)
            if not ret:
                _res['code'] = 2
                _res['msg'] = '删除任务失败!'
            self.send_json(_res)
            return
        elif op == 'start':
            mno = self.get_argument('no', '')
            if not mno:
                _res['code'] = 0
                _res['msg'] = '无效的歌曲编号!'
                self.send_json(_res)
                return
            gid = aria2_mno2gid(mno)
            if not gid:
                _res['code'] = 0
                _res['msg'] = '无此下载任务!'
                self.send_json(_res)
                return
            #gid = self.get_argument('gid', '')
            #TODO: Convert songno to url here
            ret = server.aria2.unpause(gid)
            if not ret:
                _res['code'] = 0
                _res['msg'] = '无法重新唤起此任务!请稍后再试.'
            self.send_json(_res)
            return
        elif op == 'pause':
            mno = self.get_argument('no', '')
            if not mno:
                _res['code'] = 0
                _res['msg'] = '无效的歌曲编号!'
                self.send_json(_res)
                return
            gid = aria2_mno2gid(mno)
            if not gid:
                _res['code'] = 0
                _res['msg'] = '无此下载任务!'
                self.send_json(_res)
                return
            gid = server.aria2.pause(gid)
            _res['code'] = 1
            _res['msg'] = '任务已经停止!'
            _res['gid'] = gid
            self.send_json(_res)
            return
        elif op == 'stop':
            mno = self.get_argument('no', '')
            if not mno:
                _res['code'] = 0
                _res['msg'] = '无效的歌曲编号!'
                self.send_json(_res)
                return
            gid = aria2_mno2gid(mno)
            if not gid:
                _res['code'] = 0
                _res['msg'] = '无此下载任务!'
                self.send_json(_res)
                return
            tsinfo = server.aria2.tellStatus(gid)
            if not isinstance(tsinfo, dict):
                _res['code'] = 0
                _res['msg'] = '任务不存在!'
                self.send_json(_res)
                return
            if tsinfo['status'] in ['error', 'completed', 'removed']:
                ret = self.server.aria2.removeDownloadResult(tsinfo['gid'])
            else:
                ret = server.aria2.remove(tsinfo['gid'])
                ret = self.server.aria2.removeDownloadResult(tsinfo['gid'])
            fpath = tsinfo['files'][0]['path']
            if fpath:
                os.remove(fpath)
            del_musictask_gid(mno, tsinfo['gid'])
            self.send_json(_res)
            return
        elif op == 'pauseall':
            ret = server.aria2.pauseAll()
            if ret:
                _res['code'] = 0
            self.send_json(_res)
            return
        else:
            pass

    def check_task_exists(self, mno, rt=0):
        if not mno:
            return False
        gid = aria2_mno2gid(mno)
        if gid:
            try:
                server_uri = SERVER_URI_FORMAT.format('127.0.0.1', '6800')
                server = xmlrpclib.ServerProxy(server_uri, allow_none=True)
                r = server.aria2.tellStatus(gid)
                if isinstance(r, dict):
                    logger.debug("Check for download task exists, gid:%s" % gid)
                    return True
                else:
                    return False
            except Exception as ex:
                logger.error(traceback.format_exc())
                return False

        if rt == 1:
            #如果是实时下载，检查最近是否有过已经添加成功的记录，如果有则不再下载
            #在实时下载取得状态的时候，直接返回之前的下载信息即可。此缓存2小时
            #见tsjob/cloudmusic.py
            tinfo = get_aria2_complete_task(mno)
            if tinfo:
                logger.debug("Check for realtime download task exists, gid:%s" % gid)
                return True
        return False

    def check_downlog_exists(self, mno):
        pass

    def get_xml_options(params):
        options = '<struct>\n'
        for key in options.keys():
            options += '<member>\n'
            options += '<name>%s</name>\n' % key
            options += '<value><string>%s</string></value>\n' % str(options[key])
            options += '</member>\n'
        options += '</struct>\n'


