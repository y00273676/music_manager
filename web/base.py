#! /usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import time
import logging
import json, re
import random, hashlib
import datetime

#from lib import des
from tornado import gen
from tornado.concurrent import Future
from lib.defines import *
from lib.session import Session

logger = logging.getLogger(__name__)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class WebBaseHandler(tornado.web.RequestHandler):
    user = None

    def __init__(self, *argc, **argkw):
        super(WebBaseHandler, self).__init__(*argc, **argkw)
        self.session = Session(self.application.session_manager, self)

    def get_current_user(self):
        user = {}
        user['UserNick'] = self.session.get('UserNick')
        user['UserNo'] = self.session.get('UserNo')
        user['UserType'] = self.session.get('UserType')
        user['UserTypeName'] = self.session.get('UserTypeName')
        user['uid'] = self.session.get('uid')
        return user

    def get_user_id(self):
        #return self.get_secure_cookie('uid', 0)
        return self.session.get('uid')

    def get_login_url(self):
        return '/login'

    def check_login(self):
        #if not login, redirect to login page
        self.user = None
        #try use session API
        self.user = self.get_current_user()
        if self.user['uid']:
            return True
        else:
            self.redirect("/login")
            return False

        #uid = self.get_secure_cookie('uid')
        uid = self.get_user_id()
        logger.error('check_login:  uid=%s' % uid)
        #uid = self.get_cookie('userid')
        if uid == None or uid == '':
            self.top_redirect('/login')
        else:
            u = self.get_cache(self.get_session_key(uid));
            logger.error("session value: %s" % u)
            if u and not u == '':
                user = json.loads(u)
                if isinstance(user, dict):
                    self.user = user
                    #print self.user
                    #{u'UserNick': u'', u'UserType': 0, u'UserNo': u'8'}
                    return True
            else:
                logger.error("session timeouted: uid=%s" % uid)
                self.top_redirect('/login')
        return False

    def top_redirect(self, url):
        self.redirect(url)
        #html = "<html><head/><script>alert(window.top.location.toString())</script></html>"
        #self.send_html(html)
        return

    def send_json(self, result, code=200):
        self.set_header("Content-Type", "application/json")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_status(code)
        #import codecs
        #with codecs.open('tmp.txt','w','utf-8') as fp:
               #json.dump(a,fp,ensure_ascii=False,indent=4)
        #_json = json.dumps(result, ensure_ascii=False, indent=4)
        _json = json.dumps(result, cls=MyEncoder, ensure_ascii=False, indent=4)
        #_json = json.dumps(result)
        self.write(_json)
        self.finish()

    def send_xml(self, result, code=200):
        self.set_header("Content-Type", "application/xml")
        if len(result) == 1:
            xml = xmltodict.unparse(result) #dict_to_xml(result)
        else:
            xml = xmltodict.unparse({'root':result})#dict_to_xml({'root': result})
        self.set_status(code)
        self.write(xml)
        self.finish()

    def send_string(self, result, code=200):
        self.set_header("Content-Type", "text/plain")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_status(code)
        self.write(result)
        self.finish()

    def send_html(self, result, code=200):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.set_status(code)
        self.write(result)
        self.finish()
        
    def send_text(self, result, code=200):
        self.set_header("Content-Type", "text/event-stream")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_status(code)
        _json = json.dumps(result, cls=MyEncoder, ensure_ascii=False, indent=4)
        self.write('data: '+_json.replace("\n","").replace("\r","")+'\r\n\r\n')
        self.finish()
    def send_img(self, result, code=200):
        self.set_header("Content-Type", "image/bmp")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_status(code)
        self.write(result)
        self.finish()


    def get_session_key(self, userid):
        return 'session:%s' % userid

    def get_user_cache_key(self, userid):
        return '%s:login' % userid

    def short_desc(self, desc, lenth=10):
        if not desc:
            return ''
        if len(desc) > lenth:
            return desc[0:lenth] + '...'
        else:
            return desc

    def page_info(self, path, total, psize, cur_page):
        '''
        generage a page number information in dict format.

        @params:
            @path: string, the url path which would be refert to
            @total:  total count for items
            @psize:  pagesize, how many items for each page
            @cur_page: page number for current page

        Retuens:
            dict, 

        '''
        pageinfo = {}
        if total % psize:
            pageinfo['totalpage'] = total / psize + 1
        else:
            pageinfo['totalpage'] = total / psize
        pageinfo['currentpage'] = cur_page
        pageinfo['pagesize'] = psize
        pageinfo['path'] = path

        return pageinfo
        #pageinfo['totalitems'] = total

