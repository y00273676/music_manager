#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import traceback
import logging
import threading
from tornado import ioloop
from tsjob.cloudlogin import CloudLoginTask
from tsjob.cloudmusic import CloudMusicTask

logger = logging.getLogger(__name__)

tasklist = {'cloudlogin': CloudLoginTask, 'cloudmusic': CloudMusicTask}
#tasklist = {'cloudlogin': CloudLoginTask}

count = 1

def job_callback():
    global count
    global tasklist
    for t in tasklist:
        print tasklist[t].lasttime
    count += 1
    print "done %d" % count

def run_tasks():
    global tasklist
    print '***********************'
    try:
        for t in tasklist.keys():
            ts = tasklist.get(t)
            if not ts:
                print("Failed to get handler for %s" % ts.name)
                continue
            if ts.check_time() and ts.pre_check():
                print("handler for %s will be run..." % ts.name)
                tasklist[t].do_run()
            else:
                print("handler for %s will not run..." % ts.name)
                #logger.debug("task %s not run due to lack of preconditions" % t.name)
    except Exception as ex:
        logger.error(traceback.format_exc())
    return job_callback

class _JobManager(object):
    #peridically time , by seconds
    t_inteval = 5 * 1000
    #task name
    name = 'jobmanager'
    #running status
    running = False
    #last time to run
    lasttime = 0
    #if not self.loopfd:

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
                    cls.__instance = super(_JobManager, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self, name='jobmanager'):
        self.name = name
        self.loopinst = ioloop.IOLoop.instance()
        self.loopfd = ioloop.PeriodicCallback(run_tasks, self.t_inteval, self.loopinst)

    def config(self, jobname, start=7, end=20, inteval=600):
        global tasklist
        if jobname in tasklist.keys():
            return tasklist[jobname].config(start, end, inteval)
        return False

    def addjob(self, jobname, handler):
        global tasklist
        try:
            if jobname and handler:
                tasklist['jobname'] = handler
                return True
        except Exception as ex:
            logger.error(traceback.format_exc())
        return False

    def deljob(self, jobname):
        global tasklist
        try:
            if jobname and jobname in tasklist.keys():
                tasklist.pop(jobname)
        except Exception as ex:
            logger.error(traceback.format_exc())
            return True
        finally:
            pass

    def status(self):
        tasks = []
        for t in tasklist.keys():
            status = tasklist[t]['handler'].status()
            tasks.append(status)
        return tasks

    def start(self):
        try:
            self.running = True
            self.loopfd.start()
            print("after loopfd was started")
            return True
        except Exception as ex:
            logger.error(traceback.format_exc())
        return False

    def stop(self):
        try:
            self.loopfd.stop()
            self.running = False
            return True
        except Exception as ex:
            logger.error(traceback.format_exc())
        return False

JobManager = _JobManager('jobmanager')
