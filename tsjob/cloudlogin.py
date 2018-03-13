#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import logging
import traceback
import threading
#import hashlib
from lib.http import request_json
from lib.des import DESEncrypt
from lib.mc import _defaultredis as redis_cli
from control.ktvinfo import KTVInfo
from lib.common import gen_sign_for_kcloud, generator_query_string_and_signature
from control.cloudmusic import get_cloud_session, set_cloud_session
from control.configs import get_all_config

from tsjob.base import BaseTask
logger = logging.getLogger(__name__)

class _CloudLoginTask(BaseTask):
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
                    cls.__instance = super(_CloudLoginTask, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        return cls.__instance

    def __init__(self, name='cloudtask'):
        self.name = name
        self.t_start = 0
        self.t_end = 24
        self.t_inteval = 3 * 60 #seconds
        self.lasttime = 0

        self.cloud_API_S = 'https://kcloud.v2.service.ktvdaren.com'
        self.cloud_API = 'http://kcloud.v2.service.ktvdaren.com'
        self.app_id = 'ebf0694982384de46e363e74f2c623ed'
        self.sec_key = '9c1db7829f839f362052692c89556ce3'

        self.app_ver = '4.0.0.75'

        self.box_ver = '5.0.0.72'
        self.userid = ''
        self.username = None
        self.passwd = None
        self.dogname = ''
        self.status = 'notlogin'
        self.ktvinfo = None
        self.validkey = ''

    def get_karaok_ver(self):
        self.box_ver = '5.0.0.72'

    def get_auth_info(self):
        dd = DESEncrypt()
        setinfo = get_all_config()
        if 'CloudMusic_uname' in setinfo.keys():
            self.username = setinfo['CloudMusic_uname']['config_value']
        if 'CloudMusic_passwd' in setinfo.keys():
            self.passwd = setinfo['CloudMusic_passwd']['config_value']

    def cloud_hello(self):
        '''
        通过歌曲编号，得到下载路径
        '''
        try:
            if not self.ktvinfo:
                self.ktvinfo = KTVInfo.get_ktvinfo()
                if not self.ktvinfo:
                    return False
            sinfo = get_cloud_session()
            if isinstance(sinfo, dict):
                self.validkey = sinfo['validkey']
            else:
                logger.error("Failed to get current login session")
                return False

            params = {'appid': self.app_id,
                    'appver': self.app_ver,
                    'username': self.username,
                    'userid': self.userid,
                    'dogname': self.ktvinfo['dogname'],
                    'storeid': self.ktvinfo['StoreId'],
                    'op': 'hello',
                    'validkey': self.validkey,
                    'utime': int(time.time())}

            qerystr = gen_sign_for_kcloud(params, '', self.sec_key)
            login_path = self.cloud_API_S + '/OpenService.aspx?' + qerystr

            res = request_json(login_path)
            if res['code'] == 1:
                if isinstance(res['result'], dict) and 'matches' in res['result'].keys():
                    self.validkey = res['result']['matches'][0]['validkey']
                    sinfo['validkey'] = self.validkey
                    set_cloud_session(sinfo)
                else:
                    return False
            else:
                if res:
                    logger.error("Failed to say hello: %d - %s" % (res['code'], res['msg']))
                return False
        except Exception as ex:
            logger.error(traceback.format_exc())
        return False

    def cloud_login(self):
        res, msg = self.cloud_login_msg()
        return res

    def cloud_login_msg(self):
        '''
        登录
        '''
        try:
            msg = '登录失败'
            if not (self.username and self.passwd):
                self.get_auth_info()
                if not (self.username and self.passwd):
                    return False, '未设置用户名或密码'

            if not self.ktvinfo:
                #Try get ktvinfo again
                self.ktvinfo = KTVInfo.get_ktvinfo()
                if not self.ktvinfo:
                    logger.error("cannot get ktvinfo: %s" % self.ktvinfo)
                    return False, '未得到有效的KTV信息'
            params = {'appid': self.app_id,
                    'appver': self.app_ver,
                    'dogname': self.ktvinfo['dogname'],
                    'op': 'linuxlogin',
                    'password': self.passwd,
                    'username': self.username,
                    'utime': int(time.time())}

            qerystr = gen_sign_for_kcloud(params, '', self.sec_key)
            login_path = self.cloud_API_S + '/OpenService.aspx?' + qerystr

            res = request_json(login_path)
            msg = res['msg']
            if res['code'] == 2:
                session = res['result']['matches'][0]
                session['dog'] = self.ktvinfo['dogname']
                set_cloud_session(session)
                return True, msg
            else:
                if res:
                    logger.error("Failed to say hello: %d - %s" % (res['code'], res['msg']))
        except Exception as ex:
            logger.error(traceback.format_exc())
            msg = str(ex)
        return False, msg

    def do_run(self):
        try:
            if not self.pre_check:
                logger.error("Failed in pre_check, aborted")
                return False
            cm_sec = get_cloud_session()
            if not cm_sec:
                logger.error("no session, will login again")
                if self.cloud_login():
                    logger.info("login success")
                    return True
                else:
                    logger.error("login failed")
                    return False
                return False
            else:
                self.userid = cm_sec['uid']
                self.storeid = cm_sec['storeid']
                self.dogname = cm_sec['dog']
                self.username = cm_sec['uname']
                #self.token = cm_sec['token']
                self.validkey = cm_sec['validkey']
                pass

            logger.info("only say hello")
            if not self.cloud_hello():
                self.cloud_login()
        except Exception as ex:
            logger.error(traceback.format_exc())
        finally:
            self.lasttime = time.time()

    def pre_check(self):
        return True

    def result(self):
        pass

CloudLoginTask = _CloudLoginTask('cloudlogin') 

