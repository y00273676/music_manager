#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import hmac
import base64
import setting
import logging
import hashlib
import traceback
import datetime

from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.defines import retCode
from setting import cloudStorage
from lib.types import try_to_int

logger = logging.getLogger(__name__)

class StorageHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        if not self.check_login():
            return
        fname = self.get_argument('filename', '')
        rtype = self.get_argument('type', '')
        if rtype == 'signKey':
            sign_info = self.getSignKey(fname)
            self.send_json(sign_info)
        elif rtype == 'AK':
            access_key = self.getAccessKey()
            self.send_string(access_key)
            pass
        elif rtype == 'fileurl':
            fpath = self.getPath(fname)
            self.send_string(fpath)
            pass
        elif rtype == 'BucketName':
            bname = self.getBucket()
            self.send_string(bname)
            pass
        elif rtype == 'downurl':
            url = self.getURL(fname)
            self.send_string(url)
            pass
        else:
            raise tornado.web.HTTPError(405)

    def getSignKey(self, name):
        now = datetime.datetime.now() + datetime.timedelta(seconds=30 * 60)
        timestr = now.strftime("%Y-%m-%dT%H:%M:%S.000Z").strip()

        policy = "{\"expiration\": \"" + timestr + "\","\
                "\"conditions\": ["\
                "{\"acl\": \"public-read\" },"\
                "{\"bucket\": \"" + cloudStorage['bucketName'] + "\" },"\
                "{\"key\":\"" + name.strip() + "\"},[\"starts-with\", \"$name\", \"\"],]}";


        #encodestring() return multilines string which will contain '\n'
        #we need strip all the '\n'
        p = base64.encodestring(policy).replace('\n', '')
        sign = base64.encodestring(hmac.new(cloudStorage['SK'], p, hashlib.sha1).digest()).strip()

        ret = {}
        ret["sign"] = sign;
        ret["policy"] = p;
        return ret

    def getAccessKey(self):
        return cloudStorage['AK']

    def getBucket(self):
        return cloudStorage['bucketName']

    def getPath(self, fileMd5name):
        #extendName = Path.GetExtension(fileMd5name).ToLower();
        #fileMD5Value = Path.GetFileNameWithoutExtension(fileMd5name);
        fileMD5Value, extendName = os.path.splitext(fileMd5name)

        path = ""
        extendName = extendName.lower()
        #for images
        if extendName in [".jpg", ".png", ".bmp"]:
            path = cloudStorage['imagePath']
        #for theme packages
        elif extendName == ".zip":
            path = cloudStorage['themePath']
        #for video resource
        elif extendName in [".mpg", ".ts"]:
            path = cloudStorage['videoPath']
        #for android app packages
        elif extendName == ".apk":
            path = cloudStorage['apkPath']

        if path == '':
            return ''
        else:
            today = datetime.datetime.now()
            timestr = today.strftime("%Y-%m")
            url = "%s/%s/%s%s" % (path, timestr, fileMD5Value, extendName)
            return url

    def getURL(self, filePath):
        fpath = 'http://%s.kssws.ks-cdn.com/%s' % (cloudStorage['bucketName'], filePath)
        return fpath
