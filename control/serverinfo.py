#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-18 15:22:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import socket  
import json

def get_server_info(ip):  
    address = (ip, 10086)  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    try:
        s.connect(address)  
        str='GetVideoServerStreamStatus\r\n\r\n'
        s.send(str)
        ra = s.recv(4)
#         print 'len', len(ra)
        lenx = ord(ra[3])<<24 | ord(ra[2])<<16 | ord(ra[1])<<8 | ord(ra[0])
#         print 'client:', lenx
        mdata=s.recv(lenx)
       
#         endata=mdata.decode("gbk").encode("utf-8") 
        endata=mdata
#         print 'mdata:', endata
        mjsondata=json.loads(endata)
#         mjsondata={}
        return mjsondata
        
    except Exception, e:
        return 1
    
    s.close() 
