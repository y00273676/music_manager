#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import hashlib
import traceback

from tornado import gen
from web.base import WebBaseHandler
from lib.verifycode import create_validate_code
from io import BytesIO

logger = logging.getLogger(__name__)

class VerifyCodeHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        img, code = create_validate_code(size=(120,30), font_size=20, font_type='static/fonts/NanumGothic.ttf')
        msstream = BytesIO()
        img.save(msstream, "jpeg")
        self.session['verifycode'] = code.lower()
        self.session.save()
        #img.close()
        self.set_header('Content-Type', 'image/jpg')
        self.write(msstream.getvalue())

