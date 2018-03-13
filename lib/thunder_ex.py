#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime

__all__ = ['NoLoginError', 'NoAuthError', 'TimeOutError', 'ParamError']

class TSREQError(Exception):
    """Exception raised for errors in the input.
    Attributes:
        message -- explanation of the error
        remoteip -- the client remote ip
    """

    def __init__(self, message, remoteip='', api=''):
        self.err_no = 500
        self.msg = msg
        self.remoteip = remoteip
        self.dt = datetime.datetime.now()

    def __str__(self):
        return self.msg

    def details(self):
        if remoteip == '':
            return '[%s]:%s' % (self.dt, self.msg)
        else:
            return '[%s](%s):%s' % (self.dt, self.remoteip, self.msg)
    def err_no(self):
        return self.err_no

class ParamError(TSREQError):
    def __init__(self, message='Parameter error, please check again', remoteip='', api=''):
        self.err_no = 1
        self.msg = msg
        self.remoteip = remoteip
        self.dt = datetime.datetime.now()


class NoLoginError(TSREQError):
    def __init__(self, message='Client hasn\'t login or remote ip are not allowed', remoteip='', api=''):
        self.err_no = 2
        self.msg = msg
        self.remoteip = remoteip
        self.dt = datetime.datetime.now()


class NoAuthError(TSREQError):
    def __init__(self, message='Sign error or Authentication error', remoteip='', api=''):
        self.err_no = 3
        self.msg = msg
        self.remoteip = remoteip
        self.dt = datetime.datetime.now()

class TimeOutError(TSREQError):
    def __init__(self, message='Request has timeout', remoteip='', api=''):
        self.err_no = 4
        self.msg = msg
        self.remoteip = remoteip
        self.dt = datetime.datetime.now()

