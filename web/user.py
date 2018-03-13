#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import logging
from tornado import gen
from web.base import WebBaseHandler
from lib.types import is_safe_pwd, try_to_int
from control.api import UpDataAdminPsw

class UpdatePwdHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if not self.check_login():
            self.redirect('/login')
            return
        self.render('updatepwd.html')

    @gen.coroutine
    def post(self, op):
        if not self.check_login():
            self.redirect('/login')
            return
        #if op == 'update':
        _res = {}
        _res['code'] = 1
        _res['msg'] = u"密码修改失败失败！"
        oldpwd = self.get_argument('oldpwd', '')
        newpwd = self.get_argument('newpwd', '')
        renewpwd = self.get_argument('renewpwd', '')
        if oldpwd == '':
            _res['msg'] = "旧密码不能为空！"
            self.send_json(_res)
            return
        if newpwd == '':
            _res['msg'] = "新密码不能为空！"
            self.send_json(_res)
            return
        if not renewpwd == newpwd:
            _res['msg'] = "两次输入的新密码不一致！";
            self.send_json(_res)
            return

        if not is_safe_pwd(newpwd, 6, 16):
            _res['msg'] = "密码设置的太过简单（密码必须包含数字、字母，长度6-16位）！";
            self.send_json(_res)
            return

        userid = try_to_int(self.user['UserNo'])
        if userid <= 0:
            #if user info invalid, logout directly
            self.redirect('/logout')
            return

        res = UpDataAdminPsw(userid, oldpwd, newpwd);
        if res:
            _res['code'] = 0
            _res['msg'] = "密码修改成功！";
        else:
            _res['msg'] = "密码修改失败！";
        self.send_json(_res)

