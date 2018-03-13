#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from functools import wraps
from lib.thunder_ex import *
import time
import md5
import hashlib

def ServiceMethod(params=[]):
    def wrapper(func):
        @wraps(func)
        def wrapped_func(self, *args, **kwargs):
            if self.get_argument('nosign', '0') == '1':
                return func(self, *args, **kwargs)
            #Check time
            c_time = ''
            c_time = self.get_argument('time', '0')
            if c_time.isdigit():
                c_time = long(c_time)
            else:
                c_time = 0
            s_time = time.time()
            if abs(c_time - s_time) > 600:
                #timeout
                raise TimeOutError()

            pstr = ''
            for key in params:
                pstr = pstr + "%s=%s&" % (key, self.get_argument(key, ''))
            req_str = pstr.rstrip('&')
            new_sign = hashlib.md5(req_str + self.application.appkey).hexdigest()
            sign = self.get_argument('sign', '')
            if sign == new_sign:
                #signature is right, just with the 1 to align the return value
                return func(self, *args, **kwargs)
            else:
                raise NoAuthError()
        return wrapped_func
    return wrapper

def PrivateMethod():
    def check_cip(func):
        @wraps(func)
        def checkCip_func(self, *args, **kwargs):
            cip = self.request.remote_ip
            if len(self.application.re_allowip.findall(cip)) == 0:
                #the remote ip are not allowed to access this API
                raise NoLoginError()
            return func(self, *args, **kwargs)
        return checkCip_func
    return check_cip
