#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from web.base import WebBaseHandler
from lib.types import try_to_int
from tornado import web, gen

from tsjob.cloudlogin import CloudLoginTask
from tsjob.jobmanager import JobManager

logger = logging.getLogger(__name__)

class JobHandler(WebBaseHandler):
    def get(self, op):
        _res = {'code':1, 'msg':'ok', 'result':{}}
        if op == 'list':
            info = JobManager.status()
            _res['result'] = dict(matches=info, total=len(info))
            self.send_json(_res)
            return
        else:
            raise web.HTTPError(405)

    def post(self, op):
        raise web.HTTPError(405)
