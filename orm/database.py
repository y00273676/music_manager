#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import logging
import datetime
import traceback
import time
from sqlalchemy import or_,text,and_
from sqlalchemy.orm import class_mapper
from functools import partial
from sqlalchemy import func, or_, not_
from models import \
            M_Medias, \
            M_MediaDetails, \
            M_ActorType, \
            M_Actors, \
            M_MediaType, \
            M_MediaManage, \
            M_MediaFile, \
            M_Langs, \
            M_Audios, \
            M_Carriers, \
            M_AddMedia, \
            M_MediaUserSet, \
            M_BoxSetting,\
            M_Boxsetting,\
            M_SystemSettingInfo,\
            M_Configures,\
            M_Themes,\
            M_Skins,\
            M_Rooms,\
            M_Configs,\
            M_FileServers,\
            M_Servers,\
            M_ServersGroups,\
            M_KaraokVersions,\
            M_MenPaiAdSettings,\
            M_Boxip,\
            M_CloudDownLog,\
            M_AutoPlay,\
            M_CloudMusicInfo,\
            M_KtvModuleVer

from setting import MYSQL
#import settings

db_name = MYSQL['dbs'][0]
#db_name = 'ktvcommon'

logger = logging.getLogger(__name__)

def model2dict(model):
    if not model:
        return {}
    fields = class_mapper(model.__class__).columns.keys()
    return dict((col, getattr(model, col)) for col in fields)

def model_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return model2dict(ret)
    return wrap

def models_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret:
            return partial(map, model2dict)(ret)
        else:
            return None
    return wrap

class Base(object):

    def __init__(self, orm):
        self.orm = orm

    def models_to_list(self, models):
        ret = []
        for model in models:
            data = dict((key, getattr(model, key)) for key in model.keys())
            ret.append(data)
        return ret

class TVAPPBase(Base):
    @property
    def master(self):
        return self.orm.get_session(db_name, master=True)

    @property
    def slave(self):
        return self.orm.get_session(db_name, master=True)

class MediaDetails(TVAPPBase):
    @models_to_list
    def get_by_all(self, page,psize,text,type):
        start = (page - 1) * psize
        try:
            query = self.slave.query(M_MediaDetails).join(M_Medias,M_MediaDetails.Media_ID == M_Medias.Media_ID)
            if type == None or type == '1':
                query = query.filter(M_Medias.Media_IsKaraok == '1')
            if type == '2':
                query = query.filter(M_Medias.Media_IsMovie == '1')
            if type == '3':
                query = query.filter(M_Medias.Media_IsAds == '1')
            if text!='' or text is not None:
                query = query.filter(or_(M_MediaDetails.Media_ID == text, \
                                     M_MediaDetails.Media_SerialNo == text, \
                                     M_MediaDetails.Media_Name.like(text+"%"), \
                                     M_MediaDetails.Actor_Name1 == text, \
                                     M_MediaDetails.Actor_Name2 == text, \
                                     M_MediaDetails.Actor_Name3 == text, \
                                     M_MediaDetails.Actor_Name4 == text, \
                                     M_MediaDetails.MediaType_Name1 == text, \
                                     M_MediaDetails.MediaType_Name2 == text, \
                                     M_MediaDetails.MediaType_Name3 == text, \
                                     M_MediaDetails.Language_Name == text, \
                                     M_Medias.Media_SoundSequence == text, \
                                     M_Medias.Media_HeaderSoundSequence == text )).order_by(M_MediaDetails.Media_SerialNo.desc())
            ret=query.offset(start).limit(psize)
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def get_by_count(self,text,type):
        try:
            ver = None
            query = self.slave.query(M_MediaDetails).join(M_Medias,M_MediaDetails.Media_ID == M_Medias.Media_ID)
            if type == None or type == '1' or type == '':
                query = query.filter(M_Medias.Media_IsKaraok == '1')
            if type == '2':
                query = query.filter(M_Medias.Media_IsMovie == '1')
            if type == '3':
                query = query.filter(M_Medias.Media_IsAds == '1')
            query = query.filter(or_(M_MediaDetails.Media_ID == text, \
                                 M_MediaDetails.Media_SerialNo == text, \
                                 M_MediaDetails.Media_Name.like(text+"%"), \
                                 M_MediaDetails.Actor_Name1 == text, \
                                 M_MediaDetails.Actor_Name2 == text, \
                                 M_MediaDetails.Actor_Name3 == text, \
                                 M_MediaDetails.Actor_Name4 == text, \
                                 M_MediaDetails.MediaType_Name1 == text, \
                                 M_MediaDetails.MediaType_Name2 == text, \
                                 M_MediaDetails.MediaType_Name3 == text, \
                                 M_MediaDetails.Language_Name == text))
            count = query.count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

