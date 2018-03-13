#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging 
import commands

from orm import orm as _mysql

logger = logging.getLogger(__name__)

'''
#commented by yishunli, these code merged into mediaimport, to use the mysqlclient command to load data
def clean_musicinfo():
    sql = "delete from cloud_musicinfo"
    my_session = _mysql.get_session('karaok', True)
    try:
        ret = my_session.execute(sql)
        logger.debug("delete from cloud_musicinfo, return: %s" % ret)
        return ret
    except Exception as e:
        logger.error(traceback.format_exc())
        my_session.rollback()
    finally:
        my_session.close()
    return False

def load_musicinfo_fromfile(fname):
    sql = "load data low_priority infile '%s' replace into table cloud_musicinfo character set utf8 fields terminated by '\\t' enclosed by '\"'" % (fname)
    my_session = _mysql.get_session('karaok', True)
    try:
        ret = my_session.execute(sql)
        logger.debug("load data into cloud_musicinfo, return: %s" % ret)
        return ret
    except Exception as e:
        logger.error(traceback.format_exc())
        my_session.rollback()
    finally:
        my_session.close()
    return False

def update_musicinfo_fromfile(fname):
    sql = "source %s" % (fname)
    my_session = _mysql.get_session('karaok', True)
    try:
        ret = my_session.execute(sql)
        logger.debug("update data into cloud_musicinfo, return: %s" % ret)
        return ret
    except Exception as e:
        logger.error(traceback.format_exc())
        my_session.rollback()
    finally:
        my_session.close()
    return False

'''
