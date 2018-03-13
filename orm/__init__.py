#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import random
from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from setting import MYSQL
from control.modbc import get_all_thunder_ini

from orm.database import \
        Medias, \
        MediaDetails, \
        MediaType, \
        Actors, \
        ActorType, \
        MediaManage, \
        MediaFile, \
        Langs, \
        Audios, \
        Carriers, \
        AddMedia, \
        MediaUserSet, \
        BoxSetting,\
        Boxsetting,\
        SystemSetting,\
        ConfiguresSetting,\
        Themes,\
        Skins,\
        Rooms,\
        Configs,\
        FileServers,\
        Servers,\
        ServerGroups,\
        KaraokVersion,\
        MenPaiAdSetting,\
        Boxip,\
        CloudDownLog,\
        AutoPlay,\
        CloudMusicInfo,\
        KtvModules

'''
        OauthBind, \
        RankDatum, \
        RecommendSinger, \
        RecommendSong, \

'''

def create_session(engine):
    if not engine:
        return None
    session = scoped_session(sessionmaker(bind=engine))
    return session()


class ORM(object):
    def __init__(self):
        master = MYSQL['master']
        #alldata = get_all_thunder_ini()
        #ini_master = alldata['mainserver']
        slaves = MYSQL['slaves']
        dbs = MYSQL['dbs']
        schema = 'mysql+pymysql://%s:%s@%s:%d/%s?charset=utf8'
        kwargs = {
            'pool_recycle': 3600,
            'echo': True,
            'echo_pool': True
        }

        self._session = dict(m=dict(),s=dict())

        for db in dbs:
            #master_schema = schema % (ini_master['UserName'],ini_master['Password'],ini_master['DataBaseServerIp'],master['port'],db)
            master_schema = schema % (master['user'],master['passwd'],master['host'],master['port'],db)
            engine = create_engine(master_schema, **kwargs)
            session = create_session(engine)

            self._session['m'][db] = session
            self._session['s'][db] = []

            for slave in slaves:
                slave_schema = schema % (slave['user'],slave['passwd'],slave['host'],slave['port'],db)
                engine = create_engine(slave_schema, **kwargs)
                session = create_session(engine)
                self._session['s'][db].append(session)

        #YSL: Use shorter name:
        self.mediadetails = MediaDetails(self)
        self.actortype = ActorType(self)
        self.actors = Actors(self)
        self.mediatype = MediaType(self)
        self.medias = Medias(self)
        self.cloudmusicinfo = CloudMusicInfo(self)
        self.mediamanage = MediaManage(self)
        self.mediafile = MediaFile(self)
        self.langs = Langs(self)
        self.audios = Audios(self)
        self.carriers = Carriers(self)
        self.addmedia = AddMedia(self)
        self.mediauserset = MediaUserSet(self)
        self.boxsetting=BoxSetting(self)
        self.boxset=Boxsetting(self)
        self.boxipset=Boxip(self)
        self.systemsettinginfo=SystemSetting(self)
        self.configures=ConfiguresSetting(self)
        self.configs = Configs(self)
        self.themes = Themes(self)
        self.skins = Skins(self)
        self.rooms = Rooms(self)
        self.servers = Servers(self)
        self.servergroups=ServerGroups(self)
        self.karaokversion=KaraokVersion(self)
        self.menpaiad=MenPaiAdSetting(self)
        self.downlog = CloudDownLog(self)
        self.fileservers = FileServers(self)
        self.autoplay = AutoPlay(self)
        self.ktvmodules = KtvModules(self)

    def __del__(self):
        self.close()

    @staticmethod
    def instance():
        name = 'singleton'
        if not hasattr(ORM, name):
            setattr(ORM, name, ORM())
        return getattr(ORM, name)

    def get_session(self, db, master=False):

        if not master:
            sessions = self._session['s'][db]
            if len(sessions) > 0:
                return random.choice(sessions)
        return self._session['m'][db]

    def close(self):
        for db in self._session['m']:
            self._session['m'][db].close()
            for session in self._session['s'][db]:
                session.close()


# global, called by handler
orm = ORM.instance()
