#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import logging
import platform
import threading
import traceback

from control.ktvinfo import KTVInfo

logger = logging.getLogger(__name__)

class tsTask(object):
    _status = 'not run yet'
    _confirm = False
    _lastrun = 0
    _lastmsg = ''
    _interval = 3600
    #serviceUrl =    "http://ktv.api.ktvdaren.com/"
    Ktv90 = "http://v1.ktv.api.ktvdaren.com"
    KtvApi = "http://ktv.api.ktvdaren.com"
    songlist = "http://ktv.api.ktvdaren.com"
    O2OAPI = "http://api.ktvsky.com"
    O2OAPI1 = "http://api.stage.ktvsky.com"
    kcloud_v2 = "http://kcloud.v2.service.ktvdaren.com"
    #cloudmusic appid
    cm_appid = 'ebf0694982384de46e363e74f2c623ed'
    ### 支付宝2.0RSA私钥路径
 
    def __init__(self, name='servicetask'):
        self.name = name

    def _common_init(self, name):
        self.running = False
        self._lastmsg = 'ok'
        self._confirm = False
        self._status = ''
        self._lastrun = 0
        #allow interactive task:
        self._interactive = False

        self.channel = self.get_channel()
        self.platform = self.get_platform()

    @property
    def lastrun(self):
        return self._lastrun

    @property
    def interval(self):
        return self._interval

    @property
    def confirm(self):
        return self._confirm

    @property
    def status(self):
        return self._status

    @property
    def lastmsg(self):
        return self._lastmsg

    def run(self):
        logger.error('[%s] task scheduled, time: %.2f' % (self.name, time.time()))
        if self.running:
            logger.error('[%s] already running, cannot run two instance at the same time' % self.name)
            return

        self.running = True
        try:
            #处理用户确认状态及行为：
            if self._confirm and self.status == 'confirmed':
                logger.info('[%s] run callback with confirmed action' % self.name)
                self.do_callback()
                self._lastrun = time.time()
                self._confirm = False
                return
            if self._confirm:
                logger.info('[%s] waiting user confirm action' % self.name)
                return 

            #先记时间，万一执行的时候有错误不会频繁执行:
            self._lastrun = time.time()
            #再走正常的程序
            self.do_run()
        except Exception as ex:
            logger.error(traceback.format_exc())
        finally:
            self.running = False
            logger.error('[%s] run out, time: %.2f' % (self.name, time.time()))

    def do_run(self):
        '真正的处理在这里'
        print("[%s] method do_run() not implement yet" % self.name)
        pass


    def do_callback(self):
        print("[%s] method callback() not implement yet" % self.name)
        pass

    def get_status(self):
        if self.running:
            status = '正执行中'
        else:
            if self.confirm:
                status = "等待用户确认"
            else:
                status = '已经停止'
        lastrun = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.lastrun) )
        return dict(lastrun=lastrun, status=status, confirm=self.confirm, interval = self.interval, result='success', msg=self.lastmsg, info={})

    def get_platform(self):
        self.platform = platform.uname()[4]

    def get_channel(self):
        arr = open("/etc/version").read().split(" ")
        if len(arr) == 2:
            channel = arr[1]
        else:
            channel = 'leishi'
        self.channel = channel

    def confirm_to_run(self):
        self._status = 'confirmed'
        return True


class _tsServiceTask(object):
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
                    cls.__instance = super(_tsServiceTask, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self):
        self.tasks = {}
        print("init class tsServiceTask")
        pass

    def get_ktvinfo(self):
        ktvinfo = KTVInfo.get_ktvinfo()
        return ktvinfo

    def get_ktvid(self):
        ktvinfo = self.get_ktvinfo()
        if ktvinfo:
            if 'StoreId' in ktvinfo.keys():
                return ktvinfo['StoreId']
        return None

    def get_dogname(self):
        ktvinfo = self.get_ktvinfo()
        if ktvinfo:
            if 'dogname' in ktvinfo.keys():
                return ktvinfo['dogname']
        return None

    def add_task(self, taskObj, name=''):
        if not name:
            name = taskObj.name
        if name not in self.tasks:
            self.tasks[name] = taskObj
            return True
        else:
            return False

    def del_task(self, name):
        self.tasks.pop(name)
        return True

    def task_status(self, name):
        return self.tasks[name].get_status()

    def tasks_status(self):
        tstatus = {}
        for name in self.tasks:
            tstatus[name] = self.tasks[name].get_status()
        return tstatus

    def schedule(self):
        tnow = time.time()
        for t in self.tasks:
            if (tnow - self.tasks[t].lastrun) > self.tasks[t].interval or \
                    (self.tasks[t]._confirm == True and self.tasks[t]._status == "confirmed"):
                self.tasks[t].run()
        return True

tsServiceTask = _tsServiceTask()

