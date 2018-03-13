#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import json
import socket
import hashlib
import threading
import traceback
import datetime
import codecs
import sys
if sys.version_info < (3,):
    from urllib import unquote
else:
    from urllib.parse import unquote


def getSignedUrl(url, param):
    param = param + '&time=' + str(int(time.time()));

    if url.startswith('http://open.ktv.api.ktvdaren.com'):
        sign = hashlib.md5((param + '6f9c625e6b9c11e3bb1b94de806d865').encode()).hexdigest()
    else:
        sign = hashlib.md5((unquote(param) + '').encode()).hexdigest()
    return url + param + '&sign=' + sign;

def GetStrValue(strSource,targets):
    pass
