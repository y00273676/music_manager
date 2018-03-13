#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
#from control.user import get_by_id
from menuconf.index import index_menu
#from mqtt import dmsapi
#from control import api as _apictl
from web.base import WebBaseHandler

logger = logging.getLogger(__name__)

class IndexHandler(WebBaseHandler):
    @tornado.gen.coroutine
    #@tornado.web.authenticated
    def get(self):
        self.redirect('/static/index.html')

    def create_menu(self, menu_json):
        if not isinstance(menu_json, list):
            return ''
        bs = u''
        bs += u"<ul id=\"main-nav\" class=\"nav nav-tabs nav-stacked\">\n" \
                "<li class=\"active\">\n<a href=\"index\">\n<i class=\"glyphicon " \
                "glyphicon-th-large\"></i>首页 </a>\n</li>"
        for menu in menu_json:
            if menu['rule'] == menu['user'] == '':
                pass
            else:
                allow_types = menu['rule'].split(',')
                allow_users = menu['user'].split(',')
                logger.error("login userinfo: %s" % str(self.user))
                #logger.error("allow usertypes: %s" % allow_types)
                #logger.error("allow users: %s" % allow_users)
                #if user permited by 'userno' or 'usertype', show this menu.
                if str(self.user['UserType']) in allow_types or self.user['UserNo'] in allow_users:
                    pass
                else:
                    logger.error('user don\'t have permission user:%s(%s),type:%s(%s)' % (self.user['UserNo'], type(self.user['UserNo']), self.user['UserType'], type(self.user['UserType'])))
                    continue

            chevron_icon = u""
            if 'chevrondownicon' in menu.keys() and not menu['chevrondownicon'] == '':
                chevron_icon = u"<span class=\"%s\">" % menu["chevrondownicon"]

            str_li = ""
            submenus = menu["towlevemenu"]
            if isinstance(submenus, list) and len(submenus) > 0:
                for submenu in submenus:
                    allow_types = submenu['rule'].split(',')
                    allow_users = submenu['user'].split(',')
                    #if user permited by 'userno' or 'usertype', show this menu.
                    if str(self.user['UserType']) in allow_types or self.user['UserNo'] in allow_users:
                        pass
                    else:
                        continue;

                    requesturl = ''
                    if "host" in submenu.keys():
                        requesturl += submenu['host']
                    if "address" in submenu.keys():
                        requesturl += submenu['address']

                    _target = ''
                    if not requesturl == '' and not requesturl == '#':
                        _target = 'sysMain'

                    str_li += u"<li>\n<a href=\"%s\" target=\"%s\">\n<i class=\"%s\"></i>%s</a>\n</li>" \
                            % (requesturl, _target, submenu["icon"], submenu["name"])

            bs += u"<li>\n<a href=\"#%s\" class=\"nav-header collapsed\" data-toggle=\"collapse\" aria-expanded=\"false\">\n" \
                    "<i class=\"%s\"></i>%s %s</span></a>\n<ul id=\"%s\" class=\"nav nav-listcollapse secondmenu collapse in" \
                    "style=\"height: 0px;\" aria-expanded=\"false\">%s</li></ul>\n" % \
                    (menu["towlevemenuid"], menu["icon"], menu["name"], chevron_icon, menu["towlevemenuid"], str_li)
        bs += u"</ul>"
        return bs
