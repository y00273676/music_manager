#! /usr/bin/env python
# -*- coding:utf-8 -*-
import copy

'''
wish these defines can lead all APIs to response a unify data format.
'''
retCode = {
    # 失败
    'ERROR': 0,
    # 成功
    'SUCCESS': 1,
    # 参数错误
    'PARAMETERERROR': 2,
    # 签名错误
    'SIGNERROR': 3,
    # 请求超时
    'TIMEOUT': 4,
}

_def_result = {
    #系统返回值, refer to ret_code
    'code': 0,
    #系统返回值含义
    'msg': '',
    #业务返回值
    'result': None,
    }

def default_result():
    ret = copy.deepcopy(_def_result)
    return ret

