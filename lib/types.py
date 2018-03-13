#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import string
import datetime
import traceback
import logging

logger = logging.getLogger(__name__)
def try_to_int(digi_str, default=-1):
    '''
    try to parse a string number to integer
    '''
    
    try:
        if digi_str and digi_str.isdigit():
            digi_str = int(digi_str)
        else:
            return default
    except Exception as ex:
        logger.error(traceback.format_exc())
        logger.error('Failed to convert %s' % str(ex))
        return default
    return digi_str

def try_to_long(digi_str):
    '''
    try to parse a string number to long
    note: the 0 not indicates an invalid string
    '''
    try:
        return string.atol(digi_str)
    except Exception as ex:
        logger.error(traceback.format_exc())
        logger.error('Failed to convert %s' % str(ex))
        return 0

def try_to_decimal(digi_str):
    ''' convert string value to decimal (float)
    '''
    try:
        return string.atof(digi_str)
    except Exception as ex:
        logger.error(traceback.format_exc())
        logger.error('Failed to convert %s' % str(ex))
        return -1

def try_to_date(date_str):
    '''try parse 'xxxx-xx-xx' type string to date
    '''
    try:
        date_str = date_str.replace('/', '-')
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as ex:
        logger.error(traceback.format_exc())
        logger.error('Failed to convert %s' % str(ex))
        return datetime.datetime(1970, 1, 1).date()

def try_to_datetime(date_str):
    '''try parse 'xxxx-xx-xx xx:xx:xx' type string to datetime
    '''
    try:
        date_str = date_str.replace('/', '-')
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as ex:
        logger.error(traceback.format_exc())
        logger.error('Failed to convert %s' % str(ex))
        return datetime.datetime(1970, 1, 1)

def is_date(date_str):
    #正则匹配日期格式20160708 201678 2016-07-08 2016/07/08 
    p = re.compile(r'^(\d{4})[-./]?((?:[0-1]?|1)[0-9])[-./]?((?:[0-3]?|[1-3])[0-9])?$')
    match = p.match(date_str)
    if match:
        return True
    else:
        return False

def is_mobile(phone_no):
    '''
    '''
    #正则匹配电话号码
    #p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    p = re.compile('^1[358]\d{9}$|^147\d{8}|^170\d{8}')
    match = p.match(phone_no)
    if match:
        return True
    else:
        return False

def is_email(email):
    #正则匹配邮箱和电话号码
    #p = re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+)')
    p = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
    match = p.match(email)
    if match:
        return True
    else:
        return False

def remove_empty_element(tlist):
    if not isinstance(tlist, list):
        return []
    index_list = []
    index = 0
    for sub in tlist:
        if not sub:
            index_list.append(index)
        index += 1
    index_list.reverse()

    for sub in index_list:
        tlist.pop(sub)
    return tlist

def is_safe_pwd(pwd, minlen, maxlen):
    '''
    check a password, require number + charactors, and lenth between minlen and maxlen.
    '''
    pwd_l = len(pwd)
    if pwd_l >= minlen and pwd_l <= maxlen:
        if re.search(r'[a-zA-Z]',pwd) and re.search(r'[0-9]',pwd):
            return True
    return False


