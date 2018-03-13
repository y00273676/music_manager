#!/usr/bin/env python
# -*- coding:utf-8 -*-

class app_service(object):
    applist = {}
    def __init__(self):
        pass

    def addapp(self, name, appClass):
        self.applist[name] =  appClass(name)
        pass

    def delapp(self, name):
        self.applist.pop(name)

    def startall(self):
        for app in self.applist.keys():
            if self.applist[app].start():
                print('Success start process: %s' % app)
            else:
                print('failed start process: %s' % app)

    def stopall(self):
        for app in self.applist.keys():
            if self.applist[app].stop():
                print('Success stop process: %s' % app)
            else:
                print('failed stop process: %s' % app)

    def startapp(self, name):
        if name in self.applist.keys():
            return self.applist[name].start()
        else:
            return False

    def stopapp(self, name):
        if name in self.applist.keys():
            return self.applist[name].stop()
        else:
            return True

    def status(self, name=''):
        if name:
            self.applist[name].status()
        else:
            for app in self.applist.keys():
                self.applist[app].status()
