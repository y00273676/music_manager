#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

ret_code = {
    #成功
    'Success': 1,
    #参数错误
    'ParamaError': 2,
    #签名错误
    'SignError': 3,
    #请求超时
    'TimeOut': 4,
    }

_def_return = {
    #系统返回值, refer to ret_code
    'code': 1,
    #系统返回值含义
    'msg': '',
    #业务返回值
    'data': {},
    }

def default_return():
    ret = copy.deepcopy(_def_return)
    return ret

