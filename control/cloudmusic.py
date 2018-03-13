#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import logging
import traceback
import hashlib

from lib.common import gen_sign_for_kcloud, generator_query_string_and_signature
from lib.http import request_json
from lib.des import DESEncrypt
from lib.mc import _defaultredis as redis_cli
from orm.mm import cloud_music_get_list, cloud_music_get_count
from orm import orm as _mysql

logger = logging.getLogger(__name__)

ktv_90_API = 'http://v1.ktv.api.ktvdaren.com'
cloud_API_S = 'https://kcloud.v2.service.ktvdaren.com'
cloud_API = 'http://kcloud.v2.service.ktvdaren.com'
app_id = 'ebf0694982384de46e363e74f2c623ed'
sec_key = '9c1db7829f839f362052692c89556ce3'
app_ver = '4.0.0.75'
box_ver = '5.0.0.72'
 
#cloudmusic
des_cli = DESEncrypt()

def get_cloud_session_key():
    key = hashlib.md5("cloudmusic_client_session").hexdigest().upper()
    return key

def get_musicinfo_key(mno):
    return "cache_musicinfo_%s" % mno

def get_complete_task_key(mno):
    '''
    加歌成功后，留一段时间此歌曲的下载信息
    '''
    return "cache_complete_task_%s" % mno

def get_cloudfile_key(mno):
    return "cache_musicfile_%s" % mno

def get_downtask_gid_key():
    '''
    mno -> gid
    '''
    return "cache_doanload_tasks"

def get_dljobs_map_key():
    '''
    gid -> mno
    '''
    return "aria2_gid_mapto_sno"

def get_rt_download_key():
    '''
    '''
    return "aria2_realtime_mnos"

def aria2_gid2mno(gid):
    sno = redis_cli.hget(get_dljobs_map_key(), gid)
    return sno

def aria2_mno2gid(mno):
    gid = redis_cli.hget(get_downtask_gid_key(), mno)
    return gid

def get_aria2_complete_task(mno):
    key = get_complete_task_key(mno)
    try:
        tinfo = redis_cli.get(key)
        if tinfo:
            tinfo = json.loads(tinfo)
            return tinfo
        else:
            return None
    except Exception as ex:
        logger.error(traceback.format_exc())
    return None

def get_cloud_session():
    key = get_cloud_session_key()
    sec_data = redis_cli.get(key)
    if not sec_data:
        return None
    ret = sec_data
    ret = json.loads(ret)
    if isinstance(ret, dict):
        if 'validkey' in ret.keys():
            return ret
        else:
            return None
    else:
        return None

def set_cloud_session(sec):
    key = get_cloud_session_key()
    sec_data = json.dumps(sec)
    redis_cli.set(key, sec_data)
    redis_cli.expire(key, 60*5)
    return True
    
def add_music_byapi(self, minfo, fpath):
    pass

def get_musicinfo_byno(mno):
    if not mno:
        return None
    result = []
    nos = []
    key = get_musicinfo_key(mno)
    ret = redis_cli.get(key)
    if ret:
        ret = json.loads(ret)
    if isinstance(ret, dict):
        return ret
    #TODO: seek music nos in redis cache at first
    url = cloud_API + '/MusicService.aspx?op=getmusicinfobynos&depot=0&nos=%s' % mno
    print url
    try:
        res = request_json(url, method='GET')
        session = {}
        if res['code'] == 1:
            if not res['result']:
                #已经下线的歌曲，偶有还可以下载的情况，但是拿不到信息
                logger.error("Failed to get musicinfo (no:%s), possible song has deleted on cloud side" % mno)
                return None
            m = res['result']['matches'][0]
            key = get_musicinfo_key(m['Music_No'])
            redis_cli.set(key, json.dumps(m))
            redis_cli.expire(key, 3600*24*7)
            return m
    except Exception as ex:
        logger.error(traceback.format_exc())

    if not res['code'] == 1:
        print res['msg']
    return None

def get_musicinfo_bylist(mnos):
    result = []
    nos = []
    for mno in mnos:
        key = get_musicinfo_key(mno)
        ret = redis_cli.get(key)
        if ret:
            ret = json.loads(ret)
        if isinstance(ret, dict):
            result.append(ret)
        else:
            nos.append(mno)

    if not nos:
        return result

    #TODO: seek music nos in redis cache at first
    url = cloud_API + '/MusicService.aspx?op=getmusicinfobynos&depot=0&nos=%s' % ','.join(nos)
    print url
    try:
        res = request_json(url, method='GET')
        session = {}
        if res['code'] == 1:
            for m in res['result']['matches']:
                result.append(m)
                key = get_musicinfo_key(m['Music_No'])
                redis_cli.set(key, json.dumps(m))
                redis_cli.expire(key, 3600*24*7)
        return result
    except Exception as ex:
        logger.error(traceback.format_exc())

    if not res['code'] == 1:
        print res['msg']
    return None

