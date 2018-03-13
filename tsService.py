#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define,options,parse_command_line
from setting import app_conf, session_conf
from lib.session import SessionManager
from handler.tsTask import tsServiceTask
import logging
import signal

define('port', default=80, help='listen port')
define('debug', default=False, help='debug mode')
#define('log_file_prefix', default='tsService.log', help='log file path')
define('log_to_stderr ', default=False, help='')
define('log_file_max_size ', default=1024, help='')
define('cookie_secret', type=str,
        default='f28e91bc2878a5ac6006e0a119b45a2c',
        help="signing key for secure cookies")

tornado.options.parse_command_line()

URLS = [
    (r'.*',
    (r'/', 'handler.index.indexHandler'),
    (r'/tasks/?(list|confirm)?', 'handler.index.tasksHandler'),
    )
]

template_path=app_conf['template_path']
from web import UI_MODULES

class Application(tornado.web.Application):
    def __init__(self):
        # to sing the params
        self.appkey = ''
        self.logger = logging.getLogger(__name__)
        settings = {
            'debug': options.debug,
            'gzip': True,
            'static_path': app_conf['static_path'],
            'template_path': app_conf['template_path'],
            'cookie_secret': options.cookie_secret,
            'ui_modules': UI_MODULES
        }
        self.conf = app_conf
        #self.appkey = self.conf['appkey']
        self.session_manager = SessionManager(session_conf["session_secret"],
                session_conf["store_options"], session_conf["session_timeout"])

        tornado.web.Application.__init__(self,**settings)
        for spec in URLS:
            host = spec[0]
            patterns = spec[1:]
            self.add_handlers(host,patterns)

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = Application()
    sockets = tornado.netutil.bind_sockets(options.port)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.add_sockets(sockets)
    tornado.ioloop.PeriodicCallback(tsServiceTask.schedule, 10 * 1000).start()
    tornado.ioloop.IOLoop.current().start()
    logging.info('Exit')
