#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月6日

@author: yeyinlin
'''
import sys
if sys.version_info < (3,):
    from urllib2 import urlopen
    from urllib2 import quote,unquote
else:
    from urllib.request import urlopen
    from urllib.parse import quote,unquote

import copy
import hashlib
import traceback
import logging
logger = logging.getLogger(__name__)

class yhttp(object):
    def __init__(self):
        pass

    def get_y(self, murl, outtime=10, ct='utf-8'):
        try:
            req = urlopen(url=murl,timeout=outtime)
            data = req.read().decode(ct)
            #logger.debug(u"get_Y(%s): result:\n%s" % (murl, data.encode('utf8')))
            return data

        except Exception as e:
            logger.error(traceback.format_exc())
            return ""

    def UrlEncode(self, v):
        return quote(v)
    
    def ParamSign(self, param, skey = ""):
        #参数名必须升序排序
        key_list = list(param.keys())
        key_list.sort()
        sb = ''
        sb_querystr = ''
        for i in range(len(key_list)):
            p = key_list[i]
            sb = sb + "{0}={1}".format(p,param[p])
            sb_querystr += "{0}={1}".format(p, quote(param[p]))
            if i < (len(key_list) - 1):
                sb += "&"
                sb_querystr += "&"
        sb += skey
        sign = hashlib.md5(sb).hexdigest()
        return "{0}&sign={1}".format(sb_querystr, sign)

if __name__ == '__main__':
    pass
