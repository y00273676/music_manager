#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-20 10:34:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import struct
import socket
import fcntl

def getLocalIp(ifname):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(sock.fileno(), 0x8915,struct.pack('256s', ifname[:15]))[20:24])
    except:
        return ""
if __name__=='__main__':
   print getLocalIp("eth0")

    
