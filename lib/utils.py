#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import datetime

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
    '''
    url 转码
    '''
    import urllib
    url=urllib.unquote_plus(urllib.unquote_plus(url.encode(code_str))).decode(code_str)    
    return url 

