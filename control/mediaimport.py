#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import codecs
import logging
import traceback
import commands

from orm import orm as _mysql
from control.actortype import actorTypes, actortype_name2id, add_new_actortype
from control.languages import lanaugages_name2id
from setting import TMPDIR

logger = logging.getLogger(__name__)

def parse_actors(text):
    #116122,佚名,大陆男歌星,YM,yi_ming
    #dummyact = dict(actor_no=0,actor_name='',actor_type='')
    actors = []
    acts = text.split(";")
    for act in acts:
        arr = act.split(",")
        if len(arr) == 5:
            actor = {}
            actor['actor_no'] = arr[0]
            actor['actor_name'] = arr[1]
            actor['actor_type'] = arr[2]
            actor['actor_typeid'] = actortype_name2id(arr[2].decode('utf8'))
            actor['actor_jp'] = arr[3]
            actor['actor_py'] = arr[4]
            actors.append(actor)
    for i in range(len(actors), 4):
        actors.append(None)

    return actors

def parse_empty_record_txt(fname):
    #count = _mysql.actors.get_by_count(text)
    return None

def parse_import_txt(fname, chkfile=False, cleanold=False):
    return None
    
def collect_yinyi(tbl_medias, dbinfo=None):
    fname = os.path.join(TMPDIR, "yinyi_%d.tmp" % int(time.time()))
    tbl_name = "tmp_mediasyinyi"

    try:
        cmd = '%s "drop table if exists %s " ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = '%s "create table %s ( mediano int(11) primary key)" ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        fp = open(fname, 'w+')
        fp.truncate(0)
        ret, out = commands.getstatusoutput("ls /data/TranslateLyricData/*.txt")
        for f in out:
            no, _ = os.path.splitext(f)
            if no.isdigit():
                fp.write("%s\n")
        fp.close()
        cmd = "%s \"load data local infile '%s' into table %s CHARACTER SET UTF8 fields terminated by '|' \" " % (_get_mysql_cmd(dbinfo), fname, tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        #merge yinyi
        cmd = "%s \"update %s set media_yinyi=1 where media_no in (select mediano from %s)\"" % (_get_mysql_cmd(dbinfo), tbl_medias, tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = '%s "drop table if exists %s " ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

    except Exception as ex:
        logger.error(traceback.format_exc())
        return False
    finally:
        if os.path.exists(fname):
            os.remove(fname)
    return True

def collect_dafen(tbl_medias, dbinfo=None):
    fname = os.path.join(TMPDIR, "dafen_%d.tmp" % int(time.time()))
    tbl_name = "tmp_mediasdafen"

    try:
        cmd = '%s "drop table if exists %s " ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = '%s "create table %s ( mediano int(11) primary key)" ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        fp = open(fname, 'w+')
        fp.truncate(0)
        ret, out = commands.getstatusoutput("ls /data/LyricData/*.txt")
        for f in out:
            no, _ = os.path.splitext(f)
            if no.isdigit():
                fp.write("%s\n")
        fp.close()
        cmd = "%s \"load data local infile '%s' into table %s CHARACTER SET UTF8 fields terminated by '|' \" " % (_get_mysql_cmd(dbinfo), fname, tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        #merge dafen
        cmd = "%s \"update %s set media_dafen=1 where media_no in (select mediano from %s)\"" % (_get_mysql_cmd(dbinfo), tbl_medias, tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
 
        cmd = '%s "drop table if exists %s " ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))


    except Exception as ex:
        logger.error(traceback.format_exc())
        return False
    finally:
        if os.path.exists(fname):
            os.remove(fname)
    return True

def _get_mysql_cmd(dbinfo=None):
    if dbinfo:
        return "mysql -h %s -u%s -p%s karaok -e" % (dbinfo['host'], dbinfo['user'], dbinfo['passwd'])
    else:
        return 'mysql -h 127.0.0.1 -uroot -pThunder#123 karaok -e'

def scan_all_videofiles(dbinfo={}):
    tbl_name = 'media_files'
    fname = os.path.join(TMPDIR, 'filepath_%d.tmp' % int(time.time()))
    try:
        fp = os.popen('find /video/ -iname "*.ts" -o -iname "*.mpg" -o -iname "*.ls" -o -iname "*.lss"')
        dfp = open(fname, "w+")
        for line in fp:
            line = line.strip()
            _, no = os.path.split(line)
            no, _ = os.path.splitext(no)
            if no.isdigit():
                dfp.write("%s|1|%s\n" % (no, line))
        dfp.close()

        cmd = '%s "delete from mediafiles" ' % _get_mysql_cmd(dbinfo)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = "%s \"load data local infile '%s' into table mediafiles CHARACTER SET UTF8 fields terminated by '|' \" " % (_get_mysql_cmd(dbinfo), fname)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = '%s "update medias left join mediafiles on medias.media_no = mediafiles.media_no and medias.media_newadd=1 set medias.media_file = mediafiles.media_file;"' % _get_mysql_cmd(dbinfo)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

    except Exception as ex:
        logger.error(traceback.format_exc())
        return False
    finally:
        if os.path.exists(fname):
            os.remove(fname)
    return True

def loadCloudMusic_fromfile(fname, dbinfo={}):
    if not os.path.exists(fname):
        return False
    try:
        actors = {}
        dfile = "%s.%d" % (fname, int(time.time()))
        actfile = "%s.%d.act" % (fname, int(time.time()))
        dfp = open(dfile, "w+")
        afp = open(actfile, "w+")
        i = 0
        for line in codecs.open(fname, encoding='utf-8-sig'):
            arr = line.strip().split('|')
            if len(arr) < 23:
                continue
            acts = parse_actors(arr[21])
            for a in acts:
                if not a:
                    continue
                actors[a['actor_no']] = a
            #字段详情：
            #   1      2    3     4   5        6       7      8     9   10    11   12    13    14     15     16     17         18      19     20       21    22   23
            #编号|歌曲名称|简拼|全拼|语言|歌曲格式|歌曲音频|音量|版本号|笔划|笔画|新歌|中文发|高清|语言类型|左声道|右声道|歌曲视频|替换内容|歌曲主题|3D主题|歌星|授权值
            #4000072|空姐之歌|KJZG|kong_jie_zhi_ge|国语|DVD|MPEG|6|37.8|8|4541|0|0|0|0|2|1|2||流行歌曲|影视金曲|116122,佚名,大陆男歌星,YM,yi_ming|0
            #   1      2        3           4       5    6   7   8  9   10  11 12          18    20       21      22                              23
            dfp.write("%s|%s|%s|%s|%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|" \
                    "%s|%s|%s|%s|%s|%s\n"\
                            % (arr[0], arr[1], len(arr[2]), arr[14], lanaugages_name2id(arr[4]), arr[4], arr[19], arr[20],
                        acts[0].get('actor_name') if acts[0] else '', acts[1].get('actor_name') if acts[1] else '', 
                        acts[2].get('actor_name') if acts[2] else '', acts[3].get('actor_name') if acts[3] else '', 
                        arr[5], arr[15], arr[16], 1, '',
                        arr[17], arr[6], arr[7], arr[2], arr[3],
                        arr[9], arr[10], '', arr[11],
                        0,0,1,1,0,
                        acts[0].get('actor_no') if acts[0] else '', acts[1].get('actor_no') if acts[1] else '', 
                        acts[2].get('actor_no') if acts[2] else '', acts[3].get('actor_no') if acts[3] else '', 
                        0, 0, '', 0, 0, 0))
            i += 1
        dfp.close()
        logger.debug("get %d lines from cloud music info file, saved to file: %s" % (i, dfile))

        for ano in actors:
            afp.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" \
                    % (actors[ano]['actor_no'],actors[ano]['actor_name'],"",\
                    actors[ano]['actor_typeid'],actors[ano]['actor_type'],\
                    actors[ano]['actor_py'],actors[ano]['actor_jp'],\
                    0,0,0))
        medias_tmp = "tmp_medias"
        actors_tmp = "tmp_actors"
        cmd = '%s "drop table if exists %s" ' % (_get_mysql_cmd(dbinfo), medias_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        cmd = '%s "drop table if exists %s"' % (_get_mysql_cmd(dbinfo), actors_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        cmd = '%s "create table %s (select * from medias limit 0)" ' % (_get_mysql_cmd(dbinfo), medias_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        cmd = '%s "create table %s (select * from actors limit 0)" ' % (_get_mysql_cmd(dbinfo), actors_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        cmd = "%s \"load data local infile '%s' into table %s CHARACTER SET UTF8 fields terminated by '|' \" " % (_get_mysql_cmd(dbinfo), dfile, medias_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        cmd = "%s \"load data local infile '%s' into table %s CHARACTER SET UTF8 fields terminated by '|'\" " % (_get_mysql_cmd(dbinfo), actfile, actors_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        if not collect_yinyi(medias_tmp):
            logger.error("failed to collect dafen info")

        if not collect_dafen(medias_tmp):
            logger.error("failed to collect dafen info")

        logger.info("Success parse medias info %d medias, %d actors" % (i, len(actors)))
        cmd = "%s \"update %s set media_newadd=1\" " % (_get_mysql_cmd(dbinfo), medias_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        cmd = "%s \"insert ignore into medias (select * from %s)\" " % (_get_mysql_cmd(dbinfo), medias_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        logger.info("Success merged medias")

        #原来有文件路径的，不做修改（担心有歌曲有重复文件，给改的不一样了，维持现状）
        cmd = "%s \"update medias set media_newadd=0 where media_file <> '' \" " % (_get_mysql_cmd(dbinfo))
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        logger.info("Success merged medias")

        #原来没有文件路径的，设为新加记录，后面关联文件的时候，会补上文件路径（如果有的话）
        cmd = "%s \"update medias set media_newadd=1 where media_file = '' \" " % (_get_mysql_cmd(dbinfo))
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        logger.info("Success merged medias")


        cmd = "%s \"insert ignore into actors (select * from %s)\" " % (_get_mysql_cmd(dbinfo), actors_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        logger.info("Success merged actors")

        '''
        cmd = "%s \"drop table if exists %s; drop table if exists %s\" " % (_get_mysql_cmd(dbinfo), medias_tmp, actors_tmp)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        logger.info("Success cleaned table %s,%s" % (medias_tmp, actors_tmp))
        '''

        ret = scan_all_videofiles(dbinfo)
        if ret:
            logger.debug("Success update all media file path")
        else:
            logger.debug("Failed to update all media file path")
        return True

        #清除新加歌的标识位，避免以后有影响。
        cmd = "%s \"update medias set media_newadd=0 \" " % (_get_mysql_cmd(dbinfo))
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        logger.info("Success merged medias")


    except Exception as ex:
        logger.error(traceback.format_exc())

    finally:
        #if os.path.exists(dfile):
        #    os.remove(dfile)
        #if os.path.exists(actfile):
        #    os.remove(actfile)
        pass
    return False

def load_allowdel_medias(fname, dbinfo=None):
    if not os.path.exists(fname):
        return False
    tbl_name = 'medias_allowdel'
    try:
        cmd = '%s "drop table if exists %s" ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = '%s "create table %s (select media_no from medias limit 0)" ' % (_get_mysql_cmd(dbinfo), tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))

        cmd = "%s \"load data local infile '%s' into table %s CHARACTER SET UTF8 fields terminated by '|' \" " % (_get_mysql_cmd(dbinfo), fname, tbl_name)
        ret, out = commands.getstatusoutput(cmd)
        if ret:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
        else:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
        return True
    except Exception as ex:
        logger.error(traceback.format_exc())
    return False

def load_musicinfo_fromfile(fname, dbinfo=None):
    sql = "load data low_priority local infile '%s' into table cloud_musicinfo character set utf8 fields terminated by '\\t' enclosed by '\\\"'" % (fname)
    cmd = '%s "%s" ' % (_get_mysql_cmd(dbinfo), sql)
    try:
        ret, out = commands.getstatusoutput(cmd)
        if ret == 0:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
            return True
        else:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
            return False
    except Exception as e:
        logger.error(traceback.format_exc())
    return False

def clean_musicinfo():
    sql = "delete from cloud_musicinfo"
    my_session = _mysql.get_session('karaok', True)
    try:
        ret = my_session.execute(sql)
        my_session.commit()
        logger.debug("delete from cloud_musicinfo, return: %s" % ret)
        return True
    except Exception as e:
        logger.error(traceback.format_exc())
        my_session.rollback()
    finally:
        my_session.close()
    return False

def load_musicinfo_bysource(fname, dbinfo=None):
    cmd = '%s "source %s" ' % (_get_mysql_cmd(dbinfo), fname)
    try:
        ret, out = commands.getstatusoutput(cmd)
        if ret == 0:
            logger.debug("%s\n[ret=%d]:%s" % (cmd, ret, out))
            return True
        else:
            logger.error("%s\n[ret=%d]:%s" % (cmd, ret, out))
            return False
    except Exception as e:
        logger.error(traceback.format_exc())
    return False
