#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import logging 
import commands
import traceback

from lib import http
from orm import orm as _mysql

logger = logging.getLogger(__name__)
def get_all_medias(page, psize):
    ret = None
    res = _mysql.medias.get_by_all(page,psize)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = len(res)
    return ret

def get_media_count(text = ''):
    count=_mysql.medias.get_by_count(text)
    ret = {}
    ret['total'] = count
    return ret

def get_file_by_no(mno):
    '''
    按歌曲编号查询文件路径, 多服务器组时，还要查看在哪个服务器上。
    '''
    ret = _mysql.medias.get_file_byno(mno)
    print ret
    if isinstance(ret, list) and len(ret) > 0:
        return ret[0]['MediaFile_Name']
    return None


def get_by_lang_count(lang):
    return _mysql.medias.get_by_lang_count(lang)

def get_by_lang(lang, page, psize):
    '''
    按照语种名称查询
    '''
    matches = []
    total = _mysql.medias.get_by_lang_count(lang)
    if total > 0:
        matches = _mysql.medias.get_by_lang(lang, page, psize)
    return dict(total=total, matches=matches)

def get_by_tag(tag, page, psize):
    '''
    按照3D分类(tag)查询
    '''
    matches = []
    total = _mysql.medias.get_by_tag_count(tag)
    if total > 0:
        matches = _mysql.medias.get_by_tag(tag, page, psize)
    return dict(total=total, matches=matches)

def add_update_media(media_info):
    '''
        add new media info, or update the exists record
    '''
    if 'media_langid' not in media_info.keys():
        media_info['media_langid'] = _mysql.langs.get_id_by_name(media_info['media_lang'])
    logger.error("add_update_media: langid: %d, langname: %s" % (media_info['media_langid'], media_info['media_lang']))
    media_no = media_info['media_no']
    if media_get_yinyi(media_no):
        media_info['media_yinyi'] = 1
    else:
        media_info['media_yinyi'] = 0

    if media_get_dafen(media_no):
        media_info['media_dafen'] = 1
    else:
        media_info['media_dafen'] = 0
    
    return _mysql.medias.merge_media(media_info)


def update_media(media_info):
    '''
     '''
    return _mysql.medias.update(media_info)

def upload_media(media_no, media_file, media_name):
    return _mysql.medias.upload_media(media_no, media_file, media_name)

def export_medias(fpath, only_added = False):
    return _mysql.medias.export_medias(fpath, only_added)

def get_lost_files():
    otpList = {}
    output = commands.getoutput('ls -R /video/*')
    files = output.split('\n');
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                otpList[file[:file.find(".")]]=1
    dataMap = _mysql.medias.get_no_name_list()
    qs = []
    for media in dataMap:
        if not otpList.has_key(media['media_no']):
            g={}
            g['no'] = media['media_no']
            g['name'] = dataMap[media['media_no']]
            qs.append(g)
    res = {}
    res['total'] = len(qs)
    res['matches'] = qs
    return res

def get_useless_files():
    otpList = []
    output = commands.getoutput('ls -R /video/*')
    files = output.split('\n');
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                fl={}
                fl["no"]=file[:file.find(".")]
                fl["path"]='/' + path + '/' + file
                otpList.append(fl)

    dataMap = _mysql.medias.get_no_name_list()
    ry = []
    for fl in otpList:
        if(not dataMap.has_key(fl["no"])):
            ry.append(fl)
        else:
            del dataMap[fl["no"]]
    res = {}
    res['total'] = len(ry)
    res['matches'] = ry
    return res

def media_get_climax(media_no):
    '''
    climax info 
    '''
    return None

def media_get_yinyi(media_no):
    '''
    get yinyi info for music
    '''
    fpath = os.path.join('/data/TranslateLyricData', '%d.txt' % media_no)
    return os.path.exists(fpath)

def media_get_dafen(media_no):
    '''
    get dafen info for music
    '''
    fpath = os.path.join('/data/LyricData', '%d.txt' % media_no)
    return os.path.exists(fpath)

def medias_set_newsong(nos):
    '''
    按传入的歌曲编号列表，设置新歌标记
    '''
    return _mysql.medias.set_newsong(nos)

def medias_get_delete_list():
    '''
    按传入的歌曲编号列表，设置新歌标记
    '''
    mf_list = {}
    session = _mysql.get_session('karaok') 
    try: 
        cmd = "select addtime from mediahistory limit 1"
        ts = session.execute(cmd).fetchall() 
        if ts:
            first_time = ts[0][0]
        else:
            logger.error("medias history not found, cannot delete any medias")
            return mf_list
            first_time = None

        time_1 = time.mktime(first_time.timetuple())
        time_2 = int(time.time())

        if (time_2 - time_1) / (3600 * 24) < 29:
            logger.error("medias history not enough 30 days, cannot delete any medias(%s)" % first_time)
            return mf_list

        cmd = "select media_no, media_file from medias where media_file <> '' and media_no in "\
                "(select media_no from medias_allowdel where media_no not in "\
                "(select distinct(media_no) from mediahistory)) limit 200"
        ts = session.execute(cmd).fetchall() 
        for tb in ts: 
            mf_list[str(tb[0])] = tb[1]
    except Exception as ex:
        logger.error(traceback.format_exc())
    finally:
        session.close()
    return mf_list

def medias_create_deltable():
    cmd = "create table if not exists medias_deleted(select media_no, media_file, now() as media_deltime from medias limit 0)"
    session = _mysql.get_session('karaok') 
    try: 
        ts = session.execute(cmd).fetchall() 
        return True
    except Exception as ex:
        logger.error(traceback.format_exc())
    finally:
        session.close()
    return False
 
def medias_update_fpath(nos):
    '''
    按传入的歌曲编号列表，设置新歌标记
    '''
    mf_list = {}
    session = _mysql.get_session('karaok') 
    try: 
        cmd = "insert into medias_deleted (select media_no, media_file, now() as media_deltime from medias where media_no in (%s))" % ','.join(nos)
        ts = session.execute(cmd)
        cmd = "update medias set media_file='' where media_no in (%s)" % ','.join(nos)
        ts = session.execute(cmd)
        logger.info("update delete info: %s " % ts)
        session.commit()
        return True
    except Exception as ex:
        session.rollback()
        logger.error(traceback.format_exc())
    finally:
        session.close()
    return False

