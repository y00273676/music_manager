'''
Created on 2017年4月17日

@author: yeyinlin
'''

import time
import queue
import logging
import traceback
import os
from ctypes import *

class logsystem(object):
    #静态的方法
    _ins = None
    logger=queue.Queue()
    isinit=False
    @staticmethod
    def Ins():
        if not logsystem._ins:
            logsystem._ins = logsystem()
        return logsystem._ins
    
    def __init__(self):
        self._ktvid=0
        self._ktvname=""
        self._appver=""
        self._canup=True
    def Logger(self):
        return self.logger
    
    def init(self,dsnkey,ktvid,ktvname,appver):
        if (not dsnkey) or ktvid<=0 or not appver or not ktvname:
            return False
        #TODO 此处为上传的客户端
        self._canup=True
        self._ktvid=ktvid
        self._ktvname=ktvname
        self._appver=appver
        isinit=True
        return True
    def addMlog(self,msg,level,tags=None):
        if not self.isinit or not msg or level<0:
            return False
        log={}
        error={}
        error['Data']={}
        error['msg']=msg
        log['error']=error
        log['level']=level
        log['msg']=msg
        log['tags']={}
        if tags:
            log['tags']=tags
        log['tags']['utime']=time.strftime('%y-%M-%d %H:%M:%S',time.localtime(time.time()))
        if self._logger.qsize()>2000:
            self._logger.get()
        self._logger.put(log)  
    def dispose(self):
        self._isinit=False
        self._canup=False
        self._rc=None
    
    def ansylog(self):
        if(not self._isinit):
            return
        uperr=[]
        cwd=os.path.dirname(os.getcwd())
        start=cwd.split("ThunderServer")[0]
        filename = os.path.join(start+"ThunderServer", "lib\SharpRaven.dll")
        _dll = CDLL(filename)
        
        while self._canup and not self.Logger().empty():
            #TODO停止50ms
            ex=self.Logger().get()
            try:
                self._rc['Logger']=self._ktvid
                self._rc['Release']=self._appver
                self._rc['Compression']=True
                
                if ex['error']:
                    ex['error']['Data']['ktvid']=self._ktvid
                    ex['error']['Data']['ktvname']=self._ktvname
                    
                    _dll.CaptureException(ex.error, None, ex['level'], ex.tags, None, None)
                else:
                    message={}
                    message['error']=ex.msg
                    _dll.CaptureMessage((message), ex['level'], ex.tags, None, None)
            except Exception as e:
                #如果没有上传成功时就需要再添加到队列
                uperr.append(ex)
        
        if len(uperr)>0:
            for item in uperr:
                if self._logger.qsize()<2000:
                    self._logger.put(item)

if __name__ == '__main__':
    pass