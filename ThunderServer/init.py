#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月6日

@author: yeyinlin
'''
import sys
import time
import signal
import logging
import platform
import multiprocessing
from app import app_service
from app.jobmanager import Mjobmanager
from config.appConfig import AppSet
from common.KtvInfo import hdl_ktvinfo

def config_log(logfile, loglvl = logging.ERROR, console=False):
    '''
        初始化日志配置:
        logfile:  the file which the log would be write in
        loglvl:   log level, logging.ERROR by default
        console:   boolean, if we print the log on stdout
        return:  boolean, True if success
    '''
    try:
        logging.basicConfig(
            level    = loglvl,
            format   = '%(filename)s:%(lineno)-4d[%(levelname)-7s] %(message)s',
            datefmt  = '%m-%d %H:%M',
            filename = logfile,
            filemode = 'w')

        if console:
            # define a Handler which writes INFO messages or higher to the sys.stderr
            console = logging.StreamHandler();
            console.setLevel(logging.INFO);
            # set a format which is simpler for console use
            formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
            # tell the handler to use this format
            console.setFormatter(formatter);
            logging.getLogger(__name__).addHandler(console);
        return True
    except Exception as ex:
        logging.error('Failed to initlize logging config: {0}'.fomart(str(ex)))
        return False

if __name__ == '__main__':
    loglvl = AppSet().GetCloudKtvIniValue("LogLevel")
    if platform.system().lower() == 'linux':
        logfile = '/opt/logs/trans.log'
    else:
        logfile = r'd:\thundertest.log'

    if loglvl.lower() == 'debug':
        config_log(logfile, loglvl=logging.DEBUG, console=True)
    elif loglvl.lower() == 'info':
        config_log(logfile, loglvl=logging.INFO, console=False)
    else:
        config_log(logfile, loglvl=logging.ERROR, console=False)

    i = 10
    while(i > 0):
        dogname = AppSet().get_DogName()
        if dogname:
            hdl_ktvinfo.refresh_ktvinfo()
        else:
            logging.error("Cannot get ktvinfo")
        ktvinfo = hdl_ktvinfo._info
        if dogname and ktvinfo:
            break
        else:
            time.sleep(3)
        i -= 1
        if i == 0:
            logging.error("Failed to get ktvinfo, exiting...")
            sys.exit(1)

    logging.warn("Service initializing...")
    multiprocessing.freeze_support()
    svr = app_service()
    #svr.addapp("public",prints)
    svr.addapp("jobmanager",Mjobmanager)
    svr.startall()
    
