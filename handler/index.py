#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import time
import logging
import commands
import traceback

from tornado import gen
from web.base import WebBaseHandler
from handler.tsTask import tsServiceTask
from handler.appUpdate import appUpgrade
from handler.appNewSong import appNewSong
from handler.appCloudSong import appCloudSong
from handler.appTheme import appTheme
from handler.appModule import appModule
from handler.appDeploy import appDeploy
from handler.appADInfo import appADInfo
from handler.appWallpaper import appWallpaper
from handler.appCleaner import appCleaner

logger = logging.getLogger(__name__)

#添加后台任务
#tsServiceTask.add_task(appUpgrade)
tsServiceTask.add_task(appNewSong)
#tsServiceTask.add_task(appCloudSong)
#tsServiceTask.add_task(appTheme)
#tsServiceTask.add_task(appModule)
#tsServiceTask.add_task(appDeploy)
#tsServiceTask.add_task(appCleaner)
#not ready yet:
#tsServiceTask.add_task(appADInfo)
#tsServiceTask.add_task(appWallpaper)

class indexHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        ret = {'code': 0, 'msg': 'ok', 'tasks': [], 'info':None}
        #ret['info'] = tsServiceTask.get_ktvinfo()
        ret['tasks'] = tsServiceTask.tasks_status()
        self.send_json(ret)

class tasksHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            ret = {'code': 0, 'msg': 'ok', 'tasks': [], 'info':None}
            #ret['info'] = tsServiceTask.get_ktvinfo()
            ret['tasks'] = tsServiceTask.tasks_status()
            self.send_json(ret)

    @gen.coroutine
    def post(self, op):
        if op == 'confirm':
            ret = dict(code=1, msg='ok', result=None)
            tname = self.get_argument('task', '')
            if tname not in tsServiceTask.tasks.keys():
                ret['msg'] = "task name not exists"
            if not tsServiceTask.tasks[tname].confirm:
                ret['msg'] = "time out for confirm action"
            elif tsServiceTask.tasks[tname].confirm_to_run():
                ret['code'] = 0
                ret['msg'] = "Task will be run soon"
            self.send_json(ret)
