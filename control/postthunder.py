#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:25:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import urllib2
import urllib
import json
import traceback
import logging

logger=logging.getLogger(__name__)
def postHttp(ip,mjsondata,ttype):
    starturl="http://"
    endurl=":8888/thuchange"
    url=starturl+ip+endurl
#     url="http://10.0.3.111:8080/thuchange"
  #定义要提交的数据
  #url编码
    dumpsj=json.dumps(mjsondata)
    tdata=dict(mtype=ttype,mdata=dumpsj)
    postdata=urllib.urlencode(tdata)
    print postdata
  #enable cookie
    try:
        request = urllib2.Request(url,postdata)
        response=urllib2.urlopen(request,timeout=5)
        if ttype=="2":
            return response.read()
        elif ttype=="3":
            return response.read()
        elif ttype=="4":
            return 0
        elif ttype=="5":
            return response.read()
        elif ttype=="6":
            return response.read()
        elif ttype=="7":
            return response.read()
        print response.read()
    except Exception, e:
        logger.error(traceback.format_exc(e))
        return 1
    
   
    return 0