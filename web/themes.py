#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import traceback
import tornado

from tornado import gen
from web.base import WebBaseHandler
from lib.types import try_to_int

from control.themes import get_all_themes

logger=logging.getLogger(__name__)

class ThemesHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            _res = dict(code=0, msg='ok', result=None)

            res = get_all_themes()
            if isinstance(res, dict):
                _res['result'] = res
            self.send_json(_res)
            return
        else:
            raise tornado.web.HTTPError(405)

    @gen.coroutine
    def post(self, op):
        raise tornado.web.HTTPError(405)

