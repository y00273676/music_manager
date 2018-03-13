#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
从线上拉取资源文件，并部署到相应目录去
'''

import os
import time
import json
import logging
import datetime
import traceback
import threading
import hashlib
import codecs

from common.fileutils import fileUtils
from common.ZFile import extract
from lib.http import request_json

from control.configs import get_config, update_setconfig
from handler.tsTask import tsServiceTask,tsTask
from setting import TMPDIR, DOWNLOADDIR, HTDOCDIR

logger = logging.getLogger(__name__)

#下载任务和更新任务不同时进行
class _appDeploy(tsTask):
    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('_appDeploy singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(_appDeploy, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('_appDeploy singleton is exists')
        return cls.__instance

    def __init__(self, name='appDeploy'):
        self.name = name
        self.fu = fileUtils(self.name)
        self.store_path = os.path.join(DOWNLOADDIR, self.name)
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)
        self.topath = os.path.join(HTDOCDIR, self.name)
        self.ktvid = 0
        self._common_init(self.name)
        self.lk = 2
        self.last_update = 0

        cfg = get_config('climax_update')
        if cfg:
            self.last_update = cfg['config_value']
        if self.last_update.isdigit():
            self.last_update = int(self.last_update)
        else:
            self.last_update = 0

        
    def do_run(self):
        try:
            self.ktvid = tsServiceTask.get_ktvid()
            b_failed = False
            done_tasks = 0
            cur_time = int(time.time())
            if self.lk == 1:
                url = "%s/task/ktvtasklist?ktvid=%d&time=%d&lk=1" % (self.Ktv90, self.ktvid, cur_time)
            else:
                url = "%s/task/ktvtasklist?ktvid=%d&time=%d" % (self.Ktv90, self.ktvid, cur_time)
            logger.debug(url)
            dic_res = request_json(url, timeout=10, method='GET')
            if isinstance(dic_res, dict) and dic_res['code'] == 1:
                for task in dic_res['list']:
                    task_time = 10000
                    if 'task_time' in task.keys():
                        d = datetime.datetime.strptime(task['task_time'], '%Y-%m-%d %H:%M:%S')
                        task_time = int(time.mktime(d.timetuple()))
                    logger.info('task_name: %s, task_time: %s, time:%s, update:%s' % ( task['task_linuxsavepath'], task['task_time'], task_time, self.last_update))
                    if self.last_update <= task_time:
                        ret = self.deploy_res(task)
                        if not ret:
                            #only record the failed case
                            logger.error('task_name: %s, task_time: %s, time:%s, update:%s' % ( task['task_linuxsavepath'], task['task_time'], task_time, self.last_update))
                            b_failed = True
                        else:
                            done_tasks += 1
                        if task['task_linuxsavepath'].endswith('SongClimax'):
                            if not self.load_climax():
                                logger.error("failed to load climax info to database")
            if not b_failed and done_tasks >= 1:
                #update last_update time if all task successed
                update_setconfig({'climax_update': cur_time})

        except Exception as e:
            logger.error(traceback.format_exc())

    def deploy_res(self, res):
        if not isinstance(res, dict):
            return False
        try:
            if 'task_linuxsavepath' in res.keys():
                if not os.path.exists(res['task_linuxsavepath']):
                    os.makedirs(res['task_linuxsavepath'])
            if 'task_url' in res.keys():
                url = "%s?ktvid=%d&time=%d&karaoikver=&erpver=" % (res['task_url'], self.ktvid, int(time.time()))
                logger.debug('taskname:%s, url:%s' % (res['task_name'], url))
                dic_res = request_json(url, timeout=10, method='GET')
                if not isinstance(dic_res, dict) or int(dic_res['code']) != 1:
                    return False
                dic_res = dic_res['data']
                rlist = dic_res.get('data_source')
                if isinstance(rlist, list):
                    for rf in rlist:
                        fname = os.path.join(res['task_linuxsavepath'], os.path.basename(rf))
                        logger.debug("resource: %s -> %s" % (rf, fname))
                        ret = self.down_res(rf, res['task_linuxsavepath'])
                        if not ret:
                            logger.error("failed to download %s to %s" % (res, fname))
                            return False
                rinfo = dic_res.get('data_info')
                if not rinfo:
                    return False
                if res['task_jsonname'] == 1:
                    info_name = 'data_%d.json' % int(time.time())
                else:
                    info_name = 'data.json'
                fname = os.path.join(res['task_linuxsavepath'], info_name)
                #open(fname, 'w+').write(json.dumps(rinfo))
                codecs.open(fname, 'w+', encoding='utf8').write(rinfo)
            return True
        except Exception as ex:
            logger.error(traceback.format_exc())
        return False

    def load_climax(self):
        try:
            climax_path = '/opt/thunder/www/SongClimax/'
            climax_info = json.loads(open(os.path.join(climax_path, 'data.json')).read())
            climax_list = climax_info['list']
            climax_list.sort(key=lambda obj:obj.get('addtime'), reverse=False)
            climax_dict = {}
            for climax in climax_list:
                if climax['type'] != 1:
                    #only load version-2 climax info
                    continue
                fname = os.path.join(climax_path, climax['filename'])
                for line in open(fname):
                    line = line.strip()
                    index = line.find(' ')

                    music_no = line[0:index]
                    climax = line[index:].strip()
                    climax_dict[music_no] = climax
            nfname = '/data/tmp/climax.tmp'
            nfp = open(nfname, 'w+')
            nfp.truncate(0)
            for mno in climax_dict.keys():
                nfp.write("%s|%s\n" % (mno, climax_dict[mno]))
            nfp.close()
            cmd = '/opt/local/mysql/bin/mysql -h 127.0.0.1 -u root -pThunder#123 karaok -e "delete from mediaclimax"'
            ret = os.system(cmd)
            if ret:
                logger.error("Failed to clean old data in mediaclimax table")
            cmd = '/opt/local/mysql/bin/mysql -h 127.0.0.1 -u root -pThunder#123 karaok -e '\
                    '"load data local infile \'%s\' into table mediaclimax fields terminated by \'|\'" ' % nfname
            ret = os.system(cmd)
            if ret:
                logger.error("Failed to load new data into mediaclimax table")

            cmd = '/opt/local/mysql/bin/mysql -h 127.0.0.1 -u root -pThunder#123 karaok -e "update medias set medias.media_climax=0"'
            ret = os.system(cmd)
            if ret:
                logger.error("Failed to clean mediaclimax flag in medias table")
            cmd = '/opt/local/mysql/bin/mysql -h 127.0.0.1 -u root -pThunder#123 karaok -e "update medias, mediaclimax set medias.media_climax=1,medias.media_climaxinfo = mediaclimax.media_climaxinfo where medias.media_no = mediaclimax.media_no"'
            ret = os.system(cmd)
            if ret == 0:
                os.remove(nfname)
                return True
            else:
                logger.error("Failed to apply new climax info into medias table")
                return False
        except Exception as ex:
            logger.error(traceback.format_exc())
            return False

    def file_md5(self, filename):
        '''
        calc the md5sum for a file
        better to put in common files
        '''
        f = open(filename,'rb')
        md5_obj = hashlib.md5()
        while True:
            d = f.read(8096)
            if not d:
                break
            md5_obj.update(d)
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
        return md5

    def down_res(self, url, savepath):
        filename = os.path.basename(url)
        fname = os.path.join(savepath, filename)
        downres = False
        if os.path.exists(fname):
            fmd5 = self.file_md5(fname)
            if fmd5 != filename:
                os.remove(fname)
                downres = self.fu.downfile(url, fname, None, None)
            else:
                return True
        else:
            downres = self.fu.downfile(url, fname, None, None)

        return downres


appDeploy = _appDeploy()

if __name__ == '__main__':
    pass
