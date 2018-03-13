#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import redis
import commands
from setting import REDIS as _redisconf

class RedisCached(object):
    def __init__(self, host, port, db):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def __del__(self):
        self.close()

    def close(self):
        pass

    def __getattr__(self, attr):
        return getattr(self.client, attr)

_defaultredis = RedisCached(_redisconf['host'], _redisconf['port'], _redisconf['db'])
