#!/usr/bin/python

import os
import sys
import json
import shutil
import commands
import traceback
import logging as logger


VIDEO_MOUNT_POINT = '/video'
cfg_file = '/etc/tstab'
svr_cfg_file = '/opt/thunder/etc/server.json'

def loger_init():
    #logfile = '/var/log/thunder_disk.log'
    logfile = '/home/thunder/thunder_disk.log'
    logger.basicConfig(
            level    = logger.WARNING,
            format   = '%(filename)s:%(lineno)-4d[%(levelname)-7s] %(message)s',
            datefmt  = '%m-%d %H:%M',
            filename = logfile,
            filemode = 'w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logger.StreamHandler();
    console.setLevel(logger.INFO);
    # set a format which is simpler for console use
    
#     formatter = logger.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
#     console.setFormatter(formatter);
#     logger.getLogger('').addHandler(console);


def get_mount_points():
    mp = {}
    lines = open('/proc/mounts').readlines()
    for line in lines:
        if line.startswith('/dev/sd'):
            ar = line.split(' ')
            if len(ar) > 2:
                _, dev = os.path.split(ar[0])
                _, path = os.path.split(ar[1])
                #path = ar[1]
                mp[dev] = path
    return mp

mount_points = get_mount_points()

def list_all_disk():
    fslist = get_fs_status()
    disks = {}
    l_fs = blkid()
    devpath = '/sys/block'
    for dev in os.listdir(devpath):
        if dev.startswith('sd'):
            di = {}
            di['name'] = dev
            video_dev = "%s5" % dev
            if video_dev in mount_points.keys():
                di['is_mount'] = True
                di['mount'] = mount_points[video_dev]
            else:
                di['mount'] = video_dev
                di['is_mount'] = False
            if video_dev in l_fs.keys():
                di['fstype'] = l_fs[video_dev]['type']
                di['label'] = l_fs[video_dev]['label']
            else:
                di['fstype'] = 'unknown'
                di['label'] = 'unknown'
            _, di['phyaddr'] = os.path.split(os.path.realpath(os.path.join(os.path.join(devpath, dev), 'device')))
            di['size'] = get_dev_size(video_dev)
            if di['size'] < 1900000: #smaller than 2T, not a video disk
                continue

            if "/dev/%s" % dev in fslist.keys():
                fs = fslist["/dev/%s" % dev]
                di['size'] = fs['size']
                di['used'] = fs['used']
                di['left'] = fs['left']
                di['percent'] = fs['percent']
                di['mp'] = fs['mp']
            elif "/dev/%s5" % dev in fslist.keys():
                fs = fslist["/dev/%s5" % dev]
                di['size'] = fs['size']
                di['used'] = fs['used']
                di['left'] = fs['left']
                di['percent'] = fs['percent']
                di['mp'] = fs['mp']
 
            #di['partitions'] = {}
            #for part in os.listdir(os.path.join(devpath, dev)):
            #    if part.startswith(dev):
            #        di['partitions'][part] = get_dev_size(part)
            disks[di['phyaddr']] = di
    return disks

def get_fs_status():
    output = commands.getoutput('df -h | grep "/video/disk"')
    outputList = output.split('\n');
    fslist = {}
    if(output!=""):
        for data in outputList:
                data = ' '.join(data.split())
                if data != "":
                    dataList = data.split(' ');
                    optDisc = {}
                    #optDisc['dev'] = dataList[0]
                    optDisc['size'] = dataList[1]
                    optDisc['used'] = dataList[2]
                    optDisc['left'] = dataList[3]
                    optDisc['percent'] = dataList[4]
                    optDisc['mp'] = dataList[5]
                    fslist[dataList[0]] = optDisc
    print(fslist)
    return fslist

def get_dev_size(dev):
    '''
    return: unit MB
    '''
    size = 0
    try:
        if len(dev) > 3:
            disk = dev[0:3]
            size = open('/sys/block/%s/%s/size' % (disk,dev)).read()
        else:
            size = open('/sys/block/%s/size' % dev).read()
        size = int(size)
        size = size * 512 / 1024 / 1024
    except:
        logger.error(traceback.format_exc())
        logger.error('Failed to get disk size: %s' % dev)
    return size

def blkid():
    ret_list = {}
    import re
    cmd = 'blkid'
    ret, out = commands.getstatusoutput(cmd)
    if ret:
        logger.error('Failed to get disk list info: %s \n%s' % (cmd, out))
    for line in out.split('\n'):
        logger.debug(line)
        #if line.startswith('/dev/sda'):
        #    continue
        index = line.find(':')
        if index > 0:
            block = line[:index]
            if block[-1:].isdigit():
                if block[-1:] != '5':
                    continue
                #block = block[5:8]
                #ret_list[block] = {'label':'', 'type':''}
                #continue
            block = block[5:]
            ret_list[block] = {'label':'', 'type':''}
            info = line[index+1:]
            kvs = re.findall('([A-Za-z0-9]*="[A-Za-z0-9 -\.]*")', info)
            for kv in kvs:
                kvarr = kv.split('=')
                if kvarr[0].upper() == 'LABEL':
                    ret_list[block]['label'] = kvarr[1].strip().strip('"')
                #elif kvarr[0].upper() == 'PARTLABEL':
                #    ret_list[block]['partlabel'] = kvarr[1].strip().strip('"')
                elif kvarr[0].upper() == 'TYPE':
                    ret_list[block]['type'] = kvarr[1].strip().strip('"')
            #if ret_list[block]['type'] == 'ext4':
            #    ret_list[block]['status'] = 'yes'
            #else:
            #    ret_list[block]['status'] = 'no'
    return ret_list 

def get_all_disk_info():
    return list_all_disk()

def format_disk(key):
    '''
    useless now
    '''
    return 

if __name__ == '__main__':
    loger_init()
    from pprint import pprint

    mount_point = VIDEO_MOUNT_POINT
    disk_cfg = get_all_disk_info()
    
    pprint (disk_cfg)
    pprint (mount_points)
    pprint(blkid())


