#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import datetime
import hashlib
import logging
import traceback
import time
import re

class SingletonMixin(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingletonMixin, cls).__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

class DateTimeUtils(object):
    @classmethod
    def format(cls, date):
        if not date:
            return date
        try:
            dt = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
            return '{d.year}/{d.month}/{d.day} {d.hour}:{d.minute:02}:{d.second:02}'.format(d=dt)
        except:
            return date

def decode_url(url,code_str='utf8'):
    pass
    '''
#     url 转码
#     '''
#     import urllib
#     url=urllib.unquote_plus(urllib.unquote_plus(url.encode(code_str))).decode(code_str)    
#     return url 

def md5(nostr):
    myMd5 = hashlib.md5()
    myMd5.update(nostr.encode("utf8"))
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest.lower()

def parse_command(data_str):
    if not data_str:
        return ''
    
    index = data_str.find(' ')
    if index <= 0:
        return data_str
    return data_str[:index].strip()

def parse_parameter(data_str, paramLen):
    data = data_str
    strSource = data[data.find(':')+1:]
    name = ''
    target = []
    for i in range(paramLen):
        if name == 'SongName:':
            #target[i] = strSource
            target.append(strSource)
        else:
            index = strSource.find(' ')
            if index >= 0:
                target.append(strSource[0:index])
                strSource = strSource[index+1:]
                name = strSource[0:strSource.find(':')+1]
                strSource = strSource[strSource.find(':')+1:]
            else:
                target.append(strSource)
    return target

def int_2_buf(value):
    buf = b'\x00' * 4
    try:
        value = int(value)
        logging.debug(value)
        B4 = value//(256*256*256)
        B3 = value//(256*256)%256
        B2 = value//256%256
        B1 = value%256
        if B1:
            buf = byte_2_str(B1)
        else:
            buf = b'\x00'
        if B2:
            buf = buf + byte_2_str(B2)
        else:
            buf = buf + b'\x00'
        if B3:
            buf = buf + byte_2_str(B3)
        else:
            buf = buf + b'\x00'
        if B4:
            buf = buf + byte_2_str(B4)
        else:
            buf = buf + b'\x00'
    except Exception as ex:
        logging.error('int_2_buf convert excepted')
        logging.error(value)
        logging.error(str(ex))
        logging.error(traceback.format_exc())
    
    return buf

@staticmethod
def byte_2_str(byte):
    tmp = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\x09', b'\x0a', b'\x0b', b'\x0c', b'\x0d', b'\x0e', b'\x0f', \
    b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18', b'\x19', b'\x1a', b'\x1b', b'\x1c', b'\x1d', b'\x1e', b'\x1f', \
    b'\x20', b'\x21', b'\x22', b'\x23', b'\x24', b'\x25', b'\x26', b'\x27', b'\x28', b'\x29', b'\x2a', b'\x2b', b'\x2c', b'\x2d', b'\x2e', b'\x2f', \
    b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x35', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3a', b'\x3b', b'\x3c', b'\x3d', b'\x3e', b'\x3f', \
    b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48', b'\x49', b'\x4a', b'\x4b', b'\x4c', b'\x4d', b'\x4e', b'\x4f', \
    b'\x50', b'\x51', b'\x52', b'\x53', b'\x54', b'\x55', b'\x56', b'\x57', b'\x58', b'\x59', b'\x5a', b'\x5b', b'\x5c', b'\x5d', b'\x5e', b'\x5f', \
    b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6a', b'\x6b', b'\x6c', b'\x6d', b'\x6e', b'\x6f', \
    b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7a', b'\x7b', b'\x7c', b'\x7d', b'\x7e', b'\x7f', \
    b'\x80', b'\x81', b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88', b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e', b'\x8f', \
    b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\x98', b'\x99', b'\x9a', b'\x9b', b'\x9c', b'\x9d', b'\x9e', b'\x9f', \
    b'\xa0', b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7', b'\xa8', b'\xa9', b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf', \
    b'\xb0', b'\xb1', b'\xb2', b'\xb3', b'\xb4', b'\xb5', b'\xb6', b'\xb7', b'\xb8', b'\xb9', b'\xba', b'\xbb', b'\xbc', b'\xbd', b'\xbe', b'\xbf', \
    b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc4', b'\xc5', b'\xc6', b'\xc7', b'\xc8', b'\xc9', b'\xca', b'\xcb', b'\xcc', b'\xcd', b'\xce', b'\xcf', \
    b'\xd0', b'\xd1', b'\xd2', b'\xd3', b'\xd4', b'\xd5', b'\xd6', b'\xd7', b'\xd8', b'\xd9', b'\xda', b'\xdb', b'\xdc', b'\xdd', b'\xde', b'\xdf', \
    b'\xe0', b'\xe1', b'\xe2', b'\xe3', b'\xe4', b'\xe5', b'\xe6', b'\xe7', b'\xe8', b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef', \
    b'\xf0', b'\xf1', b'\xf2', b'\xf3', b'\xf4', b'\xf5', b'\xf6', b'\xf7', b'\xf8', b'\xf9', b'\xfa', b'\xfb', b'\xfc', b'\xfd', b'\xfe', b'\xff'] 

    if byte >= 0 and byte <= 255:
        return tmp[byte]
    else:
        return tmp[0]

# 计算时间差（返回间隔秒数）
def dateDiffInSeconds(date1, date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    timedelta = date2 - date1
    return timedelta.days*24*3600 + timedelta.seconds


# <summary>
# 将版本号转换为20位十进制数
# </summary>
# <param name="version"></param>
# <returns>把1.2.1.57 转换为00001000020000100057</returns>
def VersionConvert(version):
    if version:
        result = ""
        vers = version.split('.')
        vers_len = len(vers)
        if vers_len == 4:
            for i in range(4):
                ver = vers[i]
                t_len = len(str(ver))
                if t_len == 1:
                    result = result + "0000" + ver
                    continue
                elif t_len == 2:
                    result = result + "000" + ver
                    continue
                elif t_len == 3:
                    result = result + "00" + ver
                    continue
                elif t_len == 4:
                    result = result + "0" + ver
                    continue
                elif t_len == 5:
                    result = result + ver
                    continue
                else:
                    raise ValueError('invalid version number')
        return int(result)
    else:
        logging.info('VersionConvert version is None')
    return 0

# <summary>
# 检测URL是否为weixin.qq.com
# </summary>
# <param name="url"></param>
# <returns></returns>
def isWxHost(url):
    reg = re.compile(r"^(http|https)://\w+\.+weixin.qq.com\?/", re.IGNORECASE)
    if reg.match(url):
        return True
    else:
        return False

# <summary>
# 生成时间戳       
# </summary>
# <returns></returns>
def GenerateTimeStamp():
    pass
    '''
    TimeSpan ts = DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0, 0);
    return Convert.ToInt64(ts.TotalSeconds);
    '''

# <summary>
# 生成时间戳       
# </summary>
# <returns></returns>
def GenerateTimeStamp_byutctime(utctime):
    pass
    '''
    TimeSpan ts = utctime - new DateTime(1970, 1, 1, 0, 0, 0, 0);
    return Convert.ToInt64(ts.TotalSeconds);
    '''
def ToDictionary(param,item):
    dict={}
    for a in param:
        if item in a:
            if isinstance(a, dict):
                dict[param[item]]=param
            else:
                dict[param[item]]=param
    return dict 
