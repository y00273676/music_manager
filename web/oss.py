#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import setting
import logging
import tornado
import random
import subprocess
import datetime

from tornado import gen
from lib.types import try_to_int
from web.base import WebBaseHandler

logger = logging.getLogger(__name__)

net_state_0={};
net_tick = 0

def cpu_command():
    p = subprocess.Popen('sar -P ALL 1 1', cwd=None, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    data = {}
    
    id = -1
    step = 0

    name = ''
    value = ''
    
    data['now'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    while True:
        line = p.stdout.readline()
        if not line:
            break
        #print(line)
        if ("PM" in line or 'AM' in line) and 'CPU' not in line:
            id = id + 1
            s = line.split(' ')
            step = 0
            for i in range(4, len(s)):
                if s[i] != '':
                    step = step + 1
                if step == 1:
                    name = 'cpu' + str(id)
                elif step== 2:
                    value = s[i]
                    break

            data[name] = value
    return (data)

#�ڴ���Ϣ
def memory_stat():  
    mem = {}  
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = long(var) * 1024.0
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    return mem  

#CPU��Ϣ
def cpu_stat():
    cpu = []
    cpuinfo = {}
    f = open("/proc/cpuinfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if line == '\n':
            cpu.append(cpuinfo)
            cpuinfo = {}
        if len(line) < 2: continue
        name = line.split(':')[0].rstrip()
        var = line.split(':')[1]
        cpuinfo[name] = var
    return cp

#������Ϣ
def load_stat():  
    loadavg = {}  
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()  
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    loadavg['lavg_15']=con[2]
    loadavg['nr']=con[3]
    loadavg['last_pid']=con[4]
    return loadavg

#��תʱ��
def uptime_stat():
    uptime = {}
    f = open("/proc/uptime")
    con = f.read().split()
    f.close()  
    all_sec = float(con[0])
    MINUTE,HOUR,DAY = 60,3600,86400
    uptime['day'] = int(all_sec / DAY )
    uptime['hour'] = int((all_sec % DAY) / HOUR)
    uptime['minute'] = int((all_sec % HOUR) / MINUTE)
    uptime['second'] = int(all_sec % MINUTE)
    uptime['Free rate'] = float(con[1]) / float(con[0])
    return uptime

#��ȡ��������Ϣ /proc/net/dev
#����dict,��λbyte
def net_stat():
    net = []
    f = open("/proc/net/dev")
    lines = f.readlines()
    f.close()
    net_tick = time.time()
    for line in lines[2:]:
        con = line.split()
        """ 
        intf = {} 
        intf['interface'] = con[0].lstrip(":") 
        intf['ReceiveBytes'] = int(con[1]) 
        intf['ReceivePackets'] = int(con[2]) 
        intf['ReceiveErrs'] = int(con[3]) 
        intf['ReceiveDrop'] = int(con[4]) 
        intf['ReceiveFifo'] = int(con[5]) 
        intf['ReceiveFrames'] = int(con[6]) 
        intf['ReceiveCompressed'] = int(con[7]) 
        intf['ReceiveMulticast'] = int(con[8]) 
        intf['TransmitBytes'] = int(con[9]) 
        intf['TransmitPackets'] = int(con[10]) 
        intf['TransmitErrs'] = int(con[11]) 
        intf['TransmitDrop'] = int(con[12]) 
        intf['TransmitFifo'] = int(con[13]) 
        intf['TransmitFrames'] = int(con[14]) 
        intf['TransmitCompressed'] = int(con[15]) 
        intf['TransmitMulticast'] = int(con[16]) 
        """  
        st = net_state_0[con[0].rstrip(":")]
        print(st)
        if st!=None:
            r = (int(con[1]) - st['ReceiveBytes']) / (net_tick - net_state_0['tick'])
            s = (int(con[9]) - st['TransmitBytes'])/ (net_tick - net_state_0['tick'])
            intf = dict(
                zip(
                    ( 'interface', 'ReceiveRate', 'TransmitRate'),
                    ( con[0].rstrip(":"), r, s )
                )
            )
            net.append(intf)
        
        intf = dict(
            zip(
                ( 'interface', 'ReceiveRate', 'TransmitRate'),
                ( con[0].rstrip(":"), int(con[1]), int(con[9]) )
            )
        )
        net_state_0[con[0].rstrip(":")] = intf
        net_state_0['tick']=net_tick
        """
            intf = dict(
            zip(
                ( 'interface',
                  'ReceiveBytes','ReceivePackets',
                  'ReceiveErrs','ReceiveDrop','ReceiveFifo',
                  'ReceiveFrames','ReceiveCompressed','ReceiveMulticast',
                  'TransmitBytes','TransmitPackets','TransmitErrs',
                  'TransmitDrop', 'TransmitFifo','TransmitFrames',
                  'TransmitCompressed','TransmitMulticast' ),
                ( 
                    con[0].rstrip(":"),
                    int(con[1]),int(con[2]),
                    int(con[3]),int(con[4]),int(con[5]),
                    int(con[6]),int(con[7]),int(con[8]),
                    int(con[9]),int(con[10]),int(con[11]),
                    int(con[12]),int(con[13]),int(con[14]),
                    int(con[15]),int(con[16]), )
            )
        )
        """
        
    
    print(net)

    return net

#���̿ռ�ʹ��
#ʹ������python���ú����dict,��λbyte
def disk_stat():
    import os
    hd={}
    disk = os.statvfs("/")
    hd['available'] = disk.f_bsize * disk.f_bavail
    hd['capacity'] = disk.f_bsize * disk.f_blocks
    hd['used'] = disk.f_bsize * disk.f_bfree
    print(hd)
    return hd

class OsHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'stat.do':
            p  = self.get_argument('p', '')
            ret = {}
            
            if p=='cpu':
                #net_stat()
                ret = cpu_command()
            elif p=='memory':
                ret['code'] = 0
                ret['data'] = random.randint(0, 100)
                ret['now'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            else:
                ret['code'] = 0
                ret['value'] = '65'

            self.send_json(ret)

    @gen.coroutine
    def post(self, op):
        
        if op == 'stat.do':
            p  = self.get_argument('p', '')
            ret = {}
             
            if p=='cpu':
                #net_stat()
                ret = cpu_command()
            elif p=='memory':
                ret['code'] = 0
                ret['data'] = random.randint(0, 100)
                ret['now'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            else:
                ret['code'] = 0
                ret['value'] = '65'
 
            self.send_json(ret)
 
        else:
            raise tornado.web.HTTPError(405)


