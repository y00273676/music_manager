#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import traceback
import logging
import threading
from tornado import ioloop


class BaseTask(object):
    #Start and stop time, in hour of day
    t_start = 7
    t_end = 20
    #peridically time , by seconds
    t_inteval = 600

    #task name
    name = 'basic'
    #task status
    info = 'initiallzing'
    #running status
    running = False
    #last time to run
    lasttime = 0
    loopfd = None

    def __init__(self, name):
        self.name = name

    def do_run(self):
        '''
        the real things we want to do by this task
        '''
        return True
        pass

    def config(self, start=7, end=20, inteval=600):
        self.t_start = start
        self.t_end = end
        self.t_inteval = inteval

    def start(self):
        if not self.loopfd:
            self.loopfd = ioloop.PeriodicCallback(self.do_run(), self.t_inteval)
        self.running = True
        self.loopfd.start()
        pass

    def stop(self):
        self.loopfd.stop()
        self.running = False

    def status(self):
        if self.running:
            return 'running'
        else:
            return 'stopped'

    def pre_check(self):
        '''
        checking the precondition, dogname, ktvinfo etc...
        '''
        return True

    def check_time(self):
        hour = time.localtime().tm_hour
        if (hour > self.t_start and hour > self.t_end) or (hour < self.t_start and hour < self.t_end):
            #not in time range
            print (" not in hour range, %d - %d : %d" % (self.t_start, self.t_end, hour))
            return False
        if time.time() - self.lasttime > self.t_inteval:
            print (" now: %s  lasttime: %s inteval:%s" % (time.time(), self.lasttime, self.t_inteval))
            #it's time to run again
            return True
        else:
            #not enought interval, continue waiting...
            return False

