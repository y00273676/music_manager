#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading


threadArrList=[]
def createThread(fnName):
    threadArrList.append(threading.Thread(target=fnName,args=()))