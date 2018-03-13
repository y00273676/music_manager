#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import hashlib
import traceback

from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.defines import retCode
from lib.types import try_to_int

from control.api import user_login

logger = logging.getLogger(__name__)

class LoginHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.render('login.html')

    @gen.coroutine
    def post(self):
        _res = {}
        _res['code'] = 1
        _res['msg'] = "登录失败！"
        _res['data'] = "/login"
        account = self.get_argument('account')
        pwd = self.get_argument('password')
        v_code = self.get_argument('validcode')

        verifycode = self.session.get('verifycode')
        print 'session code:%s' % verifycode
        print 'page code:%s' % v_code
        if not verifycode == v_code.lower():
            _res['msg'] = '验证码错误！'
            self.send_json(_res)
            return

        ui = user_login(account, hashlib.md5(pwd).hexdigest())
        logger.debug(str(ui))
        if ui:
            '''
            self.user = {}
            self.user['UserNick'] = ui['username']
            self.user['UserNo'] = ui['userid']
            self.user['UserType'] = ui['usertype']['id']
            self.user['UserTypeName'] = ui['usertype']['TypeName']
            self.set_cache(self.get_session_key(str(ui['userid'])), self.user, 1800);
            self.set_secure_cookie('uid', str(ui['userid']))
            '''

            self.session['UserNick'] = ui['username']
            self.session['UserNo'] = ui['userid']
            self.session['UserType'] = ui['usertype']['id']
            self.session['UserTypeName'] = ui['usertype']['TypeName']
            self.session['uid'] = ui['userid']
            self.session.save()
            print "get session UserNick: %s" % self.session.get('UserNick')

            _res = {}
            _res['code'] = 0
            _res['msg'] = "登录成功！"
            _res['data'] = "/index"
            self.send_json(_res)
        else:
            logger.info('Login Failed: user:%s, remote_ip:%s' % (account, self.request.remote_ip))
            _res = {}
            _res['code'] = 1
            _res['msg'] = "用户名或密码错误，登录失败！"
            _res['data'] = None
            self.send_json(_res)

class LogoutHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        self.logout()
        self.redirect("/login")

    @gen.coroutine
    def post(self):
        self.logout()
        self.redirect("/login")

    def logout(self):
        self.session['UserNick'] = None
        self.session['UserNo'] = None
        self.session['UserType'] = None
        self.session['UserTypeName'] = None
        self.session['uid'] = None
        self.session.save()
        pass