class MediaType(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        try:
            ret=self.slave.query(M_MediaType).all()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def update(self, sid, new_json):
        try:
            param = {}

            if 'MediaType_ID' in new_json.keys():
                param['MediaType_ID'] = new_json['MediaType_ID']

            if 'MediaType_Name' in new_json.keys():
                param['MediaType_Name'] = new_json['MediaType_Name']

            if 'MediaType_Description' in new_json.keys():
                param['MediaType_Description'] = new_json['MediaType_Description']

            if 'MediaType_IsMovie' in new_json.keys():
                param['MediaType_IsMovie'] = new_json['MediaType_IsMovie']

            if 'MediaType_IsKaraok' in new_json.keys():
                param['MediaType_IsKaraok'] = new_json['MediaType_IsKaraok']

            if 'MediaType_IsAds' in new_json.keys():
                param['MediaType_IsAds'] = new_json['MediaType_IsAds']

            if 'MediaType_NewTypeID' in new_json.keys():
                param['MediaType_NewTypeID'] = new_json['MediaType_NewTypeID']

            ret = self.master.query(M_MediaType)\
                    .filter(M_MediaType.MediaType_ID == sid)\
                    .update(param)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            self.master.close()
            return False
        finally:
            self.master.close()

class ActorType(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        try:
            ret=self.slave.query(M_ActorType).all()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_name(self):
        try:
            ret = self.slave.query(M_ActorType).filter(M_ActorType.actortype_name == tname).first()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()


    def add_actortype(self, tinfo):
        try:
            at = M_ActorType()
            at.actortype_name = tinfo['actortype_name']
            if 'actortype_desc' in tinfo.keys():
                at.actortype_desc = tinfo['actortype_desc']
            else:
                at.actortype_desc = tinfo['actortype_name']
            if 'actortype_ismovie' in tinfo.keys():
                at.actortype_ismovie = tinfo['actortype_ismovie']
            else:
                at.actortype_ismovie = 0
            if 'actortype_iskaraok' in tinfo.keys():
                at.actortype_iskaraok = tinfo['actortype_iskaraok']
            else:
                at.actortype_iskaraok = 1
            self.master.add(at)
            ret = at.actortype_id
            self.master.commit()
            return ret
        except Exception as ex:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.master.close()


class Actors(TVAPPBase):
    @models_to_list
    def get_by_all(self, page, psize, text):
        start = (page - 1) * psize
        try:
            query = self.slave.query(M_Actors)\
                    .filter(or_(M_Actors.actor_no == text, \
                    M_Actors.actor_name.like(text+"%"), \
                    M_Actors.actor_type == text ))\
                    .order_by(M_Actors.actor_click.desc())

            ret=None
            if(psize == 0):
                ret=query.all()
            else:
                ret=query.offset(start).limit(psize)
            print("^^^^^^^^^^^type of ret is %s" % type(ret))
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def get_by_count(self,text):
        try:
            ver = None

            query = self.slave.query(M_Actors)
            query = query.filter(or_(M_Actors.actor_no == text, \
                                 M_Actors.actor_name.like(text+"%"), \
                                 M_Actors.actor_type == text ))

            count = query.count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def merge_actor(self, obj):
        actortype_id = 0
        ret = self.slave.query(M_ActorType.actortype_id).filter(M_ActorType.actortype_name == obj['actor_type']).first()
        if ret and len(ret) > 0:
            actortype_id = ret[0]
        else:
            at = M_ActorType()
            at.actortype_name = obj['actor_type']
            at.actortype_desc = tinfo['actortype_desc']
            at.actortype_ismovie = 0
            at.actortype_iskaraok = 1
            self.master.add(at)
            actortype_id = at.actortype_id

        act = M_Actors()
        if 'actor_no' not in obj.keys():
            act.actor_no = self.new_actor_no()
        else:
            act.actor_no = obj['actor_no']

        act.actor_name = obj['actor_name']
        if 'actor_des' in obj.keys():
            act.actor_des = obj['actor_des']
        else:
            act.actor_des = obj['actor_name']
        act.actor_py = obj['actor_py']
        act.actor_jp = obj['actor_jp']
        act.actor_type = obj['actor_type']
        act.actor_typeid = actortype_id
        if not act.actor_no:
            logger.error('got invalid actor_no: %s' % act.actor_no)
            return False

        try:
            self.master.merge(act)
            self.master.commit()
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()
            self.slave.close()
            pass
        return True

    def new_actor_no(self):
        '''
        有效的自定义编号为900000 - 909999
        '''
        max_no = self.slave.query(func.max(M_Actors.actor_no)).filter(M_Actors.actor_no >= 900000,M_Actors.actor_no <= 909999).all()
        if max_no:
            max_no = max_no[0][0]
            print('*' * 70)
            print(max_no)
            print('*' * 70)
            if max_no > 909999:
                return 909999
            elif max_no < 900000:
                return 900000
            elif max_no > 900000:
                return max_no + 1
            else:
                return None
        else:
            return 900000

    def update_actor(self, obj):
        actor_no = obj.pop('actor_no')
        for key in obj.keys():
            if key not in ['actor_no', 'actor_name', 'actor_type', 'actor_jp', 'actor_py', 'actor_desc']:
                obj.pop(key)
        try:
            ret = self.master.query(M_Actors)\
                    .filter(M_Actors.actor_no == actor_no)\
                    .update(obj)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()
            pass
        return True

    @models_to_list
    def get_by_name(self, actname):
        ret = self.slave.query(M_Actors).filter(M_Actors.actor_name == actname).all()
        return ret

class Medias(TVAPPBase):
    @models_to_list
    def get_by_all(self, page,psize):
        start = (page - 1) * psize
        try:
            ret=self.slave.query(M_Medias)\
                    .order_by(M_Medias.medias_click.desc())\
                    .offset(start).limit(psize)
            return ret
        except:
            return None
        finally:
            self.slave.close()

    def get_by_count(self, text=''):
        try:
            count = self.slave.query(M_Medias).count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def get_no_name_list(self):
        try:
            ret=self.slave.query(M_Medias.media_no, M_Medias.media_name).all()
            if ret:
                return self.models_to_list(ret)
            else:
                return None
        except:
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_no(self, media_no):
        try:
            ret = self.slave.query(M_Medias).filter(M_Medias.media_no == media_no).all()
            return ret
        except:
            return None
        finally:
            self.slave.close()

    def del_by_no(self, media_no):
        try:
            self.slave.query(M_Medias).filter(M_Medias.media_no == media_no).delete()
        except:
            logger.error(traceback.format_exc())
            return
        finally:
            self.slave.close()

    def set_newsong(self, nos):
        try:
            upd = {}
            upd['media_isnew'] = 1
            total = self.master.query(M_Medias).filter(M_Medias.media_no.in_(nos)).update(upd, synchronize_session=False)
            self.master.commit()
            return total
        except:
            self.master.rollback()
            logger.error(traceback.format_exc())
            return 0
        finally:
            self.master.close()

    def get_by_lang_count(self, lang):
        '''
        按语言查询歌曲数量信息.传入参数为语言名称(string)
        '''
        try:
            count = self.slave.query(M_Medias).filter(M_Medias.media_lang == lang)\
                    .count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_lang(self, lang, page, psize):
        '''
        按语言查询歌曲信息.传入参数为语言名称(string)
        '''
        start = (page - 1) * psize
        try:
            ret = self.slave.query(M_Medias).filter(M_Medias.media_lang == lang)\
                    .order_by(M_Medias.media_click.desc())\
                    .offset(start).limit(psize)
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def get_by_tag_count(self, tag):
        '''
        按语言查询歌曲数量信息.传入参数为语言名称(string)
        '''
        try:
            count = self.slave.query(M_Medias).filter(or_(M_Medias.media_tag1 == tag, M_Medias.media_tag2 == tag))\
                    .count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_tag(self, tag, page, psize):
        '''
        按语言查询歌曲信息.传入参数为语言名称(string)
        '''
        start = (page - 1) * psize
        try:
            ret=self.slave.query(M_Medias).filter(or_(M_Medias.media_tag1 == tag, M_Medias.media_tag2 == tag))\
                    .order_by(M_Medias.media_click.desc())\
                    .offset(start).limit(psize)
            return ret
        except:
            return None
        finally:
            self.slave.close()

    def merge_media(self, media):
        try:
            s = M_Medias()
            s.media_no = media['media_no']
            s.media_name = media['media_name']
            s.media_namelen = media['media_namelen']
            s.media_langtype = media['media_langtype']
            s.media_lang = media['media_lang']
            s.media_langid = media['media_langid']
            s.media_tag1 = media['media_tag1']
            s.media_tag2 = media['media_tag2']
            s.media_carria = media['media_carria']
            s.media_yuan = media['media_yuan']
            s.media_ban = media['media_ban']
            s.media_file = media['media_file']
            s.media_style = media['media_style']
            s.media_audio = media['media_audio']
            s.media_volume = media['media_volume']
            s.media_jp = media['media_jp']
            s.media_py = media['media_py']
            s.media_strok = media['media_strok']
            s.media_stroks = media['media_stroks']
            s.media_isnew = media['media_isnew']
            s.media_type = media['media_type']

            if 'media_svrgroup' in media.keys():
                s.media_svrgroup = media['media_svrgroup']

            if 'media_lyric' in media.keys():
                s.media_lyric = media['media_lyric']
            if 'media_click' in media.keys():
                s.media_click = media['']
            if 'media_clickm' in media.keys():
                s.media_clickm = media['']
            if 'media_clickw' in media.keys():
                s.media_clickw = media['']

            if 'media_stars' not in media.keys():
                s.media_stars = 1
            else:
                s.media_stars = media['media_stars']


            if 'media_actno1' in media.keys():
                s.media_actno1 = media['media_actno1']
                s.media_actname1 = media['media_actname1']
            else:
                s.media_actno1 = 0
                s.media_actname1 = ''

            if 'media_actno2' in media.keys():
                s.media_actno2 = media['media_actno2']
                s.media_actname2 = media['media_actname2']
            else:
                s.media_actno2 = 0
                s.media_actname2 = ''

            if 'media_actno3' in media.keys():
                s.media_actno3 = media['media_actno3']
                s.media_actname3 = media['media_actname3']
            else:
                s.media_actno3 = 0
                s.media_actname3 = ''

            if 'media_actno4' in media.keys():
                s.media_actno4 = media['media_actno4']
                s.media_actname4 = media['media_actname4']
            else:
                s.media_actno4 = 0
                s.media_actname4 = ''

            if 'media_dafen' in media.keys():
                s.media_dafen = media['media_dafen']

            if 'media_climaxinfo' in media.keys():
                s.media_climax = 1
                s.media_climaxinfo = media['media_climaxinfo']
            else:
                s.media_climax = 0
                s.media_climaxinfo = ''
            if 'media_yinyi' in media.keys():
                s.media_yinyi = media['media_yinyi']

            self.master.merge(s)
            self.master.commit()
            self.master.close()
            return True
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def get_file_byno(self, mno):
        try:
            ret = self.slave.query(M_Medias.Media_SerialNo, M_Medias.Media_Name, M_MediaFile.MediaFile_ServerID,\
                    M_MediaFile.MediaFile_Name)\
                    .join(M_MediaFile, M_MediaFile.MediaFile_MediaManage_ID == M_Medias.Media_Manage_ID)\
                    .filter( M_Medias.Media_SerialNo == mno).all()
            ret = self.models_to_list(ret)
            return ret
        except:
            return None
        finally:
            self.slave.close()

    def update(self, info):
        if 'media_no' not in info.keys():
            return False
        media_no = info.pop('media_no')
        try:
            ret = self.master.query(M_Medias)\
                    .filter(M_Medias.media_no == media_no)\
                    .update(info)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()
        return True

    def upload_media(self, media_no, media_file, media_name):
        new = M_Medias()
        new.media_name = media_name
        new.media_namelen = 0
        new.media_svrgroup = 1
        new.media_type = 0
        new.media_stars = 0
        new.media_dafen = 0
        new.media_climax = 0
        new.media_climaxinfo = '0'
        new.media_yinyi = 0
        new.media_light = 0
        new.media_langtype = 0
        new.media_no = media_no
        new.media_file = media_file
        self.master.add(new)
        self.master.commit()
        self.master.close()
        return

    def export_medias(self, fpath, only_added=False):
        try:
            where = ''
            if only_added:
                where = ' where medias.media_no >= 9000000 '
            res = self.slave.execute("select if(media_type=1, '歌曲', '广告') as mtype,media_name, media_lang,"\
                    "concat(media_tag1, if(media_tag2='', '', concat(',',media_tag2))), "\
                    "concat(concat(act1.actor_name,',',act1.actor_type,',',act1.actor_jp,',',act1.actor_py), "\
                    "if(media_actno2, concat(',',act2.actor_name,',',act2.actor_type,',',act2.actor_jp,',',act2.actor_py), ''), "\
                    "if(media_actno3, concat(',',act3.actor_name,',',act3.actor_type,',',act3.actor_jp,',',act3.actor_py), ''), "\
                    "if(media_actno4, concat(',',act4.actor_name,',',act4.actor_type,',',act4.actor_jp,',',act4.actor_py), '')) as media_actors, "\
                    "media_carria, media_yuan, media_ban, concat(media_no, '.ts') as media_file, "\
                    "ifnull(media_style, ''), media_volume, media_audio, media_jp, ifnull(media_langtype, 0), media_strok, "\
                    "media_stroks, media_isnew, 0, 0, media_py, 0, "\
                    "concat(if(ifnull(media_actno1,0)=0, '', concat(media_actno1)), if(ifnull(media_actno2,0)=0, '', concat(',',media_actno2)), "\
                    "if(ifnull(media_actno3,0)=0,'', concat(',',media_actno3)), if(ifnull(media_actno4,0)=0, '', concat(',',media_actno4))) as actnos "\
                    "from medias left join actors act1 on act1.actor_no = medias.media_actno1 "\
                    "left join actors act2 on act2.actor_no = medias.media_actno2 "\
                    "left join actors act3 on act3.actor_no = medias.media_actno3 "\
                    "left join actors act4 on act4.actor_no = medias.media_actno4 "\
                    " %s into outfile '%s' fields terminated by '|' " % (where, fpath))
        except Exception as ex:
            logger.error(traceback.format_exc())
            return False
        finally:
            self.slave.close()
        return True


class MediaManage(TVAPPBase):
    @models_to_list
    def get_by_all(self, page,psize):
        start = (page - 1) * psize
        try:
            ret=self.slave.query(M_MediaManage).offset(start).limit(psize)
            return ret
        except:
            return None
        finally:
            self.slave.close()

    def get_by_count(self):
        try:
            ver = None
            count = self.slave.query(M_MediaManage).count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add(self):
        try:
            s = M_MediaManage()

            s.MediaManage_Nation_ID = null
            s.MediaManage_Language_ID = null
            s.MediaManage_Carrier_ID = null
            s.MediaManage_Format_ID = null
            s.MediaManage_Audio_ID = null
            s.MediaManage_OrderCount = null
            s.MediaManage_IsNew = null
            s.MediaManage_IsValid = null
            s.MediaManage_OriginalTrack = null
            s.MediaManage_AccompanyTrack = null


            self.master.add(s)
            self.master.commit()
            return s.MediaManage_ID
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class MediaFile(TVAPPBase):

    @models_to_list
    def get_by_all(self, page, psize):
        start = (page - 1) * psize
        try:
            ret=self.slave.query(M_MediaFile).offset(start).limit(psize)
            return ret
        except:
            return None
        finally:
            self.slave.close()

    def get_by_count(self):
        try:
            ver = None
            count = self.slave.query(M_MediaFile).count()
            return count
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add(self, media_no, media_file):
        try:
            s = M_MediaFile()
            s.media_no = media_no
            s.media_file = media_file
            s.media_svrgroup = 1
            self.master.add(s)
            self.master.commit()
            self.master.close()
            return
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class Langs(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        try:
            ret=self.slave.query(M_Langs).all()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def get_id_by_name(self, name):
        try:
            ret = self.slave.query(M_Langs.lang_id).filter(M_Langs.lang_name == name).first()
            return ret[0]
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add_new(self, name):
        try:
            new = M_Langs()
            new.lang_name = name
            new.lang_des = name
            self.master.add(new)
            self.master.commit()
            sid = new.lang_id
            return sid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()


class Audios(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        try:
            ret=self.slave.query(M_Audios).all()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

class Carriers(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        try:
            ret=self.slave.query(M_Carriers).all()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

class AddMedia(TVAPPBase):
    @models_to_list
    def get_by_all(self):

        try:
            ret=self.slave.query(M_AddMedia)\
                .filter(M_AddMedia.AddMedia_State == 0)\
                .all()
            return ret
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def get_by_pathAndName(self, path, name):
        try:
            res = None
            if path and name:
                res = self.slave.query(M_AddMedia)\
                        .filter(and_(M_AddMedia.AddMedia_Path==path,M_AddMedia.AddMedia_Name==name))\
                        .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add(self, ver_json):
        try:
            new = M_AddMedia()
            new.AddMedia_Name = ver_json['AddMedia_Name']
            new.AddMedia_Path = ver_json['AddMedia_Path']
            new.AddMedia_Type = ver_json['AddMedia_Type']
            new.AddMedia_Size = ver_json['AddMedia_Size']
            new.AddMedia_SerialNo = ver_json['AddMedia_SerialNo']
            new.AddMedia_CreateDate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            new.AddMedia_UpdateDate = ''
            new.AddMedia_State = 0
            print '*'*20
            print new.AddMedia_SerialNo
            self.master.add(new)
            self.master.commit()
            self.master.close()
            sid = new.AddMedia_ID
            if sid > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def active(self, sid):
        try:
            param = {}

            param["AddMedia_State"] = 0

            ret = self.master.query(M_AddMedia)\
                    .filter(M_AddMedia.AddMedia_ID == sid)\
                    .update(param)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def delete(self, sid, sno):
        try:
            param = {}
            if sid == 0:
                param['AddMedia_SerialNo'] = sno
            if sno == 0:
                param['AddMedia_ID'] = sid
            param['AddMedia_State'] = 1
            param['AddMedia_UpdateDate'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            ret = self.master.query(M_AddMedia)\
                    .filter(or_(M_AddMedia.AddMedia_ID == sid,M_AddMedia.AddMedia_SerialNo == sno))\
                    .update(param)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()


class AutoPlay(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        ret=self.slave.query(M_AutoPlay).all()
        self.slave.close()
        return ret
    @models_to_list
    def get_by_no(self, media_no):
        ret = self.slave.query(M_AutoPlay).filter(M_AutoPlay.media_no == media_no).all()
        self.slave.close()
        return ret

    def add(self,data):
        new = M_AutoPlay()
        new.media_no = data['media_no']
        new.media_svrgrp = 1
        new.media_file = data['media_file']
        self.master.add(new)
        self.master.commit()
        self.master.close()
        return
    def exchange(self, data1, data2):
        tmp = copy.deepcopy(data2)
        tmp['media_no'] = 0
        try:
            self.master.query(M_AutoPlay)\
                .filter(M_AutoPlay.media_no == data1['media_no'])\
                .update(tmp)
            self.master.commit()
            self.master.query(M_AutoPlay)\
                .filter(M_AutoPlay.media_no == data2['media_no'])\
                .update(data1)
            self.master.commit()
            self.master.query(M_AutoPlay)\
                .filter(M_AutoPlay.media_no == 0)\
                .update(data2)
            self.master.commit()
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()
        return

    def del_by_no(self, media_no):
        self.master.query(M_AutoPlay).filter(M_AutoPlay.media_no == media_no).delete()
        self.master.commit()
        self.master.close()
        return
class MediaUserSet(TVAPPBase):
    @models_to_list
    def get_by_all(self):
        ret=self.slave.query(M_MediaDetails).join(M_MediaUserSet,M_MediaUserSet.MediaUserSet_MediaId==M_MediaDetails.Media_ID)\
        .order_by(M_MediaUserSet.MediaUserSet_Shunxu.asc()).all()
        self.slave.close()
        return ret

    def get_maxId(self):
        try:
            resultProxy=self.slave.execute(text('select max(MediaUserSet_Id) from mediauserset'))
            sid = resultProxy.fetchall()
            max=sid[0][0]
            if max == None:
                max=0
            return max
        except:
            logger.error(traceback.format_exc())
            return 0
        finally:
            self.slave.close()

    def add(self, ver_json):
        try:
            new = M_MediaUserSet()
            new.MediaUserSet_Id = ver_json['MediaUserSet_Id']
            new.MediaUserSet_MediaId = ver_json['MediaUserSet_MediaId']
            new.MediaUserSet_Shunxu = ver_json['MediaUserSet_Shunxu']
            count = self.slave.query(M_MediaUserSet).filter(M_MediaUserSet.MediaUserSet_MediaId==new.MediaUserSet_MediaId).count()
            print '-'*10
            print count
            sid = new.MediaUserSet_Id
            if count < 1:
                self.master.add(new)
                self.master.commit()
            return sid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return 0
        finally:
            self.master.close()

    def exchange(self,id1,id2):
        try:
            new = M_MediaUserSet()
            resultProxy=self.master.execute(text('select MediaUserSet_Id from mediauserset where MediaUserSet_MediaId='+str(id1)))
            sid = resultProxy.fetchall()
            MediaUserSet_Id1=sid[0][0]

            resultProxy=self.master.execute(text('select MediaUserSet_Id from mediauserset where MediaUserSet_MediaId='+str(id2)))
            sid = resultProxy.fetchall()
            MediaUserSet_Id2=sid[0][0]

            sql='update mediauserset set MediaUserSet_MediaId=\''+str(id2)+'\' where MediaUserSet_Id='+str(MediaUserSet_Id1)
            resultProxy=self.master.execute(text(sql))
            self.master.commit()

            sql='update mediauserset set MediaUserSet_MediaId=\''+str(id1)+'\' where MediaUserSet_Id='+str(MediaUserSet_Id2)
            resultProxy=self.master.execute(text(sql))

            self.master.commit()
            return resultProxy.rowcount
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return 0
        finally:
            self.master.close()

    def delete(self, sid):
        try:
            ret = self.master.query(M_MediaUserSet).filter(M_MediaUserSet.MediaUserSet_MediaId == sid).delete()
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class FileServers(TVAPPBase):
    @models_to_list
    def get_by_all(self,isMain):
        ret=self.slave.query(M_FileServers).filter(M_FileServers.FileServer_IsMainGroup == isMain).all()
        self.slave.close()
        return ret

class BoxSetting(TVAPPBase):
    @models_to_list
    def get_by_id(self, sid):
        try:
            res = None
            if sid:
                res = self.slave.query(M_BoxSetting)\
                        .filter(M_BoxSetting.optionid == sid)\
                        .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_BoxSetting) \
                    .filter(M_BoxSetting.result==1)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add(self, new_json):
        try:
            new = M_BoxSetting()
            new.ktvid = new_json['ktvid']
            new.name = new_json['name']
            new.appvalue = new_json['appvalue']
            new.boxtype = new_json['boxtype']
            new.result = new_json['result']
            new.typename = new_json['typename']
            new.optionid = new_json['optionid']
            new.optionname = new_json['optionname']
            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = new.ktvid

            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

    def update(self, sid, new_json):
        try:
            param = {}

            if 'ktvid' in new_json.keys():
                param['ktvid'] = new_json['ktvid']

            if 'name' in new_json.keys():
                param['name'] = new_json['name']

            if 'appvalue' in new_json.keys():
                param['appvalue'] = new_json['appvalue']

            if 'boxtype' in new_json.keys():
                param['boxtype'] = new_json['boxtype']

            if 'result' in new_json.keys():
                param['result'] = new_json['result']

            if 'typename' in new_json.keys():
                param['typename'] = new_json['typename']

            if 'optionid' in new_json.keys():
                param['optionid'] = new_json['optionid']

            if 'optionname' in new_json.keys():
                param['optionname'] = new_json['optionname']


            ret = self.master.query(M_BoxSetting)\
                    .filter(M_BoxSetting.optionid == sid)\
                    .update(param)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def delete(self, sid):
        try:
            ret = self.master.query(M_BoxSetting)\
                    .filter(M_BoxSetting.optionid== sid)\
                    .update({'result': 0})
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class Boxsetting(TVAPPBase):
    @models_to_list
    def get_by_id(self, appvalue):
        try:
            res = None
            if sid:
                res = self.slave.query(M_Boxsetting)\
                        .filter(M_Boxsetting.AppValue == appvalue)\
                        .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_Boxsetting) \
                    .filter(M_Boxsetting.addflag==0)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add(self, new_json):
        try:
            new = M_Boxsetting()
            new.ShowName = new_json['ShowName']
            new.AppValue = new_json['AppValue']
            new.IsString = new_json['IsString']
            new.result = new_json['result']
            new.optionvalue = new_json['optionvalue']
            new.optionname = new_json['optionname']
            new.addflag = new_json['addflag']
            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = 1

            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

    def update(self, appvalue, new_json):
        try:
            param = {}

            if 'ShowName' in new_json.keys():
                param['ShowName'] = new_json['ShowName']

            if 'AppValue' in new_json.keys():
                param['AppValue'] = new_json['AppValue']

            if 'IsString' in new_json.keys():
                param['IsString'] = new_json['IsString']

            if 'optionvalue' in new_json.keys():
                param['optionvalue'] = new_json['optionvalue']

            if 'optionname' in new_json.keys():
                param['optionname'] = new_json['optionname']

            if 'addflag' in new_json.keys():
                param['addflag'] = new_json['addflag']

            if 'result' in new_json.keys():
                param['result'] = new_json['result']

            if 'flag' in new_json.keys():
                param['flag'] = new_json['flag']

            ret = self.master.query(M_Boxsetting)\
                    .filter(M_Boxsetting.AppValue == appvalue)\
                    .update(param)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def updateflag(self, flag):
        try:
            param = {}
            param['optionvalue']=''
            param['result'] = 0
            param['flag'] = flag

            ret = self.master.query(M_Boxsetting)\
                    .filter(M_Boxsetting.flag == flag)\
                    .update(param)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def delete(self, appvalue):
        try:
            ret = self.master.query(M_BoxSetting)\
                    .filter(M_BoxSetting.AppValue== appvalue)\
                    .update({'result': 0})
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class Boxip(TVAPPBase):

    @models_to_list
    def get_all(self,flag):
        try:
            res = self.slave.query(M_Boxip) \
                    .filter(M_Boxip.flag == flag)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add(self, new_json):
        try:
            new = M_Boxip()
            new.ipaddress = new_json['ipaddress']
            new.subnetmask = new_json['subnetmask']
            new.serviceip = new_json['serviceip']
            new.devicetype = new_json['devicetype']
            new.devicegraphics = new_json['devicegraphics']
            new.iprecond = new_json['iprecond']
            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = 1
            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

    def update(self, flag, new_json):
        try:
            param = {}

            if 'ipaddress' in new_json.keys():
                param['ipaddress'] = new_json['ipaddress']

            if 'subnetmask' in new_json.keys():
                param['subnetmask'] = new_json['subnetmask']

            if 'serviceip' in new_json.keys():
                param['serviceip'] = new_json['serviceip']

            if 'devicetype' in new_json.keys():
                param['devicetype'] = new_json['devicetype']

            if 'devicegraphics' in new_json.keys():
                param['devicegraphics'] = new_json['devicegraphics']

            if 'iprecond' in new_json.keys():
                param['iprecond'] = new_json['iprecond']

            ret = self.master.query(M_Boxip)\
                    .filter(M_Boxip.flag == flag)\
                    .update(param)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def delete(self, flag):
        try:
            ret = self.master.query(M_Boxip)\
                    .filter(M_Boxip.flag== flag)\
                    .update({'flag': 0})
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class SystemSetting(TVAPPBase):

    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_SystemSettingInfo) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def update(self, settinginfo_name, new_json):
        try:
            param = {}

            if 'SettingInfo_Name' in new_json.keys():
                param['SettingInfo_Name'] = new_json['SettingInfo_Name']

            if 'SettingInfo_Value' in new_json.keys():
                param['SettingInfo_Value'] = new_json['SettingInfo_Value']

            ret = self.master.query(M_SystemSettingInfo)\
                    .filter(M_SystemSettingInfo.SettingInfo_Name == settinginfo_name)\
                    .update(param)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def delete(self, settinginfo_name):
        try:
            ret = self.master.query(M_SystemSettingInfo)\
                    .filter(M_SystemSettingInfo.SettingInfo_Name== settinginfo_name)\
                    .update({'flag': 0})
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class Configs(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_Configs).all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_name(self, cname):
        try:
            res = self.slave.query(M_Configs).filter(M_Configs.config_name==cname).all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_id(self, cid):
        try:
            res = self.slave.query(M_Configs).filter(M_Configs.config_id==cid).all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def update(self, cfgs):
        try:
            for key in cfgs.keys():
                ret = self.master.query(M_Configs).filter(M_Configs.config_name == key).update(dict(config_value=cfgs[key]))
                if ret <= 0:
                    self.master.rollback()
                    return False

            self.master.commit()
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()
        return True

class ConfiguresSetting(TVAPPBase):

    @models_to_list
    def get_all(self,id):
        try:
            res = self.slave.query(M_Configures) \
                    .filter(M_Configures.Configure_ID == id)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def update(self, id, new_json):
        try:
            param = {}

            if 'Configure_Set01' in new_json.keys():
                param['Configure_Set01'] = new_json['Configure_Set01']

            if 'Configure_Set02' in new_json.keys():
                param['Configure_Set02'] = new_json['Configure_Set02']
            if 'Configure_Set03' in new_json.keys():
                param['Configure_Set03'] = new_json['Configure_Set03']
            if 'Configure_Set04' in new_json.keys():
                param['Configure_Set04'] = new_json['Configure_Set04']
            if 'Configure_Set05' in new_json.keys():
                param['Configure_Set05'] = new_json['Configure_Set05']
            if 'Configure_Set06' in new_json.keys():
                param['Configure_Set06'] = new_json['Configure_Set06']
            if 'Configure_Set07' in new_json.keys():
                param['Configure_Set07'] = new_json['Configure_Set07']
            if 'Configure_Set08' in new_json.keys():
                param['Configure_Set08'] = new_json['Configure_Set08']
            if 'Configure_Set09' in new_json.keys():
                param['Configure_Set09'] = new_json['Configure_Set09']
            if 'Configure_Set10' in new_json.keys():
                param['Configure_Set10'] = new_json['Configure_Set10']



            if 'Configure_Set11' in new_json.keys():
                param['Configure_Set11'] = new_json['Configure_Set11']
            if 'Configure_Set12' in new_json.keys():
                param['Configure_Set12'] = new_json['Configure_Set12']
            if 'Configure_Set13' in new_json.keys():
                param['Configure_Set13'] = new_json['Configure_Set13']
            if 'Configure_Set14' in new_json.keys():
                param['Configure_Set14'] = new_json['Configure_Set14']
            if 'Configure_Set15' in new_json.keys():
                param['Configure_Set15'] = new_json['Configure_Set15']
            if 'Configure_Set16' in new_json.keys():
                param['Configure_Set16'] = new_json['Configure_Set16']
            if 'Configure_Set17' in new_json.keys():
                param['Configure_Set17'] = new_json['Configure_Set17']
            if 'Configure_Set18' in new_json.keys():
                param['Configure_Set18'] = new_json['Configure_Set18']
            if 'Configure_Set19' in new_json.keys():
                param['Configure_Set19'] = new_json['Configure_Set19']
            if 'Configure_Set20' in new_json.keys():
                param['Configure_Set20'] = new_json['Configure_Set20']



            if 'Configure_Set21' in new_json.keys():
                param['Configure_Set21'] = new_json['Configure_Set21']
            if 'Configure_Set22' in new_json.keys():
                param['Configure_Set22'] = new_json['Configure_Set22']
            if 'Configure_Set23' in new_json.keys():
                param['Configure_Set23'] = new_json['Configure_Set23']
            if 'Configure_Set24' in new_json.keys():
                param['Configure_Set24'] = new_json['Configure_Set24']
            if 'Configure_Set25' in new_json.keys():
                param['Configure_Set25'] = new_json['Configure_Set25']
            if 'Configure_Set26' in new_json.keys():
                param['Configure_Set26'] = new_json['Configure_Set26']
            if 'Configure_Set27' in new_json.keys():
                param['Configure_Set27'] = new_json['Configure_Set27']
            if 'Configure_Set28' in new_json.keys():
                param['Configure_Set28'] = new_json['Configure_Set28']
            if 'Configure_Set29' in new_json.keys():
                param['Configure_Set29'] = new_json['Configure_Set29']
            if 'Configure_Set30' in new_json.keys():
                param['Configure_Set30'] = new_json['Configure_Set30']


            if 'Configure_Set31' in new_json.keys():
                param['Configure_Set31'] = new_json['Configure_Set31']
            if 'Configure_Set32' in new_json.keys():
                param['Configure_Set32'] = new_json['Configure_Set32']
            if 'Configure_Set33' in new_json.keys():
                param['Configure_Set33'] = new_json['Configure_Set33']
            if 'Configure_Set34' in new_json.keys():
                param['Configure_Set34'] = new_json['Configure_Set34']
            if 'Configure_Set35' in new_json.keys():
                param['Configure_Set35'] = new_json['Configure_Set35']
            if 'Configure_Set36' in new_json.keys():
                param['Configure_Set36'] = new_json['Configure_Set36']
            if 'Configure_Set37' in new_json.keys():
                param['Configure_Set37'] = new_json['Configure_Set37']
            if 'Configure_Set38' in new_json.keys():
                param['Configure_Set38'] = new_json['Configure_Set38']
            if 'Configure_Set39' in new_json.keys():
                param['Configure_Set39'] = new_json['Configure_Set39']
            if 'Configure_Set40' in new_json.keys():
                param['Configure_Set40'] = new_json['Configure_Set40']


            if 'Configure_Set41' in new_json.keys():
                param['Configure_Set41'] = new_json['Configure_Set41']
            if 'Configure_Set42' in new_json.keys():
                param['Configure_Set42'] = new_json['Configure_Set42']
            if 'Configure_Set43' in new_json.keys():
                param['Configure_Set43'] = new_json['Configure_Set43']
            if 'Configure_Set44' in new_json.keys():
                param['Configure_Set44'] = new_json['Configure_Set44']
            if 'Configure_Set45' in new_json.keys():
                param['Configure_Set45'] = new_json['Configure_Set45']
            if 'Configure_Set46' in new_json.keys():
                param['Configure_Set46'] = new_json['Configure_Set46']
            if 'Configure_Set47' in new_json.keys():
                param['Configure_Set47'] = new_json['Configure_Set47']
            if 'Configure_Set48' in new_json.keys():
                param['Configure_Set48'] = new_json['Configure_Set48']
            if 'Configure_Set49' in new_json.keys():
                param['Configure_Set49'] = new_json['Configure_Set49']
            if 'Configure_Set50' in new_json.keys():
                param['Configure_Set50'] = new_json['Configure_Set50']


            if 'Configure_Set51' in new_json.keys():
                param['Configure_Set51'] = new_json['Configure_Set51']
            if 'Configure_Set52' in new_json.keys():
                param['Configure_Set52'] = new_json['Configure_Set52']
            if 'Configure_Set53' in new_json.keys():
                param['Configure_Set53'] = new_json['Configure_Set53']
            if 'Configure_Set54' in new_json.keys():
                param['Configure_Set54'] = new_json['Configure_Set54']
            if 'Configure_Set55' in new_json.keys():
                param['Configure_Set55'] = new_json['Configure_Set55']
            if 'Configure_Set56' in new_json.keys():
                param['Configure_Set56'] = new_json['Configure_Set56']
            if 'Configure_Set57' in new_json.keys():
                param['Configure_Set57'] = new_json['Configure_Set57']
            if 'Configure_Set58' in new_json.keys():
                param['Configure_Set58'] = new_json['Configure_Set58']
            if 'Configure_Set59' in new_json.keys():
                param['Configure_Set59'] = new_json['Configure_Set59']
            if 'Configure_Set60' in new_json.keys():
                param['Configure_Set60'] = new_json['Configure_Set60']


            if 'Configure_BookRemind' in new_json.keys():
                param['Configure_BookRemind'] = new_json['Configure_BookRemind']
            if 'Configure_CloseDelay' in new_json.keys():
                param['Configure_CloseDelay'] = new_json['Configure_CloseDelay']
            if 'Configure_MemberDiscActOn' in new_json.keys():
                param['Configure_MemberDiscActOn'] = new_json['Configure_MemberDiscActOn']
            if 'Configure_IsMark' in new_json.keys():
                param['Configure_IsMark'] = new_json['Configure_IsMark']


            if 'Configure_IsLeadSong' in new_json.keys():
                param['Configure_IsLeadSong'] = new_json['Configure_IsLeadSong']
            if 'Configure_IsSpecialEffect' in new_json.keys():
                param['Configure_IsSpecialEffect'] = new_json['Configure_IsSpecialEffect']
            if 'Configure_SongValidTime' in new_json.keys():
                param['Configure_SongValidTime'] = new_json['Configure_SongValidTime']
            if 'Configure_Version' in new_json.keys():
                param['Configure_Version'] = new_json['Configure_Version']
            if 'Configure_IsOnlyRead' in new_json.keys():
                param['Configure_IsOnlyRead'] = new_json['Configure_IsOnlyRead']


            if 'Configure_TimeChangeRange' in new_json.keys():
                param['Configure_TimeChangeRange'] = new_json['Configure_TimeChangeRange']
            if 'Configure_IsBoundRoom' in new_json.keys():
                param['Configure_IsBoundRoom'] = new_json['Configure_IsBoundRoom']
            if 'Configure_RoomDisplayContent' in new_json.keys():
                param['Configure_RoomDisplayContent'] = new_json['Configure_RoomDisplayContent']
            if 'Configure_MaxPayingTime' in new_json.keys():
                param['Configure_MaxPayingTime'] = new_json['Configure_MaxPayingTime']
            if 'Configure_TestRoom' in new_json.keys():
                param['Configure_TestRoom'] = new_json['Configure_TestRoom']


            if 'Configure_MaxTestTime' in new_json.keys():
                param['Configure_MaxTestTime'] = new_json['Configure_MaxTestTime']
            if 'Configure_PresentPrice' in new_json.keys():
                param['Configure_PresentPrice'] = new_json['Configure_PresentPrice']
            if 'Configure_OrderControl' in new_json.keys():
                param['Configure_OrderControl'] = new_json['Configure_OrderControl']
            if 'Configure_SentTime' in new_json.keys():
                param['Configure_SentTime'] = new_json['Configure_SentTime']
            if 'Configure_SentTimeBaseA' in new_json.keys():
                param['Configure_SentTimeBaseA'] = new_json['Configure_SentTimeBaseA']


            if 'Configure_SentTimeSendA' in new_json.keys():
                param['Configure_SentTimeSendA'] = new_json['Configure_SentTimeSendA']
            if 'Configure_SentTimeBaseB' in new_json.keys():
                param['Configure_SentTimeBaseB'] = new_json['Configure_SentTimeBaseB']
            if 'Configure_SentTimeSendB' in new_json.keys():
                param['Configure_SentTimeSendB'] = new_json['Configure_SentTimeSendB']
            if 'Configure_FingerBool' in new_json.keys():
                param['Configure_FingerBool'] = new_json['Configure_FingerBool']
            if 'Configure_FingerIPAddress' in new_json.keys():
                param['Configure_FingerIPAddress'] = new_json['Configure_FingerIPAddress']


            if 'Configure_AutoPresent' in new_json.keys():
                param['Configure_AutoPresent'] = new_json['Configure_AutoPresent']
            if 'Configure_PresentIsValidateWorker' in new_json.keys():
                param['Configure_PresentIsValidateWorker'] = new_json['Configure_PresentIsValidateWorker']
            if 'Configure_DishIsValidateWorker' in new_json.keys():
                param['Configure_DishIsValidateWorker'] = new_json['Configure_DishIsValidateWorker']
            if 'Configure_ReturnIsValidateWorker' in new_json.keys():
                param['Configure_ReturnIsValidateWorker'] = new_json['Configure_ReturnIsValidateWorker']

            ret = self.master.query(M_Configures)\
                    .filter(M_Configures.Configure_ID == id)\
                    .update(param)

            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def delete(self, id):
        try:
            ret = self.master.query(M_Configures)\
                    .filter(M_Configures.Configure_Set01== id)\
                    .update({'flag': 0})
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class Themes(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_Themes) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def delete(self, theme_id):
        try:
            ret = self.master.query(M_Themes)\
                    .filter(M_Themes.theme_id== theme_id)\
                    .update({'flag': 0})
            self.master.commit()
            self.master.close()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def add(self, info):
        th = M_Themes()
        th.theme_id = info['theme_id']
        th.theme_name = info['theme_name']
        th.theme_desc = info['theme_desc']
        th.theme_path = info['theme_path']
        th.theme_unpath = info['theme_unpath']
        th.theme_type = info['theme_type']
        th.theme_date = info['theme_date']
        th.theme_author = info['theme_author']
        th.theme_state = info['theme_state']
        th.theme_bagtype = info['theme_bagtype']

        try:
            self.master.add(th)
            self.master.commit()
            return True
        except Exception as ex:
            logger.error(traceback.format_exc())
            self.master.rollback()

        finally:
            self.master.close()
        return False

    def update(self, info):
        #TODO
        return False

class Skins(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_Skins).all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def delete(self, skin_id):
        try:
            ret = self.master.query(M_Skins)\
                    .filter(M_Skins.skin_id == skin_id)\
                    .delete()
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def add(self, new_json):
        try:
            skin_name = new_json['skin_name']
            res = self.master.query(M_Skins)\
                    .filter(M_Skins.skin_name == skin_name)\
                    .count()
            if res and res > 0:
                #already has this skin name, just return
                return True

            new = M_Skins()
            new.skin_name = new_json['skin_name']
            new.skin_desc = new_json['skin_desc']
            #new.skin_file = new_json['skin_file']
            #new.skin_unpath = new_json['skin_unpath']
            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = new.skin_id
            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

class Rooms(TVAPPBase):
    #@models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_Rooms.room_mac,M_Rooms.room_no,M_Rooms.room_name,M_Rooms.room_type,M_Rooms.room_ip,M_Rooms.room_mask,M_Rooms.room_gw,M_Rooms.room_dns,M_Rooms.room_stbtype,M_Rooms.room_svr,M_Rooms.room_recordsvr,M_Rooms.room_skin,M_Rooms.room_theme,M_Rooms.room_profile,M_Rooms.room_state,M_Themes.theme_name,M_Skins.skin_name)\
                    .join(M_Themes, M_Themes.theme_id == M_Rooms.room_theme, isouter=True)\
                    .join(M_Skins, M_Skins.skin_id == M_Rooms.room_skin, isouter=True)\
                    .all()
            '''
            res = self.slave.query(M_Rooms) \
                    .order_by(M_Rooms.room_ip) \
                    .all()
            '''
            return self.models_to_list(res)
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None

    def get_part_room(self,serialno):
        return self.get_by_no(serialno)

    def get_menpai_room(self, stbtype):
        return self.get_by_stbtype(stbtype)

    def get_part_room_ip(self, roomip):
        return self.get_by_ip(roomip)

    def room_exists(self, room_mac):
        try:
            res = self.slave.query(M_Rooms).filter(M_Rooms.room_mac == room_mac).count()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return 0

    @models_to_list
    def get_by_no(self,roomno):
        try:
            res = self.slave.query(M_Rooms) \
                    .filter(M_Rooms.room_no == roomno)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None

    @models_to_list
    def get_by_ip(self, roomip):
        try:
            res = self.slave.query(M_Rooms) \
                    .filter(M_Rooms.Room_IpAddress == roomip)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None

    @models_to_list
    def get_by_stbtype(self, stbtype):
        try:
            res = self.slave.query(M_Rooms) \
                    .filter(M_Rooms.room_stbtype == stbtype)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_rooms_id(self):
        try:
            res = self.slave.query(M_Rooms.Room_ID) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None

    @models_to_list
    def get_by_mac(self, mac):
        try:
            res = self.slave.query(M_Rooms) \
                    .filter(M_Rooms.room_mac == mac.lower())\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None


    def delete(self, mac):
        try:
            ret = self.master.query(M_Rooms)\
                    .filter(M_Rooms.room_mac == mac.lower())\
                    .delete()
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
        finally:
            self.master.close()
        return False

    def add(self, new_json):
        try:
            new = M_Rooms()
            new.room_mac = new_json['room_mac'].lower()
            new.room_no = new_json['room_no']
            new.room_name = new_json['room_name']
            if 'room_type' in new_json.keys():
                new.room_type = new_json['room_type']

            new.room_ip = new_json['room_ip']
            new.room_mask = new_json['room_mask']
            if 'room_gw' in new_json.keys():
                new.room_gw = new_json['room_gw']

            if 'room_dns' in new_json.keys():
                new.room_dns = new_json['room_dns']
            #new.room_stbtype = new_json['room_stbtype']
            new.room_svr = new_json['room_svr']
            new.room_recordsvr = new_json['room_svr']
            new.room_skin = new_json['room_skin']
            if 'room_theme' in new_json.keys():
                new.room_theme = new_json['room_theme']
            if 'room_profile' in new_json.keys():
                new.room_profile = new_json['room_profile']
            new.room_state = 0

            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            return True
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
        finally:
            self.master.close()
        return False

    def update(self, new_json):
        try:
            if 'room_mac' not in new_json.keys():
                return False
            room_mac = new_json['room_mac'].lower()
            for key in new_json.keys():
                if key not in ['room_no', 'room_name', 'room_ip',\
                        'room_mask', 'room_gw', 'room_dns', 'room_stbtype',\
                        'room_svr', 'room_skin', 'room_theme', 'room_profile',\
                        'room_state']:
                    new_json.pop(key)

            ret = self.master.query(M_Rooms)\
                    .filter(M_Rooms.room_mac == room_mac)\
                    .update(new_json)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
        finally:
            self.master.close()
        return False


class Servers(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_Servers).all()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None

    def count(self):
        try:
            res = self.slave.query(M_Servers).count()
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return 0

    def get_all_ip(self):
        try:
            res = self.slave.query(M_Servers.server_ip).all()
            res = self.models_to_list(res)
            return res
        except:
            logger.error(traceback.format_exc())
        finally:
            self.slave.close()
        return None

    @models_to_list
    def get_by_group(self, grpid):
        ret=self.slave.query(M_Servers).filter(M_Servers.server_grpid == grpid).all()
        self.slave.close()
        return ret

    @models_to_list
    def get_by_name(self, svrname):
        try:
            res = self.slave.query(M_Servers) \
                    .filter(M_Servers.server_name == svrname)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def delete(self, svrid):
        try:
            ret = self.master.query(M_Servers)\
                    .filter(M_Servers.server_id == svrid)\
                    .delete()
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
        finally:
            self.master.close()
        return False

    def add(self, svrinfo):
        try:
            nid = 0
            svr = M_Servers()
            svr.server_name = svrinfo['server_name']
            svr.server_ip = svrinfo['server_ip']
            svr.server_grpid = svrinfo['server_grpid']
            self.master.add(svr)
            self.master.commit()
            nid = svr.server_id
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return 0
        finally:
            self.master.close()
        return nid

    def update(self, svrinfo):
        try:
            if 'server_id' not in svrinfo.keys():
                return False
            server_id = svrinfo.pop('server_id')
            for key in svrinfo.keys():
                if key not in ['server_name', 'server_grpid', 'server_ip', 'server_weight']:
                    svrinfo.pop(key)

            ret = self.master.query(M_Servers)\
                    .filter(M_Servers.server_id == server_id)\
                    .update(svrinfo)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class FileServers(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_FileServers) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_by_all(self,isMain):
        ret=self.slave.query(M_FileServers).filter(M_FileServers.FileServer_IsMainGroup == isMain).all()
        self.slave.close()
        return ret

    @models_to_list
    def get_part_room(self,servername):
        try:
            res = self.slave.query(M_FileServers) \
                    .filter(M_FileServers.FileServer_Name== servername)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()


    def delete(self, servername):
        try:
            ret = self.master.query(M_FileServers)\
                    .filter(M_FileServers.FileServer_Name== servername)\
                    .delete()
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def add(self, new_json):
        try:
            new = M_FileServers()
            new.FileServer_Name = new_json['FileServer_Name']
            new.FileServer_IpAddress = new_json['FileServer_IpAddress']
            new.FileServer_OS = new_json['FileServer_OS']
            new.FileServer_IsValid = new_json['FileServer_IsValid']
            new.FileServer_Group_ID = new_json['FileServer_Group_ID']
            new.FileServer_IsMainGroup = new_json['FileServer_IsMainGroup']
            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = 1
            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

    def updata(self,servername, new_json):
        try:
            param = {}
            if 'FileServer_Name' in new_json.keys():
                param['FileServer_Name'] = new_json['FileServer_Name']

            if 'FileServer_IpAddress' in new_json.keys():
                param['FileServer_IpAddress'] = new_json['FileServer_IpAddress']
            if 'FileServer_OS' in new_json.keys():
                param['FileServer_OS'] = new_json['FileServer_OS']
            if 'FileServer_IsValid' in new_json.keys():
                param['FileServer_IsValid'] = new_json['FileServer_IsValid']
            if 'FileServer_Group_ID' in new_json.keys():
                param['FileServer_Group_ID'] = new_json['FileServer_Group_ID']
            if 'FileServer_IsMainGroup' in new_json.keys():
                param['FileServer_IsMainGroup'] = new_json['FileServer_IsMainGroup']

            ret = self.master.query(M_FileServers)\
                    .filter(M_FileServers.FileServer_Name == servername)\
                    .update(param)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()


class ServerGroups(TVAPPBase):

    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_ServersGroups) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_part_server(self,groupid):
        try:
            res = self.slave.query(M_ServersGroups) \
                    .filter(M_ServersGroups.ServerGroup_ID== groupid)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def delete(self, groupid):
        try:
            ret = self.master.query(M_ServersGroups)\
                    .filter(M_ServersGroups.ServerGroup_ID== groupid)\
                    .delete()
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def add(self, new_json):
        try:
            new = M_ServersGroups()
            new.ServerGroup_ID = new_json['ServerGroup_ID']
            new.ServerGroup_Name = new_json['ServerGroup_Name']
            new.ServerGroup_IsValid = new_json['ServerGroup_IsValid']

            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = new.ServerGroup_ID
            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

    def updata(self,groupid, new_json):
        try:
            param = {}
            if 'ServerGroup_ID' in new_json.keys():
                param['ServerGroup_ID'] = new_json['ServerGroup_ID']

            if 'ServerGroup_Name' in new_json.keys():
                param['ServerGroup_Name'] = new_json['ServerGroup_Name']
            if 'ServerGroup_IsValid' in new_json.keys():
                param['ServerGroup_IsValid'] = new_json['ServerGroup_IsValid']


            ret = self.master.query(M_ServersGroups)\
                    .filter(M_ServersGroups.ServerGroup_ID == groupid)\
                    .update(param)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()


class KaraokVersion(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_KaraokVersions) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

class CloudMusicInfo(TVAPPBase):
    #M_CloudMusicInfo
    def get_all_count(self):
        try:
            res = self.slave.query(M_CloudMusicInfo).count()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_all(self, offset=0, limit=10):
        try:
            res = self.slave.query(M_CloudMusicInfo).\
                    order_by(M_CloudMusicInfo.music_lastverdate.desc()).offset(offset).limit(limit)
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def del_music(self, mno):
        try:
            ret = self.master.query(M_CloudMusicInfo)\
                    .filter(M_CloudMusicInfo.music_no == mno).delete()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            return False
        finally:
            self.master.close()

    def search_all_count(self, key):
        try:
            if key:
                if key.isdigit():
                    res = self.slave.query(M_CloudMusicInfo).filter(or_(
                        M_CloudMusicInfo.music_no == int(key), \
                        M_CloudMusicInfo.music_name == key, \
                        M_CloudMusicInfo.music_singer == key, \
                        M_CloudMusicInfo.music_type1 == key, \
                        M_CloudMusicInfo.music_lang == key, \
                        )).count()
                else:
                    res = self.slave.query(M_CloudMusicInfo).filter(or_(
                        M_CloudMusicInfo.music_name == key, \
                        M_CloudMusicInfo.music_singer == key, \
                        M_CloudMusicInfo.music_type1 == key, \
                        M_CloudMusicInfo.music_lang == key, \
                        )).count()
            else:
                res = self.slave.query(M_CloudMusicInfo).count()
            return res
        except:
            logger.error(traceback.format_exc())
            return 0
        finally:
            self.slave.close()
        return 0

    @models_to_list
    def search_all(self, key, offset=0, limit=10):
        try:
            if key:
                if key.isdigit():
                    res = self.slave.query(M_CloudMusicInfo).filter(or_(
                        M_CloudMusicInfo.music_no == int(key), \
                        M_CloudMusicInfo.music_name == key, \
                        M_CloudMusicInfo.music_singer == key\
                        )).order_by(M_CloudMusicInfo.music_lastverdate.desc())\
                        .offset(offset).limit(limit)
                else:
                    res = self.slave.query(M_CloudMusicInfo).filter(or_(
                        M_CloudMusicInfo.music_name == key, \
                        M_CloudMusicInfo.music_singer == key, \
                        M_CloudMusicInfo.music_type1 == key, \
                        M_CloudMusicInfo.music_lang == key\
                        )).order_by(M_CloudMusicInfo.music_lastverdate.desc())\
                        .offset(offset).limit(limit)
            else:
                res = self.slave.query(M_CloudMusicInfo)\
                        .order_by(M_CloudMusicInfo.music_lastverdate.desc())\
                        .offset(offset).limit(limit)
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

class CloudDownLog(TVAPPBase):
    def get_all_count(self):
        try:
            res = self.slave.query(M_CloudDownLog).count()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_all(self, offset=0, limit=10):
        try:
            res = self.slave.query(M_CloudDownLog).order_by(M_CloudDownLog.down_id.desc()).offset(offset).limit(limit)
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add_downlog(self, downinfo):
        dl = M_CloudDownLog()
        if 'down_gid' in downinfo.keys():
            dl.down_gid = downinfo['down_gid']
        if 'music_no' in downinfo.keys():
            dl.music_no = downinfo['music_no']
        if 'music_caption' in downinfo.keys():
            dl.music_caption = downinfo['music_caption']
        if 'music_singer' in downinfo.keys():
            dl.music_singer = downinfo['music_singer']
        if 'music_lang' in downinfo.keys():
            dl.music_lang = downinfo['music_lang']
        if 'music_theme' in downinfo.keys():
            dl.music_theme = downinfo['music_theme']
        if 'music_ver' in downinfo.keys():
            dl.music_ver = downinfo['music_ver']
        if 'music_verdate' in downinfo.keys():
            dl.music_verdate = downinfo['music_verdate']
        if 'down_path' in downinfo.keys():
            dl.down_path = downinfo['down_path']
        if 'down_url' in downinfo.keys():
            dl.down_url = downinfo['down_url']
        if 'down_stime' in downinfo.keys():
            dl.down_stime = downinfo['down_stime']
        if 'down_etime' in downinfo.keys():
            dl.down_etime = downinfo['down_etime']
        if 'down_status' in downinfo.keys():
            dl.down_status = downinfo['down_status']
        if 'music_addtime' in downinfo.keys():
            dl.music_addtime = downinfo['music_addtime']
        if 'music_hot' in downinfo.keys():
            dl.music_hot = downinfo['music_hot']
        if 'music_replace' in downinfo.keys():
            dl.music_replace = downinfo['music_replace']
        if 'music_type' in downinfo.keys():
            dl.music_type = downinfo['music_type']
        if 'down_type' in downinfo.keys():
            dl.down_type = downinfo['down_type']
        if 'file_md5' in downinfo.keys():
            dl.file_md5 = downinfo['file_md5']
        if 'file_type' in downinfo.keys():
            dl.file_type = downinfo['file_type']
        if 'file_size' in downinfo.keys():
            dl.file_size = downinfo['file_size']
        if 'movie_type' in downinfo.keys():
            dl.movie_type = downinfo['movie_type']

        try:
            self.master.add(dl)
            self.master.commit()
            did = dl.down_id
            self.master.close()
            if did > 0:
                return True
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def update_by_id(self, downid, param):
        try:
            ret = self.master.query(M_CloudDownLog)\
                    .filter(M_CloudDownLog.down_id == down_id)\
                    .update(param)
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def update_by_mno_gid(self, mno, gid, param):
        try:
            ret = self.master.query(M_CloudDownLog)\
                    .filter(M_CloudDownLog.down_gid == gid, M_CloudDownLog.music_no == mno)\
                    .update(param)
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

class KtvModules(TVAPPBase):
    @models_to_list
    def get_all(self, bagtype=0):
        try:
            if bagtype in (1, 2):
                res = self.slave.query(M_KtvModuleVer).filter(M_KtvModuleVer.bagtype == bagtype)\
                        .all()
            else:
                res = self.slave.query(M_KtvModuleVer).all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_latest(self, bagtype=0):
        try:
            if bagtype in (1, 2):
                res = self.slave.query(M_KtvModuleVer).filter(M_KtvModuleVer.bagtype == bagtype)\
                        .order_by(M_KtvModuleVer.id.desc())\
                        .offset(0).limit(1)
            else:
                res = self.slave.query(M_KtvModuleVer).order_by(M_KtvModuleVer.id.desc())\
                        .offset(0).limit(1)
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_byid(self, mid):
        try:
            res = self.slave.query(M_KtvModuleVer).filter(M_KtvModuleVer.id == mid)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def add_module(self, minfo):
        try:
            m = M_KtvModuleVer()
            m.id = minfo['id']
            m.name = minfo['name']
            m.addtime = minfo['addtime']
            m.fileurl = minfo['fileurl']
            m.unpath = minfo['unpath']
            m.version = minfo['version']
            m.isuse = minfo['isuse']
            m.needun = minfo['needun']
            m.desc = minfo['desc']
            m.msgtime = minfo['msgtime']
            m.isshow = minfo['isshow']
            m.bagtype = minfo['bagtype']
            m.isdefault = minfo['isdefault']
            m.revision = minfo['revision']
            m.vertype = minfo['vertype']

            self.master.add(m)
            ret = m.id
            self.master.commit()
            return ret
        except:
            self.master.rollback()
            logger.error(traceback.format_exc())
            return None
        finally:
            self.master.close()

    def del_module(self, mid):
        try:
            ret = self.master.query(M_KtvModuleVer).filter(M_KtvModuleVer.id == mid).delete()
            self.master.commit()
            if ret > 0:
                return True
        except:
            self.master.rollback()
            logger.error(traceback.format_exc())
        finally:
            self.master.close()
        return False

class MenPaiAdSetting(TVAPPBase):
    @models_to_list
    def get_all(self):
        try:
            res = self.slave.query(M_MenPaiAdSettings) \
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    @models_to_list
    def get_all_bytype(self,mentype):
        try:
            res = self.slave.query(M_MenPaiAdSettings) \
                    .filter(M_MenPaiAdSettings.MenPaiType_ID== mentype)\
                    .all()
            return res
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            self.slave.close()

    def delete(self, settingid):
        try:
            ret = self.master.query(M_MenPaiAdSettings)\
                    .filter(M_MenPaiAdSettings.MenPaiAdSetting_Id== settingid)\
                    .delete()
            self.master.commit()

            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def deleteall(self):
        try:
            ret = self.master.query(M_MenPaiAdSettings)\
                    .delete()
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

    def deletebyroom(self, roomid):
        try:
            ret = self.master.query(M_MenPaiAdSettings)\
                    .filter(M_MenPaiAdSettings.MenPaiAdSettings_RoomID== roomid)\
                    .delete()
            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()


    def add(self, new_json):
        try:
            new = M_MenPaiAdSettings()
            new.MenPaiAdSetting_SerialNo = new_json['MenPaiAdSetting_SerialNo']
            new.MenPaiAdSetting_PlayCount = new_json['MenPaiAdSetting_PlayCount']
            new.MenPaiType_ID = new_json['MenPaiType_ID']
            new.MenPaiAdSettings_RoomID = new_json['MenPaiAdSettings_RoomID']

            self.master.add(new)
            self.master.commit()
            #the object <new> will be not available after the session closed.
            nid = new.MenPaiAdSetting_SerialNo

            return nid
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return None
        finally:
            self.master.close()

    def updata(self,adid, new_json):
        try:
            param = {}
            if 'MenPaiAdSetting_SerialNo' in new_json.keys():
                param['MenPaiAdSetting_SerialNo'] = new_json['MenPaiAdSetting_SerialNo']

            if 'MenPaiAdSetting_PlayCount' in new_json.keys():
                param['MenPaiAdSetting_PlayCount'] = new_json['MenPaiAdSetting_PlayCount']
            if 'MenPaiType_ID' in new_json.keys():
                param['MenPaiType_ID'] = new_json['MenPaiType_ID']
            if 'MenPaiAdSettings_RoomID' in new_json.keys():
                param['MenPaiAdSettings_RoomID'] = new_json['MenPaiAdSettings_RoomID']


            ret = self.master.query(M_MenPaiAdSettings)\
                    .filter(M_MenPaiAdSettings.MenPaiAdSetting_Id == adid)\
                    .update(param)

            self.master.commit()
            if ret > 0:
                return True
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            self.master.rollback()
            return False
        finally:
            self.master.close()

