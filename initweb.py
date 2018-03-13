#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define,options,parse_command_line
from setting import app_conf, session_conf
from lib.session import SessionManager
from tsjob.jobmanager import JobManager
import logging
import signal

define('port', default=80, help='listen port')
define('debug', default=True, help='debug mode')
# define('log_file_prefix', default='ktv_tv.log', help='log file path')
#define("logging", default="warning",
#        help=("Set the Python log level. If 'none', tornado won't touch the "
#            "logging configuration."), metavar="debug|info|warning|error|none")
define('log_to_stderr ', default=True, help='')
define('log_file_max_size ', default=1024, help='')
#define('log_file_num_backups', default=10, help='')
define('cookie_secret', type=str,
        default='thunder#!$!(@^',
        help="signing key for secure cookies")

tornado.options.parse_command_line()

URLS = [
    (r'.*',
    (r'/dl/?(add|remove|pause|pauseall|resume|stop|stopall|start|startall|list|status)?', 'web.aria2.Aria2Handler'),
    (r'/clmusic/?(list|search|info|rtdl|dlog)?', 'web.cloudmusic.CloudMusicHandler'),
    #(r'/sphinx/media', 'web.sphinx_search.MediaHandler'),
    #(r'/sphinx/key', 'web.sphinx_search.KeywordHandler'),
    (r'/job/list', 'web.job.JobHandler'),
    (r'/test','web.test.TestHandler'),
    (r'/mediadetails/?(list|count|upload)?', 'web.mediadetails.mediadetails'),
    (r'/mediatype/?(list|update)?', 'web.mediatype.mediatype'),
    (r'/actors/?(list|count|add|update)?', 'web.actors.actors'),
    (r'/actortype/?(list)?', 'web.actortype.actortype'),
    (r'/medias/?(list|count|add|getNo|delete|export|bylang|click|bytag|lostfiles|uselessfiles)?', 'web.medias.medias'),
    (r'/mediamanage/?(list|count|add)?', 'web.mediamanage.mediamanage'),
    (r'/mediafile/?(list|count|upload|add|uploads|exists)?', 'web.mediafile.mediafile'),
    (r'/languages/?(list|update|add)?', 'web.languages.languages'),
    (r'/audios/?(list)?', 'web.audios.audios'),
    (r'/carriers/?(list)?', 'web.carriers.carriers'),
    (r'/addmedia/?(list|add|del)?', 'web.addmedia.addmedia'),
    (r'/mediauserset/?(list|add|exchange|del|max)?', 'web.mediauserset.mediauserset'),
    (r'/sql/?(addMusic|deleteMusic|addMusicType|addActor|selectMediasSequence|selectMediasSequenceCount|getMediasInfo|updateOrderCount|getMediasNoFromFileName|uploadImportTxt|parseImportTxt|scanVideos|checkDisk|cloud_batch_add|get_disk_stat|get_file_list|deleteAllData|getFileOutput|onlyParseText|selectMediaTypeFromMediaDetailsCount|selectMediaDetailsForType|checkFiles|matchingDisk|scpFile|addmediaToFiles|updateMediaDetailsCount|login|get_file_listSize|getMediaFileCountFromIp|notFindFileExport|getAddMediaFileFormScpOtherService|getIsAddData|importLyricText|setUnRead|selectMessage|selectAllDisk|getDiskListSize|get_disk_statInfo|openFile|get_all_disk_info|format_disk|selectConfigures55|setConfigures55|deleteMediaUserSet|selectAdvertisementIdList|selectAllAddMedia|executeSendMessage|getOtherFileList|getLostFileList|seachFile|deleteDiskFile|upfilepath|getTime|log|logConsole|updateNullData|deleteNullData)?', 'web.sql.sql'),
    (r'/fileservers/?(list|listAll)?', 'web.fileservers.fileservers'),
    (r'/servers/?(ls|servicerestart|servicestop|list|add|del|update|filecount|listdisk|listdir|count)?', 'web.servers.ServersHandler'),
    (r'/websource?', 'web.websource.websource'),
    (r'/oss/?(stat.do)?', 'web.oss.OsHandler'),
    (r'/ktvbox','web.ktvbox.BoxHandler'),
    (r'/rooms/?(setting|add|update|del|list|show|flush|sync)','web.rooms.RoomsHandler'),
    (r'/themes/?(add|update|del|list|local)','web.themes.ThemesHandler'),
    (r'/skins/?(add|update|del|list|local)','web.skins.SkinsHandler'),
    (r'/boxsetting','web.ktvbox.SettingHandler'),
    (r'/androidbox','web.androidbox.AndBoxHandler'),
    (r'/fangtai','web.fangtai.FangTaiHandler'),
    (r'/boxs','web.boxs.BoxsHandler'),
    (r'/isset','web.issetting.InitSetHandler'),
    #(r'/systemset','web.systemsetting.SystemSetHandler'),
    (r'/ktvsetting','web.ktvsetting.KtvSettingHandler'),
    (r'/dog/?(show|get|upfile|setpwd|delpwd)?','web.sercrtdog.DogHandler'),
    (r'/fujia','web.fujiasetting.FujiaHandler'),
    (r'/menpai','web.menpai.MenpaiHandler'),
    (r'/thuchange','web.thuchange.ChangeHandler'),
    (r'/sqlimport','handler.media.mediaParseHandler'),
    (r'/sqlupload','handler.media.mediaUploadHandler'),
    (r'/config/?(list|update|get)?','web.config.ConfigHandler'),
    (r'/getMediasInfo','handler.media.getmediainfoHandler'),
    (r'/mediaupdate','handler.media.updatemediaHandler'),
    (r'/updatenullmedia','handler.media.deletenullHandler'),
    (r'/search', 'handler.media.searchlHandler'),
    (r'/searchcount', 'handler.media.searchcountHandler'),
    (r'/mediadel', 'handler.media.mediadelHandler'),
    (r'/loop/?(list|add|del|count|exchange)?','handler.media.loopHandler'),
    (r'/looptype/?(set|del|get)?','handler.media.looptypeHandler'),
    (r'/media/get_status', 'handler.media.statusHandler'),
    (r'/dbchk/?(status|check|repair)?','web.health.DBCheck'),
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
    JobManager.start()
    tornado.ioloop.IOLoop.current().start()
    logging.info('Exit')
