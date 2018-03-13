#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import json
import time
import codecs
import commands
import traceback

from tornado import gen
from control.languages import get_all_languages
from control.actortype import get_all_actortype
from web.base import WebBaseHandler
from orm.mm import *
from orm import orm as _mysql
from pymysql import escape_string
from web.websource import executeSendMessage
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

logger = logging.getLogger(__name__)

DEFAULT_CODES=['gbk','gb2312','utf8','GB18030','utf16','big5']
tmp_path = "/data/tmp"
media_status = 0
#库文件上传
class mediaUploadHandler(WebBaseHandler):
    @gen.coroutine
    def post(self):
        ret = {}
        #upload_path = os.path.join(os.path.dirname(__file__),'importTxt')
        #if not os.path.isdir(upload_path):
        #    os.makedirs(upload_path)
        #fileN = self.get_argument('fileName', '')
        #filepath = os.path.join(upload_path,fileN)

        #cannot use /tmp here , since we may don't have enought space there
        if not os.path.isdir(tmp_path):
            os.makedirs(tmp_path)
        filepath = os.path.join(tmp_path, 'media_text_%d.tmp' % int(time.time()))
        file_metas = self.request.files['file']
        meta = file_metas[0]
        with open(filepath,'w') as up:
            up.write(meta['body'])
        up.close()
        ret['code'] = 0
        ret['path'] = filepath
        self.send_json(ret)

