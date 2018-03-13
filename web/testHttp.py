#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket



if __name__=='__main__':
    ipList = socket.gethostbyname_ex(socket.gethostname())
    print(ipList[2])
