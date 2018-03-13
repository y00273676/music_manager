#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
import os
import json
import commands
from tornado import gen
from lib.types import try_to_int
from web.base import WebBaseHandler
from orm.mm import addMessage
from control.getfileservice import get_all as getAllIp

logger = logging.getLogger(__name__)

messageList=[]

class websource(WebBaseHandler):
    
    def sendPost(url, data):  
        req = urllib2.Request(url)  
        data = urllib.urlencode(data)  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
        response = opener.open(req, data)  
        return response.read()  
    
    @gen.coroutine
    def get(self):
        objArr = []
        try:
            while(len(messageList)>0):
                obj = messageList.pop(0)
                obj['_tMark'] = time.time()
                objArr.append(obj)
        except:
            pass
        self.send_text(objArr)
    @gen.coroutine
    def options(self):
        self.send_json('')
        
    @gen.coroutine
    def post(self):
        ret={}
        ret['code']=1
        obj = json.loads(self.request.body)
        try:
            if(obj.has_key("id")):
                messageList.append(obj)
            else:
                obj['unRead']=0
                obj['time']=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                if not 'ip' in obj:
                    obj['ip']=''
                if not 'app' in obj:
                    obj['app']=''
                obj['id'] = addMessage(obj)
                outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")
                myIpList=outp.split('\n')
                ipList = getAllIp()
                if ipList == None:
                    ret['text']='当前未设置服务器组ip'
                    messageList.append(obj)
                else:
                    for matObj in ipList['matches']:
                        ip = matObj['FileServer_IpAddress']
                        bol = False
                        for i in myIpList:
                            if i==ip:
                                bol=True
                        if (bol):
                            messageList.append(obj)
                        else:
                            try:
                                sendPost('http://'+str(ip)+':8888/websource', obj)
                            except:
                                pass
        except:
            ret['error']=traceback.format_exc()
        ret['code']=0
        self.send_json(ret)
        
def executeSendMessage(obj):
    obj['unRead']=0
    obj['time']=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    obj['ip']=''
    obj['app']=''
    obj['id'] = addMessage(obj)
    messageList.append(obj)
    return obj
        
            
        
        
    

    