# 库文件导入
class mediaParseHandler(WebBaseHandler):
    executor = ThreadPoolExecutor(2)
    def parse_actors(self, actinfo, actnos, all_actortype):
        acts = {}
        # actnos = actnos.split(',')
        if not actinfo:
            return []

        arr = actinfo.split(',')
        if len(arr) % 4 != 0 or len(arr) < 4:
            return []
        i = 0
        for i in range(0, len(actnos)):
            act = {}
            j = i * 4
            act['name'] = arr[j]
            act['des'] = arr[j]
            act['type'] = arr[j + 1]
            act['typeid'] = 0
            for k in all_actortype:
                if k['actortype_name'] == act['type']:
                    act['typeid'] = int(k['actortype_id'])
            act['jp'] = arr[j + 2]
            act['py'] = arr[j + 3]
            acts[actnos[i]] = act
        return acts

    @run_on_executor
    def get(self):
        global media_status
        if media_status != 0:
            ret = {}
            ret['code'] = -1
            ret['msg'] = '正在导入数据中，无法处理新的请求'
            self.send_json(ret)
            return
        media_status = 1
        newadd = '1'
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        all_lang = get_all_languages()
        all_actortype = get_all_actortype()
        media_data = 'REPLACE INTO karaok.medias(media_no,media_name,\
                      media_namelen,media_langtype,media_langid,media_lang,media_tag1,\
                      media_tag2,media_actname1,media_actname2,media_actname3,media_actname4,media_carria,media_yuan,\
                      media_ban,media_svrgroup,media_file,media_style,\
                      media_audio,media_volume,media_jp,media_py,media_strok,\
                      media_stroks,media_lyric,media_isnew,media_clickm,\
                      media_clickw,media_click,media_type,media_actno1,\
                      media_actno2,media_actno3,media_actno4,media_dafen,\
                      media_climax,media_climaxinfo,media_yinyi,media_light,media_newadd) \
                      VALUES({},"{}",{},{},{},"{}","{}","{}","{}","{}","{}","{}","{}",{},{},{},\
                     "{}",{},"{}",{},"{}","{}",{},"{}","{}",{},{},{},{},{},{},{},{},{},{},{},"{}",{},{},{});'
        actor_data = 'REPLACE INTO karaok.actors (actor_no,actor_name,actor_des,actor_typeid,\
                      actor_type,actor_py,actor_jp,actor_click,actor_clickw,\
                     actor_clickm) VALUES({},"{}","{}",{},"{}","{}","{}",{},{},{});'
        lsy_data = "REPLACE INTO karaok.cloud_musicshadow (Shadow_no,savepath,music_type)\
                      VALUES({},'{}','{}');"
        ret = {}
        ret['code'] = 1
        isdelete = int(self.get_argument('isdelete', 0))
        get_media_count = 'select count(*) from medias;'
        cursor.execute(get_media_count)
        p = cursor.fetchall()
        count = p[0][0]
        if count == 0:
            isdelete = 1

        if isdelete == 1:
            sql_del = "delete from medias;\
                       delete from actors;\
                       delete from cloud_musicshadow;"
            cursor.execute(sql_del)
            medias_fp = open(os.path.join(tmp_path, 'medias.data'), 'w+')
            actors_fp = open(os.path.join(tmp_path, 'actors.data'), 'w+')
            lsy_fp = open(os.path.join(tmp_path, 'lsy.data'), 'w+')
        else:
            media_fp = open(os.path.join(tmp_path, 'media.data'), 'w+')
        try:
            obj = {"title":"消息提示","content":"当前已开始解析库文件","state":1}
            executeSendMessage(obj)
            upload_path=os.path.join(os.path.dirname(__file__),'importTxt')
            if not os.path.isdir(upload_path):
                os.makedirs(upload_path)
            #直接传入上一个Upload请求返回的文件路径（绝对路径）
            filepath = self.get_argument('fileName', '')
            result = []
            act_list = []
            try:
                fp = open(filepath)
            except Exception as ex:
                logger.error(traceback.format_exc())
                logger.error('failed to open  file')
                return
            for line in fp:

                line = line.strip()
                for i in DEFAULT_CODES:
                    try:
                        line = line.decode(i).encode('utf-8')
                        break
                    except:
                        continue
                arr = line.split('|')
                if len(arr) < 22:
                    logger.error(line)
                    continue
                if arr[0] == '广告':
                    media_type = '2'
                elif arr[0] == '电影':
                    media_type = '3'
                else:
                    media_type = '1'

                media_name = arr[1]
                media_lang = arr[2]
                media_langid = 0
                for i in all_lang['matches']:
                    if i['lang_name'].encode('utf8') == media_lang:
                        media_langid = int(i['lang_id'])

                media_tags = arr[3]
                media_tag1 = ''
                media_tag2 = ''
                tags = media_tags.split(',')
                index = len(tags)
                if index > 0:
                    media_tag1 = tags[0]
                if index > 1:
                    media_tag2 = tags[1]

                media_actname1 = ''
                media_actname2 = ''
                media_actname3 = ''
                media_actname4 = ''

                media_actno1 = '0'
                media_actno2 = '0'
                media_actno3 = '0'
                media_actno4 = '0'
                media_actors = arr[4]
                #载体DVD等等
                media_carria = arr[5]
                #原唱左声道
                media_yuan = arr[6]
                #伴唱右声道
                media_ban = arr[7]
                #maybe the filepath
                media_file = arr[8]
                fno = media_file.split('.')
                media_no = fno[0]
                media_file = ''
                media_videotype = arr[9]
                media_volume = arr[10]
                media_audio = arr[11]
                media_jp = arr[12]
                media_namelen = str(len(media_jp))
                media_langtype = arr[13]
                media_stroke = arr[14]
                media_strokes = arr[15]
                #media_heng = arr[15]
                media_py = arr[19]
                media_actnos = arr[21]
                acts = media_actnos.split(';')
                index = len(acts)
                new_acts = self.parse_actors(media_actors, acts, all_actortype['matches'])

                i = 0
                for ano in new_acts:
                    if i == 0:
                        media_actno1 = ano
                        media_actname1 = new_acts[ano]['name']
                    elif i == 1:
                        media_actno2 = ano
                        media_actname2 = new_acts[ano]['name']
                    elif i == 2:
                        media_actno3 = ano
                        media_actname3 = new_acts[ano]['name']
                    elif i == 3:
                        media_actno4 = ano
                        media_actname3 = new_acts[ano]['name']
                    i += 1
                    if ano not in act_list:
                        act_list.append(ano)
                        if isdelete == 1:
                            actors_fp.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(ano, escape_string(new_acts[ano]['name']), escape_string(new_acts[ano]['des']), new_acts[ano]['typeid'], new_acts[ano]['type'],new_acts[ano]['py'], new_acts[ano]['jp'], '0', '0', '0'))
                            actors_fp.write('\n')
                        else:
                            media_fp.write(actor_data.format(ano, escape_string(new_acts[ano]['name']), escape_string(new_acts[ano]['des']), new_acts[ano]['typeid'], new_acts[ano]['type'],new_acts[ano]['py'], new_acts[ano]['jp'], '0', '0', '0'))
                            media_fp.write('\n')

                media_lyric = ''
                media_isnew = arr[16]
                media_click = '0'
                media_clickm = '0'
                media_clickw = '0'
                media_dafen = '0'
                media_climax = 0
                media_climaxinfo = '0'
                media_yinyi = '0'
                media_light = '0'
                media_svrgroup = '1'
                media_stars = 1
                no_str = str(media_no)
                if not no_str.startswith('55'):
                    if isdelete == 1:
                        medias_fp.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format \
                                (media_no, escape_string(media_name), media_namelen, media_langtype, media_langid, media_lang,\
                                media_tag1, media_tag2, escape_string(media_actname1), escape_string(media_actname2), escape_string(media_actname3), escape_string(media_actname4), media_carria, \
                                media_yuan, media_ban, media_svrgroup, media_file,\
                                media_videotype, media_audio, media_volume, \
                                media_jp, media_py,\
                                media_stroke, media_strokes, media_lyric, media_isnew, \
                                media_clickm, media_clickw, media_click, \
                                media_type, media_stars, media_actno1, media_actno2, media_actno3, media_actno4, \
                                media_dafen, media_climax, media_climaxinfo, media_yinyi, media_light, newadd))
                        medias_fp.write("\n")
                    else:
                        media_fp.write(media_data.format \
                                (media_no, escape_string(media_name), media_namelen, media_langtype, media_langid, media_lang,\
                                media_tag1, media_tag2, escape_string(media_actname1), escape_string(media_actname2), escape_string(media_actname3), escape_string(media_actname4), media_carria, \
                                media_yuan, media_ban, media_svrgroup, media_file,\
                                media_videotype, media_audio, media_volume, \
                                media_jp, media_py,\
                                media_stroke, media_strokes, media_lyric, media_isnew, \
                                media_clickm, media_clickw, media_click, \
                                media_type, media_actno1, media_actno2, media_actno3, media_actno4, \
                                media_dafen, media_climax, media_climaxinfo, media_yinyi, media_light, newadd))
                        media_fp.write("\n")
                else:
                    if isdelete == 0:
                        media_fp.write(lsy_data.format(media_no, '', media_tag1))
                    else:
                        lsy_fp.write("{}|{}|{}".format(media_no, '', media_tag1))
            if isdelete == 0:
                media_fp.close()
            else:
                medias_fp.close()
                actors_fp.close()
                lsy_fp.close()

            media_status = 2
            fp.close()
            try:
                if isdelete == 0:
                    commands.getoutput('/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 < %s' % os.path.join(tmp_path, 'media.data'))
                else:
                    sql_medias = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.medias fields terminated by '|';"''' % os.path.join(tmp_path, 'medias.data')
                    os.system(sql_medias)
                    sql_actors = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.actors fields terminated by '|';"''' % os.path.join(tmp_path, 'actors.data')
                    os.system(sql_actors)
                    sql_lsy = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.cloud_musicshadow fields terminated by '|';"''' % os.path.join(tmp_path, 'lsy.data')
                    os.system(sql_lsy)
            except:
                media_status = -1
            #--------------------------------finish parse---------------------------
            obj = {"title":"消息提示","content":"解析库文件完成,开始扫描磁盘","state":1}
            executeSendMessage(obj)

            print '*'*20
            ret['code'] = 0
        except:
            logger.error(traceback.format_exc())
            print traceback.format_exc()
            ret['error']=traceback.format_exc()
            pass

        #是否插入空纪录
        isload = self.get_argument('isload', 0)

        #ts_output = commands.getoutput("ls -r /video/*/* | grep -E '[0-9]{7}.ts'$")
        ts_output =commands.getoutput('find /video/ -iname "*.ts" -o -iname "*.mpg"')
        ts_output = ts_output.split('\n')
        r = r'[0-9]{7}'
        #ts_no1 = re.findall(r, ts_output)

        media_file = open(os.path.join(tmp_path, 'media_file.data'), 'w+')

        for i in ts_output:
            media_no = re.findall(r, i)
            media_file.write("{}|{}|{}".format(media_no[0], 1, i).decode('utf-8').encode('utf-8'))
            media_file.write("\n")

        media_file.close()
        sql_setname = 'SET character_set_database = utf8 ;'
        cursor.execute(sql_setname)
        sql_delmedifile = "delete from mediafiles;"
        cursor.execute(sql_delmedifile)
        sql_load = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.mediafiles fields terminated by '|';"''' % os.path.join(tmp_path, 'media_file.data')
        try :
            os.system(sql_load)
            sql_inner = "update medias inner join mediafiles on medias.media_no = mediafiles.media_no and medias.media_newadd = 1 set medias.media_file = mediafiles.media_file;"
            cursor.execute(sql_inner)
        except:
            media_status = -1

        #sync climax info
        sql_climax = "update medias inner join mediaclimax on medias.media_no = mediaclimax.media_no set medias.media_climaxinfo = mediaclimax.media_climaxinfo, medias.media_climax = 1;"
        cursor.execute(sql_climax)

        if int(isload) == 0:
            sql_del = "delete from medias where medias.media_file='' and medias.media_newadd =1;"
            cursor.execute(sql_del)
        sql_getallcount = 'select count(*) from medias where medias.media_newadd=1;'
        cursor.execute(sql_getallcount)
        p = cursor.fetchall()
        count = p[0][0]
        sql_reset = "update medias set media_newadd = 0"
        cursor.execute(sql_reset)
        #lyricData fix
        try:
            get_all_lyric = 'ls /opt/thunder/www/LyricData/| grep -E "[0-9]{7}.txt"'
            output = commands.getoutput(get_all_lyric)
            output = output.split('\n')
            tmp_file = open(os.path.join(tmp_path, 'tmp.data'), 'w+')
            for i in output:
                media_no = re.findall(r, i)
                tmp_file.write("{}|{}".format(media_no[0], 1))
                tmp_file.write("\n")
            tmp_file.close()

            sql_load = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.tmp fields terminated by '|';"''' % os.path.join(tmp_path, 'tmp.data')
            os.system(sql_load)
            sql_inner = "update medias inner join tmp on medias.media_no = tmp.media_no  set medias.media_dafen = '1';"
            cursor.execute(sql_inner)
            sql_del = "delete from karaok.tmp;"
            cursor.execute(sql_del)
        except:
            pass
        finally:
            tmp_file.close()

        #yinyin fix
        try:
            get_all_yinyin = 'ls /opt/thunder/www/TranslateLyricData/ | grep -E "[0-9]{7}.txt"'
            output = commands.getoutput(get_all_yinyin)
            output = output.split('\n')
            tmp_file = open(os.path.join(tmp_path, 'tmp.data'), 'w+')
            for i in output:
                media_no = re.findall(r, i)
                tmp_file.write("{}|{}".format(media_no[0], 1))
                tmp_file.write("\n")
            tmp_file.close()
            sql_load = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.tmp fields terminated by '|';"''' % os.path.join(tmp_path, 'tmp.data')
            os.system(sql_load)
            sql_inner = "update medias inner join tmp on medias.media_no = tmp.media_no  set medias.media_yinyi = '1';"
            cursor.execute(sql_inner)
            sql_del = "delete from karaok.tmp;"
            cursor.execute(sql_del)
        except:
            pass
        finally:
            tmp_file.close()

        #dianjilv
        try:
            djl_fp = open('/opt/thunder/twm/web/songInfo/AddSongInfo.dat', 'r+')
            djl_w_fp = open(os.path.join(tmp_path, 'djl.data'), 'w+')
            for line in djl_fp:
                line = line[3:]
                djl_w_fp.write(line)
                djl_w_fp.write('\n')
            djl_w_fp.close()
            djl_fp.close()
            sql_load = '''/opt/local/mysql/bin/mysql --default-character-set=utf8 -h127.0.0.1 -uroot -pThunder#123 -e "LOAD DATA LOCAL INFILE '%s' INTO TABLE karaok.tmp fields terminated by '|';"''' % os.path.join(tmp_path, 'djl.data')
            os.system(sql_load)
            sql_inner = "update medias inner join tmp on medias.media_no = tmp.media_no  set medias.media_click = tmp.status;"
            cursor.execute(sql_inner)
            sql_del = "delete from karaok.tmp;"
            cursor.execute(sql_del)
        except:
            pass
        finally:
            djl_w_fp.close()
            djl_fp.close()

        outData = {}
        outData['mediatypeSize'] = count
        ret['data'] = outData
        cursor.close()
        media_status = 0
        self.send_json(ret)

class getmediainfoHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        ret = {}
        media_no = self.get_argument('media_no', 0)
        res = _mysql.medias.get_by_no(media_no)

        if len(res) >0:
            ret['data'] = {}
            ret['data']['Media_Name'] = res[0]['media_name']
            ret['data']['Language_ID'] = res[0]['media_langid']

            # 遍历所有media type
            ret['data']['MediaType1'] = {}
            ret['data']['MediaType1']['name'] = res[0]['media_tag1']
            ret['data']['MediaType2'] = {}
            ret['data']['MediaType2']['name'] = res[0]['media_tag2']

            ret['data']['Media_HeaderSoundSequence'] = res[0]['media_jp']
            ret['data']['Media_AllSoundSequence'] = res[0]['media_py']
            ret['data']['Actor1'] = {}
            ret['data']['Actor2'] = {}
            ret['data']['Actor3'] = {}
            ret['data']['Actor4'] = {}
            ret['data']['Actor1']['Actor_Name']= res[0]['media_actname1']
            ret['data']['Actor2']['Actor_Name']= res[0]['media_actname2']
            ret['data']['Actor3']['Actor_Name']= res[0]['media_actname3']
            ret['data']['Actor4']['Actor_Name']= res[0]['media_actname4']
            #volume
            ret['data']['Media_IsReserved2'] = res[0]['media_volume']
            #stroke
            ret['data']['Media_HeadStroke'] = res[0]['media_strok']
            #bihua
            ret['data']['Media_StrokeNum'] = res[0]['media_stroks']
            ret['data']['Carrier_Name'] = res[0]['media_carria']
            ret['data']['Audio_Name'] = res[0]['media_audio']
            ret['data']['Media_IsReserved3'] = res[0]['media_yinyi']
            ret['data']['MediaManage_OriginalTrack'] = res[0]['media_yuan']
            ret['data']['MediaManage_AccompanyTrack'] = res[0]['media_ban']
            ret['data']['MediaManage_OrderCount'] = res[0]['media_click']
            if res[0]['media_type'] == 3:
                ret['data']['Media_IsMovie'] = 1
            if res[0]['media_type'] == 1:
                ret['data']['Media_IsKaraok'] = 1
            if res[0]['media_type'] == 2:
                ret['data']['Media_IsAds'] = 1
            ret['data']['isNewSong'] = res[0]['media_isnew']
            ret['data']['Media_Lyric'] = res[0]['media_lyric']
            ret['data']['Media_no'] = res[0]['media_no']
            ret['data']['Lights'] = res[0]['media_light']
            ret['data']['Media_IsReserved3'] = res[0]['media_style']
        else:
            ret['msg'] = '未找到该文件的纪录'

        self.send_json(ret)
        return


