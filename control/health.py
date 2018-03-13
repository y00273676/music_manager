#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import traceback

from lib import http
from orm import orm as _mysql

logger = logging.getLogger(__name__)

def get_all_table_status():
    tbs = []
    session = _mysql.get_session('karaok')
    try:
        ts = session.execute("show tables").fetchall()
        tblist = []
        for tb in ts:
            tblist.append(tb[0])
        tblist = ','.join(tblist)
        status = session.execute("check table %s" % tblist).fetchall()
        for row in status:
            t = {}
            t['name'] = row[0][7:]
            t['op'] = row[1]
            t['msgtype'] = row[2]
            t['msg'] = row[3]
            tbs.append(t)
    except Exception as ex:
        logger.error(traceback.format_exc())
        pass
    finally:
        session.close()
    return tbs

def repair_db_table(tname):
    res = '数据库表%s修复成功' % tname
    session = _mysql.get_session('karaok')
    try:
        ts = session.execute("select ENGINE from information_schema.TABLES where TABLE_SCHEMA='karaok' and TABLE_NAME='%s'" % tname).fetchall()
        engine = ts[0][0]
        if engine != 'MyISAM':
            return "%s类型的数据表不支持修复" % engine
        ts = session.execute("repair table %s" % tname).fetchall()
        if len(ts) > 0:
            if ts[0][3] != 'OK':
                res = ts[0][3]
        else:
            res = "没有找到要修复的数据表"
    except Exception as ex:
        res = str(ex)
        logger.error(traceback.format_exc())
        pass
    finally:
        session.close()
    return res