def set_cloudfile_status(mno, status):
    '''
    update db to set download status
    '''
    sql = ''
    return True

def save_download_log(mno, minfo):
    '''
    insert download log to table cloud_downfile.
    '''
    return True

def complete_download_log(mno, gid):
    '''
    download log in table cloud_downfile, to set the complete time.
    '''
    return True

def get_cloudmusic_url(mno, dtype=0):
    #https://kcloud.v2.service.ktvdaren.com/MusicService.aspx?appid=ebf0694982384de46e363e74f2c623ed&appver=4.0.0.76&dogname=&filetype=0&musicno=7650021&op=getmusicdownurl&storeid=87832&type=2&userid=17779&username=cx90hcs&utime=1497493237&validkey=ebc9e4378f4dc098368f4492143c06ce&sign=681b1bf04e409d9287c72b68a408a89a&downtyp=0&boxver=5.0.0.72
    ses = get_cloud_session()

    int_t = int(time.time())

    params = {'appid': app_id,
            'appver': app_ver,
            'dogname': ses['dog'],
            'filetype': 0, #0或1：歌曲 2：资料 3:电影 4:任务
            'musicno': mno,
            'op': 'getmusicdownurl',
            'storeid': ses['storeid'],
            'userid': ses['uid'],
            'username': ses['uname'],
            'validkey': ses['validkey'],
            'type': 2,
            'utime': int_t}

    qerystr = gen_sign_for_kcloud(params, '', sec_key)
    url = cloud_API_S + '/MusicService.aspx?' + qerystr
            #'downtype': dtype,
    url += "&downtype=%d&boxver=%s&clientid=1" % (dtype, box_ver)
    print (url)

    res = request_json(url, method='GET')
    if res['code'] == 1:
        minfo = res['result']['matches'][0]
        redis_cli.set(get_cloudfile_key(mno), json.dumps(minfo))
        redis_cli.expire(get_cloudfile_key(mno), 3600*3)
        return minfo
    elif isinstance(res, dict) and res['code'] == -3:
        logger.error(u'cannot find this music info from cloud, maybe it has been deleted. musicno: %s' % mno)
        delete_music_info(mno)
        return None
    else:
        print "get download url: res: %s" % res
    return None

def get_download_limit():
    ses = get_cloud_session()
    url = ktv_90_API + '/cdn/downspeed?dogname=%s' % ses['dog']
    res = request_json(url, method='GET')
    if res['code'] == 1:
        return res['data']
    else:
        print "get download limit: %s" % res
    return None

def get_musictask_gid(mno):
    return aria2_mno2gid(mno)

def set_musictask_gid(mno, gid, realtime=0):
    redis_cli.hset(get_downtask_gid_key(), mno, gid)
    redis_cli.hset(get_dljobs_map_key(), gid, mno)
    if realtime == 1:
        redis_cli.sadd(get_rt_download_key(), mno)
    return True

def set_mno_realtime_download(mno):
    redis_cli.sadd(get_rt_download_key(), mno)

def del_musictask_gid(mno, gid):
    redis_cli.hdel(get_downtask_gid_key(), mno)
    redis_cli.hdel(get_dljobs_map_key(), gid)
    redis_cli.srem(get_rt_download_key(), mno)
    return True

def get_musicinfo_key(mno):
    key = 'music_info_%s' % mno
    return key

def cache_musicinfo(mno, minfo):
    return redis_cli.set(get_musicinfo_key(), mno, minfo)

def get_cloudmusic_list(offset=0, limit=10):
    '''
    查看云端可下载列表信息
    '''
    res = []
    total = cloud_music_get_count()
    if total > 0:
        res = cloud_music_get_list(offset, limit)
    return dict(total=total, matches=res)

def search_cloudmusic_list(key, offset=0, limit=10):
    '''
    查看云端可下载列表信息, 搜索接口
    '''
    ret = None
    total = _mysql.cloudmusicinfo.search_all_count(key)
    res = _mysql.cloudmusicinfo.search_all(key, offset, limit)
    if isinstance(res, list) and len(res) > 0:
        ret = {}
        ret['matches'] = res
        ret['total'] = total
    return ret

from orm import orm as _mysql

def get_music_downlog(offset=0, limit=10):
    res = []
    total = _mysql.downlog.get_all_count()
    if total > 0:
        res = _mysql.downlog.get_all(offset, limit)
    if isinstance(res, list):
        return dict(matches=res, total=total)
    return None


def update_downstatus(gid, mno, status):
    params = dict(down_status=status)
    return _mysql.downlog.update_by_gid_mno(gid, mno, params)

def add_music_downlog(downinfo):
    '''
    添加下载日志
    '''
    return _mysql.downlog.add_downlog(downinfo)

def update_downlog_by_mnogid(mno, gid, downinfo):
    return _mysql.downlog.update_by_mno_gid(mno, gid, downinfo)

def delete_music_info(mno):
    return _mysql.cloudmusicinfo.del_music(mno)