class updatemediaHandler(WebBaseHandler):
    def Is_actor_exist(self, actname):
        ret = _mysql.actors.get_by_name(actname)
        return ret
    def post(self):
        result = {}
        try:
            # get arguments
            info = json.loads(self.request.body)
        except Exception as ex:
            result['code'] = 1
            result['msg'] = '参数错误'
            self.send_json(result)
            return

        data = {}
        data['media_no'] = info.get('serialno', 0)
        data['media_name'] = info.get('iname', '')
        data['media_langid'] = int(info.get('ltype',''))
        data['media_lang'] = info.get('lname','')
        # 遍历所有media type
        data['media_tag1'] = info.get('type1', '')
        data['media_tag2'] = info.get('type2', '')
        data['media_jp'] = info.get('jianpin', '')
        data['media_py'] = info.get('pinyin', '')
        data['media_actname1'] = info.get('sname1', '')
        data['media_actname2'] = info.get('sname2', '')
        data['media_actname3'] = info.get('sname3', '')
        data['media_actname4'] = info.get('sname4', '')
        Is_data_ok = True
        for i in range(4):
            if data['media_actname{}'.format(i+1)] != '':
                res = self.Is_actor_exist(data['media_actname{}'.format(i+1)])
                if res == None and Is_data_ok == True:
                    Is_data_ok = False
                elif res != None:
                    data['media_actno{}'.format(i+1)] = res[0]['actor_no']

        if Is_data_ok != True:
            result['code'] = 1
            result['msg'] = '歌星信息错误，如果是新增歌星，请先在歌星管理中添加'
            self.send_json(result)
            return

        # volume
        data['media_volume'] = info.get('volume', 0)
        if data['media_volume'] == '':
            data['media_volume'] = 0
        # stroke
        data['media_strok'] = info.get('stroke', 0)
        if data['media_strok'] == '':
            data['media_strok'] = 0
        # bihua
        data['media_stroks'] = info.get('bihua', '')
        data['media_carria'] = info.get('videoformat', '')
        data['media_audio'] = info.get('audioformat', '')
        data['media_yuan'] = info.get('ztrack', 0)
        if data['media_yuan'] == '':
            data['media_yuan'] = 0
        data['media_ban'] = info.get('ytrack', 0)
        if data['media_ban'] == '':
            data['media_ban'] = 0
        data['media_click'] = info.get('ordercount', 0)

        if info.get('IsKaraok', 0) == 1:
            data['media_type'] = 1
        if info.get('IsAds', 0) == 1:
            data['media_type'] = 2
        if info.get('IsMovie', 0) == 1:
            data['media_type'] = 3

        data['media_isnew'] = info.get('isnew', 0)
        data['media_lyric'] = info.get('lyric', '')

        data['media_light'] = info.get('lights', 0)
        data['media_style'] = info.get('videotype', 0)
        _mysql.medias.update(data)

        result['code'] = 0
        self.send_json(result)
        return


class deletenullHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        '''
        sql_count = "select count(*) from medias where medias.media_file='' or medias.media_file is null;"
        cursor.execute(sql_count)
        p = cursor.fetchall()
        count = p[0][0]
        '''
        logger.error('delete-null: clean null medias')
        sql_del = "delete from medias where medias.media_file='' or medias.media_file is null;"
        m_count = cursor.execute(sql_del)
        logger.error('delete-null: clean flag in actors')
        sql_del = "update actors set actor_newadd = 1"
        cursor.execute(sql_del)
        logger.error('delete-null: set flag for actor1')
        sql_del = "update actors set actor_newadd = 0 where actor_no in (select media_actno1 from medias) "
        cursor.execute(sql_del)
        logger.error('delete-null: set flag for actor2')
        sql_del = "update actors set actor_newadd = 0 where actor_no in (select media_actno2 from medias where media_actno2 > 0) "
        cursor.execute(sql_del)
        logger.error('delete-null: set flag for actor3')
        sql_del = "update actors set actor_newadd = 0 where actor_no in (select media_actno3 from medias where media_actno3 > 0) "
        cursor.execute(sql_del)
        logger.error('delete-null: set flag for actor4')
        sql_del = "update actors set actor_newadd = 0 where actor_no in (select media_actno4 from medias where media_actno3 > 0) "
        cursor.execute(sql_del)

        #sql_del = "delete from actors where actor_no not in (select media_actno1 from medias) "\
        #        "and actor_no not in (select media_actno2 from medias) and "\
        #        "actor_no not in (select media_actno3 from medias) and "\
        #        "actor_no not in (select media_actno4 from medias);"
        sql_del = "delete from actors where actor_newadd = 1 "
        a_count = cursor.execute(sql_del)
        logger.error('删除成功（共删除：%d歌曲，%d歌星）' % (m_count, a_count))

        cursor.close()
        ret = {}
        ret['code'] = 0
        ret['count'] = m_count
        ret['msg'] = '删除成功（共删除：%d歌曲，%d歌星）' % (m_count, a_count)
        self.send_json(ret)
        return

class searchlHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        page = int(self.get_argument('page', 0))
        psize = int(self.get_argument('psize', 0))
        text = self.get_argument('text', '').encode('utf-8')

        if text == '':
            sql_selectall = "select * from karaok.medias limit {} offset {};".format(psize, (page-1)*psize)
            cursor.execute(sql_selectall)
        else:
            try:
                media_no = int(text)
                sql_searchtxt = "select * from karaok.medias where medias.media_no={}".format(media_no)
            except:
                sql_search = "select * from karaok.medias where match \
                              (media_name, media_jp, media_actname1,\
                               media_actname2, media_actname3, media_actname4) \
                               against('{}' IN BOOLEAN MODE) or media_lang = '{}' \
                                or media_tag1 = '{}' or media_tag2 = '{}' \
                               limit {} offset {};"

                sql_searchtxt = sql_search.format(text, text, text, text, psize, (page-1)*psize)
            cursor.execute(sql_searchtxt)

        res = cursor.fetchall()
        res_tmp = []
        if res != None and res != ():
            for i , j in enumerate(res):
                res_tmp.append({})
                res_tmp[i]['Media_SerialNo'] = j[0]
                res_tmp[i]['Media_Name'] = j[1]
                res_tmp[i]['Actor_Name1'] = j[8]
                res_tmp[i]['Actor_Name2'] = j[9]
                res_tmp[i]['Actor_Name3'] = j[10]
                res_tmp[i]['Actor_Name4'] = j[11]
                res_tmp[i]['MediaType_Name1'] = j[6]
                res_tmp[i]['MediaType_Name2'] = j[7]
                res_tmp[i]['Language_Name'] = j[5]
                res_tmp[i]['Media_File'] = j[16]
                res_tmp[i]['Carrier'] = j[12]
                res_tmp[i]['Audio_type'] = j[18]
        cursor.close()
        ret = {}
        ret['data'] = {}
        ret['data']['matches'] = res_tmp
        ret['total'] = len(res_tmp)
        self.send_json(ret)
        return

class searchcountHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        result = {}
        result['code'] = 1
        result['msg'] = ''
        result['data'] = {}
        conn = getDataBaseConnection()
        cursor = conn.cursor()
        text = self.get_argument('text', '').encode('utf-8')
        if text == '':
            sql_getallcount = 'select count(*) from medias;'
            n = cursor.execute(sql_getallcount)

        else:
            sql_search = "select count(*) from karaok.medias where match \
                                    (media_name, media_jp, media_actname1,\
                                     media_actname2, media_actname3, media_actname4) \
                                     against('{}' IN BOOLEAN MODE) or media_no = '{}' \
                                     or media_lang = '{}' or media_tag1 = '{}' or media_tag2 = '{}';"

            sql_searchtxt = sql_search.format(text, text, text, text, text)
            n = cursor.execute(sql_searchtxt)

        p = cursor.fetchall()
        count = p[0][0]
        result['data']['total'] = count
        cursor.close()
        self.send_json(result)
        return

class mediadelHandler(WebBaseHandler):
    @gen.coroutine
    def post(self):
        result = {}

        media_no = self.get_argument('AddMedia_SerialNo', 0)
        res = _mysql.medias.get_by_no(media_no)
        media_file = res[0].get('media_file','')
        if media_file != '':
            del_media = 'rm -rf {}'.format(media_file)
            commands.getoutput(del_media)
        _mysql.medias.del_by_no(media_no)
        result['code'] = 0
        result['msg'] = '删除成功'
        self.send_json(result)
        return


class loopHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'list':
            conn = getDataBaseConnection()
            cursor = conn.cursor()
            page = int(self.get_argument('page', 0))
            psize = int(self.get_argument('psize', 0))
            text = self.get_argument('text', '').encode('utf-8')
            loop_type = int(self.get_argument('type', 0))
            if loop_type == 3:
                loop_type = 2
            if text == '' and loop_type != 0:
                sql_selectall = "select * from karaok.medias where media_type={} limit {} offset {};".format(loop_type, psize, (page-1)*psize)
                cursor.execute(sql_selectall)
            elif loop_type!=0:
                sql_search = "select * from karaok.medias where (match \
                              (media_name, media_jp, media_actname1,\
                               media_actname2, media_actname3, media_actname4) \
                               against('{}' IN BOOLEAN MODE) or media_no = '{}' \
                               or media_lang = '{}' or media_tag1 = '{}' or media_tag2 = '{}') \
                               and media_type = {} limit {} offset {};"

                sql_searchtxt = sql_search.format(text, text, text, text, text, loop_type, psize, (page-1)*psize)
                cursor.execute(sql_searchtxt)
            else:
                sql_selectall = "select * from karaok.medias  join karaok.autoplay on  karaok.medias.media_no = karaok.autoplay.media_no"
                cursor.execute(sql_selectall)

            res = cursor.fetchall()
            res_tmp = []
            if res != None and res != ():
                for i , j in enumerate(res):
                    res_tmp.append({})
                    res_tmp[i]['Media_ID'] = j[0]
                    res_tmp[i]['Media_Name'] = j[1]
                    res_tmp[i]['Actor_Name1'] = j[8]
                    res_tmp[i]['Actor_Name2'] = j[9]
                    res_tmp[i]['Actor_Name3'] = j[10]
                    res_tmp[i]['Actor_Name4'] = j[11]
                    res_tmp[i]['MediaType_Name1'] = j[6]
                    res_tmp[i]['MediaType_Name2'] = j[7]
                    res_tmp[i]['Language_Name'] = j[5]
                    res_tmp[i]['Media_File'] = j[16]
                    res_tmp[i]['Carrier'] = j[12]
                    res_tmp[i]['Audio_type'] = j[18]
            cursor.close()
            ret = {}
            ret['data'] = {}
            ret['data']['matches'] = res_tmp
            ret['total'] = len(res_tmp)
            self.send_json(ret)
            return
        if op == 'count':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = {}
            conn = getDataBaseConnection()
            cursor = conn.cursor()
            text = self.get_argument('text', '').encode('utf-8')
            loop_type  = int(self.get_argument('type', 0))
            if loop_type == 3:
                loop_type = 2

            if text == '' and loop_type !=0:
                sql_getallcount = 'select count(*) from medias where media_type={};'.format(loop_type)
                n = cursor.execute(sql_getallcount)

            else:
                sql_search = "select count(*) from karaok.medias where (match \
                                        (media_name, media_jp, media_actname1,\
                                         media_actname2, media_actname3, media_actname4) \
                                         against('{}' IN BOOLEAN MODE) or media_no = '{}' \
                                         or media_lang = '{}' or media_tag1 = '{}' or media_tag2 = '{}') \
                                         and media_type = {};"

                sql_searchtxt = sql_search.format(text, text, text, text, text, loop_type)
                n = cursor.execute(sql_searchtxt)

            p = cursor.fetchall()
            count = p[0][0]
            result['data']['total'] = count
            cursor.close()
            self.send_json(result)
            return
    @gen.coroutine
    def post(self, op):
        if op == 'del':
            ret = {}
            media_no = self.get_argument('media_no', 0)
            if media_no != 0:
                _mysql.autoplay.del_by_no(media_no)
                ret['code'] = 0
            else:
                ret['code'] = 1
                ret['msg'] = 'wrong para'
            self.send_json(ret)
            return
        if op == 'exchange':
            ret = {}
            media_no1 = self.get_argument('MediaId1', 0)
            media_no2 = self.get_argument('MediaId2', 0)
            if media_no1 != 0 and media_no2 != 0:
                ret1 =  _mysql.autoplay.get_by_no(media_no1)
                ret2 = _mysql.autoplay.get_by_no(media_no2)
                _mysql.autoplay.exchange(ret1[0], ret2[0])
                ret['code'] = 0
            else:
                ret['code'] = 1
                ret['msg'] = 'wrong para'
            self.send_json(ret)
            return
        if op == 'add':
            result = {}
            result['code'] = 1
            media_no = self.get_argument('MediaUserSet_MediaId', 0)
            conn = getDataBaseConnection()
            cursor = conn.cursor()
            sql_getcount = 'select count(*) from autoplay;'
            cursor.execute(sql_getcount)
            p = cursor.fetchall()
            if p[0][0] >= 300:
                result['code'] = 1
                result['msg'] = '公共歌曲达到上限，请先删除一些歌曲再添加'
            elif media_no == 0:
                result['code'] = 1
                result['msg'] = 'wrong param'
            else:
                res = _mysql.medias.get_by_no(media_no)
                res_loop = _mysql.autoplay.get_by_no(media_no)
                if (res != None and res != []) and (res_loop == [] or res_loop == None):
                    data = {}
                    data['media_no'] = media_no
                    data['media_svrgrp'] = 1
                    data['media_file'] = res[0]['media_file']
                    _mysql.autoplay.add(data)
                    result['code'] = 0
                else:
                    result['msg'] = '请不要重复添加'

            self.send_json(result)
            return


class looptypeHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        if op == 'set':
            ret = {}
            ret['code'] = 0
            loop_type  = self.get_argument('type', '')
            conn = getDataBaseConnection()
            cursor = conn.cursor()
            sql = "update config set config_value = {} where config_name = 'Loop_play';".format(loop_type)
            cursor.execute(sql)
            cursor.close()
            self.send_json(ret)
            return
        if op == 'get':
            ret = {}
            ret['code'] = 1
            conn = getDataBaseConnection()
            cursor = conn.cursor()
            sql = "select config_value from config where config_name='Loop_play'"
            cursor.execute(sql)
            res = cursor.fetchall()
            if res != None and res!=():
                ret['data'] = res[0][0]
                ret['code'] = 0
            cursor.close()
            self.send_json(ret)
            return
        if op == 'del':
            ret = {}
            ret['code'] = 0
            conn = getDataBaseConnection()
            cursor = conn.cursor()
            sql = "delete from autoplay"
            cursor.execute(sql)
            cursor.close()
            self.send_json(ret)
            return
    @gen.coroutine
    def post(self, op):
        pass

class statusHandler(WebBaseHandler):
    def get(self):
        global media_status
        data = {'status': media_status}
        self.send_json(data)
