#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import json
import logging
import traceback
import threading
import psutil
import shutil
import xmlrpclib
import datetime

from lib.mc import _defaultredis as redis_cli
from control.cloudmusic import aria2_gid2mno, get_musicinfo_byno, \
        aria2_mno2gid, get_complete_task_key, aria2_gid2mno, \
        del_musictask_gid, update_downlog_by_mnogid

from control.actors import add_actor
from control.medias import get_file_by_no, add_update_media

from tsjob.base import BaseTask
logger = logging.getLogger(__name__)

SERVER_URI_FORMAT = 'http://{0}:{1}/rpc'
class _CloudMusicTask(BaseTask):

    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_CloudMusicTask, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self, name):
        self.lasttime = 0
        self.name = name
        self.server = self.init_rpc_server()
        self.t_start = 0
        self.t_end = 24
        self.t_inteval = 5 #seconds
        self.lasttime = 0

    def init_rpc_server(self):
        server_uri = SERVER_URI_FORMAT.format('127.0.0.1', '6800')
        server = xmlrpclib.ServerProxy(server_uri, allow_none=True)
        return server

    def get_download_list(self):
        pass

    def add_music_info(self, minfo, f_src, f_dest):
        #delete old file at first
        if f_src != f_dest:
            if os.path.exists(f_dest):
                os.remove(f_dest)
            #copy file
            ret = shutil.copy2(f_src, f_dest)
            #ret = os.system("/bin/cp -f %s %s" % (f_src, f_dest))
            #if copy successed, delete sourc file
            #if os.path.exists(f_dest):
            #    os.remove(f_src)
            logger.info("copy %s to %s, return : %s" % (f_src, f_dest, str(ret)))

        music = {}
        #not call api to add music, to avoid the api calling loop 
        if isinstance(minfo['Singers'], list):
            i = 1
            for singer in minfo['Singers']:

                actinfo = {}
                actinfo['actor_no'] = singer['Singer_Id']
                actinfo['actor_name'] = singer['Singer_Name']
                actinfo['actor_jp'] = singer['Singer_JianPin']
                actinfo['actor_py'] = singer['Singer_PinYin']
                actinfo['actor_type'] = singer['Singer_TypeName']
                ret = add_actor(actinfo)
                music['media_actno%d'%i] = singer['Singer_Id']
                music['media_actname%d'%i] = singer['Singer_Name']
                i += 1
            while(i <= 4):
                music['media_actno%d'%i] = 0
                music['media_actname%d'%i] = ''
                i += 1
        music['media_lang'] = minfo['Music_Language']
        music['media_no'] = minfo['Music_No']
        music['media_name'] = minfo['Music_Caption']
        music['media_namelen'] = len(minfo['Music_JianPin'])
        music['media_tag1'] = minfo['Music_3d1']
        music['media_tag2'] = minfo['Music_3d2']
        music['media_jp'] = minfo['Music_JianPin']
        music['media_py'] = minfo['Music_PinYin']
        music['media_actname1'] = minfo['Music_SingerName']
        music['media_actname2'] = minfo['Music_SingerNameTwo']
        music['media_actname3'] = minfo['Music_SingerNameThree']
        music['media_actname4'] = minfo['Music_SingerNameFour']
        music['media_langtype'] = minfo['Music_LanguageType']
        music['media_stars'] = minfo['Music_Star']
        music['media_volume'] = minfo['Music_Volume']
        music['media_strok'] = minfo['Music_Stroke']
        music['media_stroks'] = minfo['Music_Bihua']
        music['media_carria'] = minfo['Music_VideoFormat']
        music['media_audio'] = minfo['Music_AudioFormat']
        music['media_style'] = minfo['Music_VideoType']
        music['media_type'] = 1
        music['media_yuan'] = minfo['Music_ZTrack']
        music['media_ban'] = minfo['Music_YTrack']
        music['media_isnew'] = minfo['Music_IsNew']
        music['media_file'] = f_dest
        music['media_lyric'] = minfo['Music_Lyric']
        ret = add_update_media(music)
        logger.error("add music return: %s \nmusicinfo:%s" % (ret, music))
        if isinstance(ret, dict) and ret['code'] == 0:
            return True
        else:
            return False
        return False

    def get_serial_no(self, fname):
        '''
        从文件名取出歌曲编号，为了后面做目录的散列分布。
            暂时不支持非数字歌曲编号
        '''
        if not fname:
            return None
        arr = fname.split('.')
        if arr[0].isdigit():
            return int(arr[0])
        else:
            return None

    def new_video_path(self, mno, fsize, fname):
        '''
        返回歌曲文件应该放到哪个路径：
        1. 直接按歌曲编号后两数字做散列，以后云下歌的路径都会散列开。
        2. 取后两位的用意是为了应对（以后可能的）大的存储阵列（30万/100=3000每目录）
        3. 编号从后面取，是为了防止（如果从前面取）歌曲编号分布不均匀。
        '''
        video_root = "/video"
        b_name = ''
        bigest = 0
        serialno = self.get_serial_no(fname)
        if not serialno:
            return None

        try:
            #找空间最大的磁盘，放进去
            for d in os.listdir(video_root):
                v_path = os.path.join(video_root, d)
                du = psutil.disk_usage(v_path)
                if du.free > bigest:
                    #目录按歌曲编号的后两位做散列
                    b_name = os.path.join(v_path, 'music_%02d' % int(serialno % 100))
                    bigest = du.free
            if b_name:
                #如果目录不存在，创建目录
                if not os.path.exists(b_name):
                    os.mkdir(b_name)
            logger.debug("bigest free: %d, file size: %d, path: %s" % (bigest, fsize, b_name))
            if bigest <= fsize:
                #no space left
                return None

            des_path = os.path.join(b_name, fname)
            return des_path
        except Exception as ex:
            logger.error(traceback.format_exc())
        return None

    def old_video_path(self, mno):
        '''
        '''
        return get_file_by_no(mno)

    def find_video_path(self, mno, fsize, fname):
        '''
        返回歌曲文件应该放到哪个路径：
        1. 如果已经有此歌曲，直接替换到现有路径上
        2. 如果没有此歌曲，则按歌曲编号后两数字做散列，以后云下歌的路径都会散列开。
        3. 取后两位的用意是为了应对（以后可能的）大的存储阵列（30万/100=3000每目录）
        4. 编号从后面取，是为了防止（如果从前面取）歌曲编号分布不均匀。
        '''
        video_root = "/video"
        b_name = ''
        bigest = 0
        serialno = self.get_serial_no(fname)
        if not serialno:
            return None

        try:
            fpath = get_file_by_no(mno)
            if fpath:
                #如果找到现有的路径，直接替换到现有路径中
                return fpath

            #否则，找空间最大的磁盘，放进去
            for d in os.listdir(video_root):
                v_path = os.path.join(video_root, d)
                du = psutil.disk_usage(v_path)
                if du.free > bigest:
                    #目录按歌曲编号的后两位做散列
                    b_name = os.path.join(v_path, 'music_%02d' % int(serialno % 100))
                    bigest = du.free
            if b_name:
                #如果目录不存在，创建目录
                if not os.path.exists(b_name):
                    os.mkdir(b_name)
            logger.debug("bigest free: %d, file size: %d, path: %s" % (bigest, fsize, b_name))
            if bigest <= fsize:
                #no space left
                return None

            des_path = os.path.join(b_name, fname)
            return des_path
        except Exception as ex:
            logger.error(traceback.format_exc())
        return ''

    def check_aria2_task(self):
        ret2 = self.server.aria2.tellStopped(0, 1000)
        if ret2:
            for r in ret2:
                print(r['status'], r['files'][0]['uris'][0]['uri'],\
                        r['files'][0]['path'])
                if not r['status'] == 'complete':
                    continue
                mno = aria2_gid2mno(r['gid'])
                logger.debug("find completed mno: gid: %s -> mno:%s" % (r['gid'], mno))
                if mno:
                    minfo = get_musicinfo_byno(mno)
                    if not isinstance(minfo, dict):
                        logger.error('cannot fine minfo: %s' % mno)
                        continue
                else:
                    logger.debug("Failed find completed mno: gid: %s -> mno:%s" % (r['gid'], mno))
                    continue
                _, fname = os.path.split(r['files'][0]['path'])
                old_path = self.old_video_path(mno)
                des_path = self.new_video_path(mno, int(r['totalLength']), fname)
                #des_path = self.find_video_path(mno, int(r['totalLength']), fname)
                logger.debug("filepath: %s, filename: %s" % (des_path, fname))
                if des_path == '':
                    logger.error("cannot find path for new music")
                    continue
                logger.debug("addmusic: %s, %s" % (r['files'][0]['path'],  des_path))
                _ret = self.add_music_info(minfo, r['files'][0]['path'],  des_path)
                if _ret:
                    if old_path and old_path != des_path and os.path.exists(old_path):
                        os.remove(old_path)
                dinfo = {}
                dinfo['down_path'] = r['files'][0]['path']
                dinfo['down_url'] = r['files'][0]['uris'][0]['uri']
                dinfo['down_etime'] = datetime.datetime.now()
                dinfo['down_status'] = 1
                dinfo['music_addtime'] = datetime.datetime.now()
                if old_path:
                    dinfo['music_replace'] = 1
                else:
                    dinfo['music_replace'] = 0
                #dinfo['file_md5'] = gid
                #dinfo['file_type'] = gid
                logger.error(r)
                dinfo['file_size'] = r['totalLength']

                update_downlog_by_mnogid(mno, r['gid'], dinfo)

                #Store the completed task for 2 hours.
                key = get_complete_task_key(aria2_gid2mno(r['gid']))
                dlinfo = {}
                dlinfo['status'] = 'added'
                dlinfo['percent'] = '100'
                dlinfo['url'] = r['files'][0]['uris'][0]['uri']
                dlinfo['complete'] = r['completedLength']
                dlinfo['fpath'] = des_path
                dlinfo['gid'] = r['gid']
                dlinfo['total'] = r['totalLength']
                redis_cli.set(key, json.dumps(dlinfo))
                redis_cli.expire(key, 3600 * 1)
                if r['status'] in ["error", "removed", "complete"]:
                    self.server.aria2.removeDownloadResult(r['gid'])
                else:
                    self.server.aria2.remove(r['gid'])
                #清除GID到Music_NO的缓存映射信息。还需要一个定时清理多余项的定时任务
                #以防止出现大量的无效映射信息
                del_musictask_gid(mno, r['gid'])

                if os.path.exists(r['files'][0]['path']) and r['files'][0]['path'] != des_path:
                    os.remove(r['files'][0]['path'])

                logger.debug("add music file to %s" % des_path)

    def do_run(self):
        self.check_aria2_task()
        self.lasttime = time.time()
        pass

CloudMusicTask = _CloudMusicTask('cloudmusic')
