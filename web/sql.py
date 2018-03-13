#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import setting
import logging
import tornado
import traceback
import os
import json
import base64
import codecs
import md5
from tornado import gen
from lib.types import try_to_int
from web.base import WebBaseHandler
from orm.mm import *
from orm.mountdisk import get_all_disk_info, format_disk
import threading
import commands
import urllib
import urllib2
import socket
from orm.scp import scopyIp
from web.websource import executeSendMessage
from orm.actorimg import get_actor_pic

logger = logging.getLogger(__name__)

BOM_CODE={"BOM_UTF8":'utf_8',"BOM_LE":'utf_16_le',"BOM_BE":'utf_16_be'}

DEFAULT_CODES=['utf8','GB18030','gbk','utf16','big5','GB2312']

def decode_file(d):
    for k in BOM_CODE:
        if k==d[:len(k)]:
            code=BOM_CODE[k]
            d=d[len(k):]
            text=d.decode(code)
            return text.splitlines()

    for encoding in DEFAULT_CODES:
        try:
            text=d.decode(encoding)
            return text.splitlines()
        except:
            continue
    raise Exception('解码失败')

def read_file(file_name):
    with open(file_name,'rb')as fn:
        return decode_file(fn.read())


noAndPathMap={}

isStopAdd={}
isStopAdd[0]=False
isAddData={}
isAddData[0]=False



class sql(WebBaseHandler):

    def parse_actors(self, actinfo, actnos):
        acts = {}
        #actnos = actnos.split(',')
        if not actinfo:
            return []

        arr = actinfo.split(',')
        if len(arr) % 4 != 0 or len(arr) < 4:
            return []
        i = 0
        for i in range(0, len(actnos)):
            act = {}
            j = i*4
            act['name'] = arr[j]
            act['des'] = arr[j]
            act['type'] = arr[j+1]
            act['py'] = arr[j+2]
            act['jp'] = arr[j+3]
            acts[actnos[i]] = act
        return acts

    @gen.coroutine
    def get(self,op):
        ret = {}
        ret['code'] = 1
        if op == 'getIsAddData':
            ret['state']=isAddData[0]
            self.send_json(ret)
        if op == 'getTime':
            ret['code'] = 0
            ret['data'] = time.time()
            self.send_json(ret)
        if op == 'selectMediasSequence':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                obj = {}
                obj['Language_ID'] = self.get_argument('Language_ID', '')
                obj['page'] = self.get_argument('page', '0')
                obj['psize'] = self.get_argument('psize', '5')
                list = sp_selectmediassequence(**obj)
                if len(list) > 0:
                    ret['data'] = list
            self.send_json(ret)
        elif op == 'selectMediasSequenceCount':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                obj = {}
                obj['Language_ID'] = self.get_argument('Language_ID', '')
                count = sp_selectmediassequencecount(**obj)
                ret['data'] = count
            self.send_json(ret)
        elif op == 'log':
            file_object = open('/var/log/thunder/twm.log')
            text=""
            try:
                 text = file_object.read( )
            finally:
                 file_object.close()
            self.send_string(text)
        elif op == 'logConsole':
            file_object = open('/var/log/thunder/twm-console.log')
            text=""
            try:
                 text = file_object.read( )
            finally:
                 file_object.close()
            self.send_string(text)
        elif op == 'selectMediaDetailsForType':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                obj = {}
                obj['type'] = self.get_argument('type', '')
                obj['page'] = self.get_argument('page', '0')
                obj['psize'] = self.get_argument('psize', '5')
                list = sp_selectMediaDetailsForType(**obj)
                if len(list) > 0:
                    ret['data'] = list
            self.send_json(ret)

        elif op == 'updateMediaDetailsCount':
            no = self.get_argument('no', '')
            count = self.get_argument('count', '0')
            sp_updateMediaDetailsCount(no,count)
            ret={}
            ret['code']=0
            self.send_json(ret)


        elif op == 'selectMediaTypeFromMediaDetailsCount':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                type = self.get_argument('type', '')
                count = sp_selectMediaTypeFromMediaDetailsCount(type)
                ret['data'] = count
            self.send_json(ret)


        elif op == 'getMediasInfo':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                no = self.get_argument('Media_SerialNo', '')
                media={}
                media['Media_SerialNo']=no
                res = sp_getexportdata(**media)
                if len(res)>0:
                    m_exportdata = res[0]
                    mediaType = sp_getmediatype(**m_exportdata)
                    actorList = sp_getacotr(**m_exportdata)
                    isNewSong = sp_isnewsong(**m_exportdata)
                    i = 1
                    for media in mediaType:
                        m_exportdata['MediaType'+str(i)] = {}
                        m_exportdata['MediaType'+str(i)]['name'] = media['MediaType_Name']
                        i+=1
                    i = 1
                    m_exportdata['Actor'] = {}
                    for actor in actorList:
                        m_exportdata['Actor'+str(i)] = {}
                        m_exportdata['Actor'+str(i)]['Actor_Name'] = actor['Actor_Name']
                        m_exportdata['Actor'+str(i)]['ActorType_Name'] = actor['ActorType_Name']
                        m_exportdata['Actor'+str(i)]['Actor_HeaderSoundSequence'] = actor['Actor_HeaderSoundSequence']
                        m_exportdata['Actor'+str(i)]['Actor_AllSoundSequence'] = actor['Actor_AllSoundSequence']
                        i+=1
                    m_exportdata['isNewSong'] = isNewSong
                    ret['data'] = m_exportdata
                else:
                    ret['msg']='未找到该文件信息记录,请删除该上传文件后重试'
            self.send_json(ret)
        elif op == 'getMediasNoFromFileName':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                obj = {}
                obj['Media_Name'] = self.get_argument('Media_Name', '')
                no = sp_getmediasfromfilename(**obj)
                ret['data'] = no
                ret['code']=0
            self.send_json(ret)
        if op == 'scanVideos':
            tick = time.time()
#             scanvideos("/video/")
            fileMap = {}
            repeatMap = []

            ip1= self.get_argument('ip1', '')
            ip2= self.get_argument('ip2', '')

            print ip1
            print ip2

            ipList=[]

            outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")

            ipList=outp.split('\n')

            ip1Result=''
            ip2Result=''

            bol = False
            for i in ipList:
                if i==ip1:
                    bol=True
            if ip1!='':
                if (bol):
                    ip1Result = commands.getoutput('ls -R /video/*')
                else:
                    response1 = urllib2.urlopen('http://'+ip1+':8888/sql/getFileOutput')
                    ip1Result = response1.read()

            bol = False
            for i in ipList:
                if i==ip2:
                    bol=True
            if ip2!='':
                if (bol):
                    ip2Result = commands.getoutput('ls -R /video/*')
                else:
                    response2 = urllib2.urlopen('http://'+ip2+':8888/sql/getFileOutput')
                    ip2Result = response2.read()

            files1 = ip1Result.split('\n')
            for file in files1:
                if file.startswith('/'):
                    path = file[1 : len(file)-1]
                else:
                    if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                        if fileMap.has_key(file):
                            repeatMap.append('/' + path + '/' + file)
                        else:
                            fileMap[file] = '/' + path + '/' + file

            files2 = ip2Result.split('\n')
            for file in files2:
                if file.startswith('/'):
                    path = file[1 : len(file)-1]
                else:
                    if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                        if fileMap.has_key(file):
                            repeatMap.append('/' + path + '/' + file)
                        else:
                            fileMap[file] = '/' + path + '/' + file

            print '歌曲数量为'+str(len(fileMap))
            print '重复数量为'+str(len(repeatMap))


            result = {}
            result['歌曲数量'] = len(fileMap)
            result['重复数量'] = len(repeatMap)
#             result = checkDisk(fileMap)


            print '-'*20
            print (time.time()-tick)
            ret['code'] = 0
            ret['data'] = result
            self.send_json(ret)

        if op == 'getFileOutput':
            output = commands.getoutput('ls -R /video/*')
            self.send_string(output)

        elif op == 'parseImportTxt':
            isStopAdd[0]=False
            isAddData[0]=True
            media_data = "REPLACE INTO karaok.medias(media_no,media_name,media_namelen,media_langid,media_lang,media_tag1,media_tag2,media_actors,media_carria,media_yuan,media_ban,media_svrgroup,media_file,media_style,media_audio,media_volume,media_jp,media_py,media_strok,media_stroks,media_lyric,media_isnew,media_clickm,media_clickw,media_click,media_type,media_actno1,media_actno2,media_actno3,media_actno4,media_dafen,media_climax,media_climaxinfo,media_yinyi,media_light) VALUES({},'{}',{},{},'{}','{}','{}','{}','{}',{},{},{},'{}',{},'{}',{},'{}','{}',{},'{}','{}',{},{},{},{},{},{},{},{},{},{},{},'{}',{},{});"
            actor_data = "REPLACE INTO karaok.actors (actor_no,actor_name,actor_des,actor_type,actor_py,actor_jp,actor_click,actor_clickw,actor_clickm) VALUES({},'{}','{}','{}','{}','{}',{},{},{});"
            videotypes = ['流水影', 'MV', '演唱会']
            carriers = {'DVD': '2', 'MPEG1': '3', 'MPEG2':'4', 'SVCD':'5', 'MP3': '6', 'WAV': '7', 'LS':'8', 'LSS':'9', 'WAV':'10'}
            ret = {}
            ret['code'] = 1
            try:
                obj = {"title":"消息提示","content":"当前已开始解析库文件","state":1}
                executeSendMessage(obj)
                getDataBaseConnectionMusic()
                upload_path=os.path.join(os.path.dirname(__file__),'importTxt')
                if not os.path.isdir(upload_path):
                    os.makedirs(upload_path)
                fileN= self.get_argument('fileName', '')
                filepath=os.path.join(upload_path,fileN)
                result = []
                act_list = []
                media_fp = open('medias.data', 'w+')
                try:
                    fp = open(filepath)
                except Exception as ex:
                    print('failed to open  file')
                    return
                for line in fp:
                    line = line.strip()
                    arr = line.split('|')
                    if len(arr) < 20:
                        continue
                    if arr[0] == '广告':
                        media_type = '2'
                    elif arr[0] == '电影':
                        media_type = '3'
                    else:
                        media_type = '1'

                    media_name = arr[1]
                    media_lang = arr[2]
                    media_tags = arr[3]
                    media_tag1 = ''
                    media_tag2 = ''
                    tags = media_tags.split(',')
                    index = len(tags)
                    if index > 0:
                        media_tag1 = tags[0]
                    if index > 1:
                        media_tag2 = tags[1]

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
                    media_videotype = arr[9]
                    media_volume = arr[10]
                    media_audio = arr[11]
                    media_jp = arr[12]
                    media_namelen = str(len(media_jp))
                    media_langid = arr[13]
                    media_stroke = arr[14]
                    media_strokes = arr[15]
                    #media_heng = arr[15]
                    media_py = arr[19]
                    media_actnos = arr[21]
                    acts = media_actnos.split(';')
                    index = len(acts)
                    new_acts = self.parse_actors(media_actors, acts)
                    for ano in new_acts:
                        if ano not in act_list:
                            act_list.append(ano)
                            media_fp.write(actor_data.format(ano, new_acts[ano]['name'], new_acts[ano]['des'], new_acts[ano]['type'],new_acts[ano]['py'], new_acts[ano]['jp'], '0', '0', '0').decode('gbk').encode('utf-8'))

                    media_actno1 = '0'
                    media_actno2 = '0'
                    media_actno3 = '0'
                    media_actno4 = '0'
                    if index > 0:
                        media_actno1 = acts[0]
                    if index > 1:
                        media_actno2 = acts[1]
                    if index > 2:
                        media_actno3 = acts[2]
                    if index > 3:
                        media_actno4 = acts[3]

                    media_lyric = ''
                    media_isnew = '0'
                    media_click = '0'
                    media_clickm = '0'
                    media_clickw = '0'
                    media_dafen = '0'
                    media_climax = '0'
                    media_climaxinfo = ''
                    media_yinyi = '0'
                    media_light = '0'
                    media_svrgroup = '1'

                    media_fp.write(media_data.format \
                            (media_no, media_name, media_namelen, media_langid, media_lang,\
                            media_tag1, media_tag2, media_actors, media_carria, \
                            media_yuan, media_ban, media_svrgroup, media_file,\
                            media_videotype, media_audio, media_volume, \
                            media_jp, media_py,\
                            media_stroke, media_strokes, media_lyric, media_isnew, \
                            media_clickm, media_clickw, media_click, \
                            media_type, media_actno1, media_actno2, media_actno3, media_actno4, \
                            media_dafen, media_climax, media_climaxinfo, media_yinyi, media_light).decode('gbk').encode('utf-8'))
                    media_fp.write("\n")
                media_fp.close()
                commands.getoutput('mysql -u root -pThunder#123<medias.data')
                #--------------------------------finish parse---------------------------
                obj = {"title":"消息提示","content":"解析库文件完成,开始扫描磁盘","state":1}
                executeSendMessage(obj)
                outData = {}
                outData['mediatypeSize'] = 0
                outData['mediaTotal'] = 0
                outData['successCount'] = 0
                outData['notFindCount'] = 0
                outData['notFindMediaArrList'] = ''
                ret['data'] = outData

                print '*'*20
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                isStopAdd[0]=False
                isAddData[0]=False
                pass
            self.send_json(ret)


        elif op == 'cloud_batch_add':
            upload_path='/tmp'
            if not os.path.isdir(upload_path):
                os.makedirs(upload_path)
            fileN= self.get_argument('filename', '')
            ret = {}
            ret['code'] = 1
            tm = time.time()
            carrierList = selectCarrierList()
            audioList = selectAudioList()
            languageList = selectLanguageList()
            mediaArrList={}
            actorArrList={}
            mediaTypeArrList={}
            filepath=os.path.join(upload_path,fileN)
            result = []
            i = 0
            mediasNo = getMedia_sequenceNoPY(sp_createuniqueid(table='medias', columname='Media')-1)
            managerNo = getMedia_sequenceNoPY(sp_createuniqueid(table='mediasmanage', columname='MediaManage')-1)
            mediadetailNo = getMedia_sequenceNoPY(sp_createuniqueid( table='mediadetails', columname='MediaDetail')-1)
            mediafilesNo = getMedia_sequenceNoPY(sp_createuniqueid( table = 'mediafiles', columname='MediaFile')-1)
            mediasSequence = getMedia_sequenceNoPY(getSequence()-1)
            actorNo = getMedia_sequenceNoPY(sp_GetFirstAvailableID(table='actors', columname='Actor_ID')-1)
            actorSequence = getMedia_sequenceNoPY(addActorGetNo()-1)
            mediatypesNo = getMedia_sequenceNoPY(sp_createuniqueid(table='mediatypes', columname='MediaType')-1)
            marker = sp_getaddmediamark()
            for line in read_file(filepath):
                i+=1
                if i > 2:
                    if time.time()-tm>10:
                        print i
                        tm = time.time()
                    txtArr = line.split('|')
                    media = {}
                    media['iname']=txtArr[1].replace('\'',' ')
                    media['lname']=txtArr[2]
                    if txtArr[3].find(',')>0:
                        media['type1']=txtArr[3].split(',')[0]
                        media['type2']=txtArr[3].split(',')[1]
                        arrType = txtArr[3].split(',')
                        for tp in arrType:
                            mediaTp={}
                            mediaTp['curid']='0'
                            mediaTp['name']=tp
                            mediaTp['description']=tp
                            mediaTp['typeid']='1'
                            mediaTp['mediatypesNo']=mediatypesNo
                            mediaTypeArrList[mediaTp['name']]=mediaTp
                    else:
                        media['type1']=txtArr[3]
                        media['type2']=''
                        mediaTp={}
                        mediaTp['curid']='0'
                        mediaTp['name']=txtArr[3]
                        mediaTp['description']=txtArr[3]
                        mediaTp['typeid']='1'
                        mediaTp['mediatypesNo']=mediatypesNo
                        mediaTypeArrList[mediaTp['name']]=mediaTp
                    media['sname1'] = ''
                    media['sname2'] = ''
                    media['sname3'] = ''
                    media['sname4'] = ''
                    if txtArr[4].find(','):
                        starInfo = txtArr[4].split(',')
                        infoCount = len(starInfo)/4
                        if infoCount == 1:
                            media['sname1'] = starInfo[0].replace('\'',' ')
                            actor = {}
                            actor['actor_name'] = starInfo[0].replace('\'',' ')
                            actor['actor_typename'] = starInfo[1]
                            actor['actor_photo'] = ''
                            actor['actor_jianpin'] = starInfo[2]
                            actor['actor_pinyin'] = starInfo[3]
                            actor['actor_no'] = txtArr[21]
                            actor['actorNo']=actorNo
                            actor['actorSequence']=actorSequence
                            actorArrList[actor['actor_name']]=actor
                        else:
                            actorNoArr = txtArr[21].split(';')
                            for k in range(infoCount):
                                media['sname'+str(k+1)] = starInfo[k*4].replace('\'',' ')
                                actor = {}
                                actor['actor_name'] = starInfo[k*4].replace('\'',' ')
                                actor['actor_typename'] = starInfo[k*4+1]
                                actor['actor_photo'] = ''
                                actor['actor_jianpin'] = starInfo[k*4+2]
                                actor['actor_pinyin'] = starInfo[k*4+3]
                                actor['actor_no'] = actorNoArr[k]
                                actor['actorNo']=actorNo
                                actor['actorSequence']=actorSequence
                                actorArrList[actor['actor_name']]=actor
                    if carrierList.has_key(txtArr[5]):
                        media['videoformat'] = txtArr[5]
                        media['media_carrier_id']=carrierList[txtArr[5]]
                    else:
                        media['videoformat']='MPEG1'
                        media['media_carrier_id']=carrierList['MPEG1']
                    media['ztrack']=txtArr[6]
                    media['ytrack']=txtArr[7]
                    fileNo = txtArr[8]
                    media['serialno']=fileNo[:fileNo.find(".")]
                    media['filename']=fileNo
                    media['videotype']=txtArr[9]
                    media['volume']=txtArr[10]
                    if audioList.has_key(txtArr[11]):
                        media['audioformat']=txtArr[11]
                        media['media_audio_id']=audioList[txtArr[11]]
                    else:
                        media['audioformat']='MPEG'
                        media['media_audio_id']=audioList['MPEG']
                    media['jianpin']=txtArr[12]
                    media['ltype']=txtArr[13]
                    if languageList.has_key(media['lname']):
                        media['media_language_id'] = languageList[media['lname']]
                    else:
                        media['media_language_id'] = '8'
                    media['stroke']=txtArr[14]
                    media['bihua']=txtArr[15]
                    media['isnew']=txtArr[16]
                    media['pinyin']=txtArr[19]
                    media['type3']=''
                    media['typeid']='0'
                    media['groupid']='1'
                    media['fileserver_id']=''
                    media['isMenpai']='0'
                    media['lyric']=''
                    media['marker']=marker
                    media['mediasNo']=mediasNo
                    media['managerNo']=managerNo
                    media['mediadetailNo']=mediadetailNo
                    media['mediafilesNo']=mediafilesNo
                    media['mediasSequence']=mediasSequence
                    mediaArrList[media['filename']]=media
            for med in mediaArrList:
                print mediaArrList[med]['iname']
                sp_addmedias(**mediaArrList[med])
            for mTp in mediaTypeArrList:
                print mediaTypeArrList[mTp]['name']
                sp_addmediatype(**mediaTypeArrList[mTp])
            for acti in actorArrList:
                print actorArrList[acti]['actor_name']
                sp_AddActor(**actorArrList[acti])
            print '*'*20
            print (time.time()-tm)

        if op == 'get_disk_stat':
#             output = commands.getoutput('df -lh | grep /video')
            output = commands.getoutput('df -l')
            outputList = output.split('\n');
            otpList = []
            if(output!=""):
                for data in outputList:
                    data = ' '.join(data.split())
                    dataList = data.split(' ');
                    if dataList[0]!='Filesystem':
                        optDisc = {}
                        optDisc['dev'] = dataList[0]
                        optDisc['size'] = dataList[1]
                        optDisc['used'] = dataList[2]
                        optDisc['left'] = dataList[3]
                        optDisc['mp'] = dataList[5]
                        otpList.append(optDisc)
            self.send_json(otpList)

        if op == 'get_file_list':
            otpList = []
            output = commands.getoutput('ls -R /video/*')
            #print status, output
            files = output.split('\n');
            for file in files:
                if file.startswith('/'):
                    path = file[1 : len(file)-1]
                else:
                    if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                        otpList.append('/' + path + '/' + file)
            self.send_json(otpList)

        if op == 'get_file_listSize':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                otpList = []
                output = commands.getoutput('ls -R /video/*')
                files = output.split('\n');
                for file in files:
                    if file.startswith('/'):
                        path = file[1 : len(file)-1]
                    else:
                        if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                            otpList.append('/' + path + '/' + file)
                ret = {}
                ret['code'] = 0
                ret['data'] = len(otpList)
            self.send_json(ret)

        if op == 'getOtherFileList':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
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

                dataMap = getOtherFileListSerialNo()

                ry = []
                for fl in otpList:
                    if(not dataMap.has_key(fl["no"])):
                        ry.append(fl)
                    else:
                        del dataMap[fl["no"]]

                ret = {}
                ret['code'] = 0
                ret['data'] = ry
                ret['size'] = len(ry)
            self.send_json(ret)
        if op == 'getLostFileList':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                otpList = {}
                output = commands.getoutput('ls -R /video/*')
                files = output.split('\n');
                for file in files:
                    if file.startswith('/'):
                        path = file[1 : len(file)-1]
                    else:
                        if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                            otpList[file[:file.find(".")]]=1
                dataMap = getOtherFileListSerialNo()
                qs = []
                for no in dataMap:
                    if not otpList.has_key(no):
                        g={}
                        g['no']=no
                        g['name']=dataMap[no]
                        qs.append(g)
                ret = {}
                ret['code'] = 0
                ret['data'] = qs
                ret['size'] = len(qs)
            self.send_json(ret)

        if op == 'deleteAllData':
            isStopAdd[0]=True
            time.sleep(0.5)
            try:
                deleteAllData()
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            isAddData[0]=False
            self.send_json(ret)

        if op == 'onlyParseText':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                obj = {"title":"消息提示","content":"当前已开始解析库文件","state":1}
                executeSendMessage(obj)
                getDataBaseConnectionMusic()
                isStopAdd[0]=False
                isAddData[0]=True
                try:
                    upload_path=os.path.join(os.path.dirname(__file__),'importTxt')
                    if not os.path.isdir(upload_path):
                        os.makedirs(upload_path)
                    fileN= self.get_argument('fileName', '')

                    ret = {}
                    ret['code'] = 1
                    tm = time.time()
                    carrierList = selectCarrierList()
                    audioList = selectAudioList()
                    languageList = selectLanguageList()
                    mediaArrList={}
                    actorArrList={}
                    mediaTypeArrList={}
                    filepath=os.path.join(upload_path,fileN)
                    result = []
                    i = 0
                    mediasNo = getMedia_sequenceNoPY(sp_createuniqueid(table='medias', columname='Media')-1)
                    mediasSequence = getMedia_sequenceNoPY(getSequence()-1)
                    actorNo = getMedia_sequenceNoPY(sp_GetFirstAvailableID(table='actors', columname='Actor_ID')-1)
                    actorSequence = getMedia_sequenceNoPY(addActorGetNo()-1)
                    mediatypesNo = getMedia_sequenceNoPY(sp_createuniqueid(table='mediatypes', columname='MediaType')-1)
                    marker = sp_getaddmediamark()
                    for line in read_file(filepath):
                        i+=1
                        if i > 2:
                            if time.time()-tm>10:
                                print i
                                tm = time.time()
                            txtArr = line.split('|')
                            media = {}


                            media['iname']=txtArr[1].replace('\'',' ')
                            media['lname']=txtArr[2]
                            if txtArr[3].find(',')>0:
                                media['type1']=txtArr[3].split(',')[0]
                                media['type2']=txtArr[3].split(',')[1]
                                arrType = txtArr[3].split(',')
                                for tp in arrType:
                                    mediaTp={}
                                    mediaTp['curid']='0'
                                    mediaTp['name']=tp
                                    mediaTp['description']=tp
                                    mediaTp['typeid']='1'
                                    mediaTp['mediatypesNo']=mediatypesNo
                                    mediaTypeArrList[mediaTp['name']]=mediaTp
                            else:
                                media['type1']=txtArr[3]
                                media['type2']=''
                                mediaTp={}
                                mediaTp['curid']='0'
                                mediaTp['name']=txtArr[3]
                                mediaTp['description']=txtArr[3]
                                mediaTp['typeid']='1'
                                mediaTp['mediatypesNo']=mediatypesNo
                                mediaTypeArrList[mediaTp['name']]=mediaTp
                            media['sname1'] = ''
                            media['sname2'] = ''
                            media['sname3'] = ''
                            media['sname4'] = ''
                            if txtArr[4].find(','):
                                starInfo = txtArr[4].split(',')
                                infoCount = len(starInfo)/4
                                if infoCount == 1:
                                    media['sname1'] = starInfo[0].replace('\'',' ')
                                    actor = {}
                                    actor['actor_name'] = starInfo[0].replace('\'',' ')
                                    actor['actor_typename'] = starInfo[1]
                                    actor['actor_photo'] = ''
                                    actor['actor_jianpin'] = starInfo[2]
                                    actor['actor_pinyin'] = starInfo[3]
                                    actor['actor_no'] = txtArr[21]
                                    actor['actorNo']=actorNo
                                    actor['actorSequence']=actorSequence
                                    actorArrList[actor['actor_name']]=actor
                                else:
                                    actorNoArr = txtArr[21].split(';')
                                    for k in range(infoCount):
                                        media['sname'+str(k+1)] = starInfo[k*4].replace('\'',' ')
                                        actor = {}
                                        actor['actor_name'] = starInfo[k*4].replace('\'',' ')
                                        actor['actor_typename'] = starInfo[k*4+1]
                                        actor['actor_photo'] = ''
                                        actor['actor_jianpin'] = starInfo[k*4+2]
                                        actor['actor_pinyin'] = starInfo[k*4+3]
                                        actor['actor_no'] = actorNoArr[k]
                                        actor['actorNo']=actorNo
                                        actor['actorSequence']=actorSequence
                                        actorArrList[actor['actor_name']]=actor
                            if carrierList.has_key(txtArr[5]):
                                media['videoformat'] = txtArr[5]
                                media['media_carrier_id']=carrierList[txtArr[5]]
                            else:
                                media['videoformat']='MPEG1'
                                media['media_carrier_id']=carrierList['MPEG1']
                            media['ztrack']=txtArr[6]
                            media['ytrack']=txtArr[7]
                            fileNo = txtArr[8]
                            media['serialno']=fileNo[:fileNo.find(".")]
                            media['filename']=fileNo
                            media['videotype']=txtArr[9]
                            media['volume']=txtArr[10]
                            if audioList.has_key(txtArr[11]):
                                media['audioformat']=txtArr[11]
                                media['media_audio_id']=audioList[txtArr[11]]
                            else:
                                media['audioformat']='MPEG'
                                media['media_audio_id']=audioList['MPEG']
                            media['jianpin']=txtArr[12]
                            media['ltype']=txtArr[13]
                            if languageList.has_key(media['lname']):
                                media['media_language_id'] = languageList[media['lname']]
                            else:
                                media['media_language_id'] = '8'
                            media['stroke']=txtArr[14]
                            media['bihua']=txtArr[15]
                            media['isnew']=txtArr[16]
                            media['pinyin']=txtArr[19]
                            media['type3']=''
                            media['typeid']='0'
                            media['groupid']='1'
                            media['fileserver_id']=''
                            media['isMenpai']='0'
                            media['lyric']=''
                            media['marker']=marker
                            media['mediasNo']=mediasNo
                            media['mediasSequence']=mediasSequence
                            mediaArrList[media['filename']]=media
                    actorArrListHaveFile={}

                    addMediaSQL=[]

                    deleteAllAddMedias()


                    t1 = threading.Thread(target=parseFileDataToSQLData,args=(mediaArrList,actorArrList,mediaTypeArrList,actorArrListHaveFile))
                    t1.setDaemon(True)
                    t1.start()

                    outData = {}
                    outData['mediaTotal'] = len(mediaArrList)
                    ret['data'] = outData

                    print '*'*20
                    print (time.time()-tm)
                    ret['code'] = 0
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                    isStopAdd[0]=False
                    isAddData[0]=False
                    pass
            self.send_json(ret)


        if op == 'checkFiles':
            ip1= self.get_argument('ip1', '')
            ip2= self.get_argument('ip2', '')
            ipList=[]
            outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")
            ipList=outp.split('\n')
            ip1Result=''
            ip2Result=''
            bol = False
            for i in ipList:
                if i==ip1:
                    bol=True
            if (bol):
                ip1Result = commands.getoutput('ls -R /video/*')
            else:
                response1 = urllib2.urlopen('http://'+ip1+':8888/sql/getFileOutput')
                ip1Result = response1.read()

            bol = False
            for i in ipList:
                if i==ip2:
                    bol=True
            if (bol):
                ip2Result = commands.getoutput('ls -R /video/*')
            else:
                response2 = urllib2.urlopen('http://'+ip2+':8888/sql/getFileOutput')
                ip2Result = response2.read()


            mediaData = selectAllMediaDataForUpdateMedias()

            haveFileData = {}
            notDataMedia = {}
            notFileMedia = {}


            def scanvideosFN(file):
                no = file[0:file.find('.')]
                if mediaData.has_key(no):
                    haveFileData[no] = no
                else:
                    notDataMedia[no] = no

            for i in mediaData:
                if haveFileData.has_key(i) == False:
                    notFileMedia[i] = i

            deleteAllAddMedias()

            scanvideos(ip1Result,1,scanvideosFN)
            scanvideos(ip2Result,0,scanvideosFN)

            returnNotFindMedia=[]
            for i in notFileMedia:
                returnNotFindMedia.append(i)

            ret = {}
            ret['code'] = 0
            ret['data'] = {}
            ret['data']['haveFileDataCount']=len(haveFileData)
            ret['data']['notDataMediaCount']=len(notDataMedia)
            ret['data']['notFileMediaCount']=len(notFileMedia)
            ret['data']['notFileMedia']=returnNotFindMedia

            self.send_json(ret)


        if op == 'matchingDisk':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                ip1= self.get_argument('ip1', '')
                ip2= self.get_argument('ip2', '')
                ipList=[]
                outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")
                ipList=outp.split('\n')
                ip1Result=''
                ip2Result=''
                bol = False
                for i in ipList:
                    if i==ip1:
                        bol=True
                if (bol):
                    ip1Result = commands.getoutput('ls -R /video/*')
                else:
                    response1 = urllib2.urlopen('http://'+ip1+':8888/sql/getFileOutput')
                    ip1Result = response1.read()

                bol = False
                for i in ipList:
                    if i==ip2:
                        bol=True
                if (bol):
                    ip2Result = commands.getoutput('ls -R /video/*')
                else:
                    response2 = urllib2.urlopen('http://'+ip2+':8888/sql/getFileOutput')
                    ip2Result = response2.read()

                ip1ResultData = scanFilesFormOutput(ip1Result)
                ip2ResultData = scanFilesFormOutput(ip2Result)
                print 'ip1ResultData: %s' % ip1ResultData
                print 'ip2ResultData: %s' % ip2ResultData
                ip1ResultDataHave = {}
                ip2ResultDataHave = {}
                for i in ip1ResultData:
                    if ip2ResultData.has_key(i)==False:
                        ip1ResultDataHave[i]=ip1ResultData[i]
                for i in ip2ResultData:
                    if ip1ResultData.has_key(i)==False:
                        ip2ResultDataHave[i]=ip2ResultData[i]
                ret = {}
                ret['ip1']=ip1
                ret['ip1ResultDataHave']=ip1ResultDataHave
                ret['ip2']=ip2
                ret['ip2ResultDataHave']=ip2ResultDataHave

            self.send_json(ret)

        if op == 'scpFile':
            ip= self.get_argument('ip', '')
            filePath= self.get_argument('filePath', '')
            print 'ip:'+ip
            print 'filePath:'+filePath
            ret = {}
            ret['code'] = 0
            ret['data'] = scopyIp(ip,filePath)
            self.send_json(ret)

        if op == 'addmediaToFiles':
            no= self.get_argument('no', '')
            addmediaToFiles(no)
            updatepath()
            print 'updatepath'
            setUpdateDate()
            print 'setUpdateDate'
            createMediasSequence()
            print 'createMediasSequence'
            ret={}
            ret['code']=0
            self.send_json(ret)

        if op == 'getMediaFileCountFromIp':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                ip= self.get_argument('ip', '')
                ret = {}
                ret['code']=0
                ret['data']=getMediaFileCountFromIp(ip)
            self.send_json(ret)

        if op == 'getAddMediaFileFormScpOtherService':
            ret={}
            '''
            no= self.get_argument('no', '')
            ip= self.get_argument('ip', '')
            map = getAddMediaFileFormScpOtherService(no,ip)
            for i in map:
                scopyIp(i,map[i])
            '''
            ret['code']=0
            self.send_json(ret)

        if op == 'importLyricText':
            ret={}
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                otpList = scanLyricText()
                n = 0
                e = 0
                try:
                    for k in otpList:
                        if otpList.has_key(k):
                            tList = ""
                            try:
                                tList = read_file(otpList[k])
                            except:
                                continue
                            text = "\r\n".join(tList)
                            path,fname= os.path.split(otpList[k])
                            if path.endswith("Lyric")==True:
                                #判断歌词文件大小  （暂定 10K）
                                if len(text) < 10240:
                                    if saveLyricText(k,text) == True:
                                        n+=1
                                    else:
                                        e+=1
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                    pass
                ret['code']=0
                ret['data']=n
                ret['errordata']=e
            self.send_json(ret)

        if op == 'setUnRead':
            id= self.get_argument('id', '')
            ret={}
            ret['code']=1
            try:
                updateUnRead(id)
                ret['code']=0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'selectMessage':
            ret = {}
            ret['code']=1
            page = self.get_argument('page', '')
            count = self.get_argument('count', '')
            try:
                data = selectMessage(page,count)
                ret['code']=0
                ret['data']=data
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'selectAllDisk':
            ret = {}
            ret['code']=1
            try:
                resultText = commands.getoutput('ls /video')
                list = resultText.split('\n')
                ret['data']=list
                ret['code']=0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'getDiskListSize':
            if isAddData[0]==True:
                ret['msg']='当前库文件导入中,请稍后再试'
            else:
                diskName = self.get_argument('diskName', '')
                otpList = []
                output = commands.getoutput('ls -R /video/'+str(diskName))
                files = output.split('\n');
                for file in files:
                    if file.startswith('/'):
                        path = file[1 : len(file)-1]
                    else:
                        if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                            otpList.append('/' + path + '/' + file)
                ret = {}
                ret['code'] = 0
                ret['data'] = len(otpList)
            self.send_json(ret)

        if op == 'get_disk_statInfo':
            ret={}
            ret['code']=1
            output = commands.getoutput('df -lh | grep /video')
            outputList = output.split('\n');
            otpList = []
            if(output!=""):
                for data in outputList:
                        data = ' '.join(data.split())
                        if data != "":
                            dataList = data.split(' ');
                            optDisc = {}
                            optDisc['dev'] = dataList[0]
                            optDisc['size'] = dataList[1]
                            optDisc['used'] = dataList[2]
                            optDisc['left'] = dataList[3]
                            optDisc['mp'] = dataList[5]
                            otpList.append(optDisc)
                ret['code']=0
                ret['data']=otpList
            self.send_json(ret)
#         if op == 'openFile':
#             ret = {}
#             ret['code']=1
#             try:
#                 path = self.get_argument('path', '')
#                 resultText = commands.getoutput('ls /video/'+path)
#                 if resultText.find("ls:")==0:
#                     resultText=''
#                 list = resultText.split('\n')
#                 ret['data']=list
#                 ret['code']=0
#             except:
#                 logger.error(traceback.format_exc())
#                 print traceback.format_exc()
#                 ret['error']=traceback.format_exc()
#                 pass
#             self.send_json(ret)
        if op == 'openFile':
            ret = {}
            ret['code']=1
            try:
                path = self.get_argument('path', '')
                resultText = commands.getoutput('ls -lh /video/'+path)
                resultList = resultText.split("\n")
                res = []
                for line in resultList:
                    list = line.split()
                    if list[0]=="total" or list[len(list)-1]=="./" or list[len(list)-1]=="../":
                        continue
                    file = {}
                    if list[0][0] == "-":
                        file['type'] = "f"
                    if list[0][0] == "d":
                        file['type'] = "d"
                    file["size"] = list[4]
                    file["name"] = list[8]
                    res.append(file)
                ret['data'] = res
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'get_all_disk_info':
            data=get_all_disk_info()
            self.send_json(data)
        if op == 'format_disk':
            ret = {}
            ret['code'] = 1
            try:
                key = self.get_argument('key', '')
                json = format_disk(key)
                if json != None:
                    ret['data'] = json[key]
                    ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'selectConfigures55':
            ret = {}
            ret['code'] = 1
            try:
                ret['data'] = selectConfigures55()
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'setConfigures55':
            ret = {}
            ret['code'] = 1
            type = self.get_argument('type', '')
            try:
                setConfigures55(type)
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'deleteMediaUserSet':
            ret = {}
            ret['code'] = 1
            try:
                deleteMediaUserSet()
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'selectAdvertisementIdList':
            ret = {}
            ret['code'] = 1
            try:
                ret['data'] = selectAdvertisementIdList()
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)
        if op == 'selectAllAddMedia':
            ret = {}
            ret['code'] = 1
            try:
                ret['data'] = selectAllAddMedia()
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)
        if op=="executeSendMessage":
            ret = {}
            ret['code'] = 1
            try:
                title = self.get_argument('title', '')
                content = self.get_argument('content', '')
                state = self.get_argument('state', '')
                obj = {"title":title,"content":content,"state":state}
                ret['data'] = executeSendMessage(obj)
                ret['code'] = 0
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
                pass
            self.send_json(ret)

        if op == 'seachFile':
            ret = {}
            ret['code'] = 1
            path = self.get_argument('path', '')
            name = self.get_argument('name', '')
            resultText = commands.getoutput('find /video/'+path+' -name '+name+'*')
            resultList = resultText.split("\n")
            ret['data'] = resultList
            ret['code'] = 0
            self.send_json(ret)

        if op == 'deleteDiskFile':
            path = self.get_argument('path', '')
            ret={}
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                logger.error(traceback.format_exc())
                print traceback.format_exc()
                ret['error']=traceback.format_exc()
            ret['code']=0
            self.send_json(ret)

        if op == 'upfilepath':
            ret={}
            ip = self.get_argument('ip', '')
            if ip == "":
                ret['code']=1
            else:
                ipList=[]
                outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")
                ipList=outp.split('\n')
                ip1Result=''
                bol = False
                for i in ipList:
                    if i==ip:
                        bol=True
                if (bol):
                    ip1Result = commands.getoutput('ls -R /video/*')
                else:
                    try:
                        response1 = urllib2.urlopen('http://'+ip+':8888/sql/getFileOutput')
                        ip1Result = response1.read()
                    except:
                        ip1Result = ""
                if ip1Result == "":
                    ret['code']=1
                else:
                    files = ip1Result.split('\n');
                    path = ''
                    fileListDsic={}
                    for file in files:
                        if file.startswith('/'):
                            path = file[1 : len(file)-1]
                        else:
                            if file.lower().endswith('.txt')==False:
                                if file.lower().endswith('.ts')==True or file.lower().endswith('.mpg')==True:
                                    no = file[0:file.find('.')]
                                    if fileListDsic.has_key(no)==False:
                                        fileListDsic[no]='/' + path + '/' + file
                    ret['code']=0
                    ret['data']=fileListDsic
                    id = getFileServerIdFromIp(ip)
                    if id=="":
                        ret['code']=1
                    else:
                        upfilepath(fileListDsic,id)
            self.send_json(ret)
        if op=='deleteNullData':
            t = time.time()
            print '开始整理记录'
            ret={}
            outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")
            ipList=outp.split('\n')
            print 'ipList:'
            print ipList

            pathArr={}
            def scanvideosFN(no,path):
                if path not in pathArr:
#                     pathArr.append(path)
                    m1 = md5.new()
                    m1.update(path)
                    pathArr[m1.hexdigest()]=no

            def getListData(json1,json2):
                reList=[]
                for no in json1:
                    reList.append(no)
                for no in json2:
                    if not no in json1:
                        reList.append(no)
                return reList

            groupList=getFileServerAllGroup()
            print 'groupList:'
            print groupList
            deleteArrList=[]
            for groupId in groupList:
                ips = getFileServerAllIp(groupId)
                print 'ips:'
                print ips
                for ip in ips:
                    bol = False
                    for i in ipList:
                        if i==ip:
                            bol=True
                    if (bol):
                        ipResult = commands.getoutput('ls -R /video/*')
                    else:
                        response = urllib2.urlopen('http://'+ip+':8888/sql/getFileOutput')
                        ipResult = response.read()
                    scanvideosArr(ipResult,scanvideosFN)
                print 'selectAllDataForNullData'
                print len(pathArr)
                deleteArrList.append(selectAllDataForNullData(pathArr,groupId))
            if len(deleteArrList)==1:
                deleteArr = deleteArrList[0]
            elif len(deleteArrList)==2:
                deleteArr = getListData(deleteArrList[0],deleteArrList[1])
            print 'deleteArrLen:'
            print len(deleteArr)
            print '开始删除 deleteMediamanageactorForNullData'
            deleteMediamanageactorForNullData(deleteArr)
            print '开始删除 deleteMediamanagedirectorForNullData'
            deleteMediamanagedirectorForNullData(deleteArr)
            print '开始删除 deleteMediamanagetypeForNullData'
            deleteMediamanagetypeForNullData(deleteArr)
            print '开始删除 deleteMediafilesForNullData'
            deleteMediafilesForNullData(deleteArr)
            print '开始删除 deleteMediasmenuForNullData'
            deleteMediasmenuForNullData(deleteArr)
            print '开始删除 deleteMediasForNullData'
            deleteMediasForNullData(deleteArr)
            print '开始删除 deleteMediasmanageForNullData'
            deleteMediasmanageForNullData(deleteArr)
            print '开始删除 deleteMediadetailsForNullData'
            deleteMediadetailsForNullData(deleteArr)
            print '开始删除 deleteMeidasindexForNullData'
            deleteMeidasindexForNullData(deleteArr)
            print '开始删除 deleteMedianewsongForNullData'
            deleteMedianewsongForNullData(deleteArr)
            print '开始删除 deleteMediasorderForNullData'
            deleteMediasorderForNullData(deleteArr)
            print '开始修改 updateSystemsettinginfoForNullData'
            updateSystemsettinginfoForNullData()
            print '执行完成'
            print( time.time() - t )
            ret['code']=0
            ret['len']=len(deleteArr)
            self.send_json(ret)

        if op=='updateNullData':
            t = time.time()
            print '开始整理记录'
            ret={}
            outp=commands.getoutput("ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}' | grep -v 'fe80'")
            ipList=outp.split('\n')
            print 'ipList:'
            print ipList
            pathArr={}
            def scanvideosFN(no,path):
                if path not in pathArr:
#                     pathArr.append(path)
                    m1 = md5.new()
                    m1.update(path)
                    pathArr[m1.hexdigest()]=no

            def getListData(json1,json2):
                reList=[]
                for no in json1:
                    reList.append(no)
                for no in json2:
                    if not no in json1:
                        reList.append(no)
                return reList

            groupList=getFileServerAllGroup()
            print 'groupList:'
            print groupList
            deleteArrList=[]
            for groupId in groupList:
                ips = getFileServerAllIp(groupId)
                print 'ips:'
                print ips
                for ip in ips:
                    bol = False
                    for i in ipList:
                        if i==ip:
                            bol=True
                    if (bol):
                        ipResult = commands.getoutput('ls -R /video/*')
                    else:
                        response = urllib2.urlopen('http://'+ip+':8888/sql/getFileOutput')
                        ipResult = response.read()
                    scanvideosArr(ipResult,scanvideosFN)
                print 'selectAllDataForNullData'
                print len(pathArr)
                deleteArrList.append(selectAllDataForNullData(pathArr,groupId))
            if len(deleteArrList)==1:
                deleteArr = deleteArrList[0]
            elif len(deleteArrList)==2:
                deleteArr = getListData(deleteArrList[0],deleteArrList[1])
            print 'deleteArrLen:'
            print len(deleteArr)
            if len(deleteArr)>0:
                for i in deleteArr:
                    print i
            print '执行updateMediasForNullData'
            updateMediasForNullData(deleteArr)
            print 'SP_SetMediaIndex'
            sp_execute("call SP_SetMediaIndex()")
            print '执行完成'
            print( time.time() - t )
            ret['code']=0
            ret['len']=len(deleteArr)
            self.send_json(ret)




    @gen.coroutine
    def options(self, op):
        self.send_json('')

    @gen.coroutine
    def post(self, op):
        ret = {}
        ret['code'] = 1
        obj = {}
        if isAddData[0]==True:
            ret['msg']='当前库文件导入中,请稍后再试'
            self.send_json(ret)
        else:
            try:
                obj = json.loads(self.request.body)
            except:
                logger.error(traceback.format_exc())
                ret['error']=traceback.format_exc()
                pass
            if op == 'addMusic':
                '''
                obj['type3']=''
                obj['typeid']='0'
                if 'groupid' not in obj or obj['groupid']=='':
                    obj['groupid']='1'
                if 'group_id' not in obj or obj['group_id']=='':
                    obj['group_id']='1'
                obj['fileserver_id']=''
                obj['isMenpai']='0'
                lname = obj['lname']
                if lname=='国语':
                    obj['ltype']=0
                elif lname=='日语':
                    obj['ltype']=1
                elif lname=='韩语':
                    obj['ltype']=2
                else:
                    obj['ltype']=0
                mediasNo = getMedia_sequenceNoPY(sp_createuniqueid(table='medias', columname='Media')-1)
                managerNo = getMedia_sequenceNoPY(sp_createuniqueid(table='mediasmanage', columname='MediaManage')-1)
                mediadetailNo = getMedia_sequenceNoPY(sp_createuniqueid( table='mediadetails', columname='MediaDetail')-1)
                mediasSequence = getMedia_sequenceNoPY(getSequence()-1)
                mediafilesNo = getMedia_sequenceNoPY(sp_createuniqueid( table = 'mediafiles', columname='MediaFile')-1)
                marker = sp_getaddmediamark()

                obj['mediasNo']=mediasNo
                obj['managerNo']=managerNo
                obj['mediadetailNo']=mediadetailNo
                obj['mediafilesNo']=mediafilesNo
                obj['mediasSequence']=mediasSequence
                obj['marker']=marker

                if obj.has_key("isAdvertisement") and obj["isAdvertisement"] == "1":
                    obj['serialno'] = spm_getserialnoIsAdvertisement(**obj)
                else:
                    if not obj.has_key('serialno') or obj['serialno'] is None:
                        obj['serialno'] = spm_getserialno(**obj)
                '''
                try:
                    output = commands.getoutput('df | grep /video/')
                    '''
                    lines = output.split('\n');
                    left = 0
                    mp = ''
                    inx = 0
                    for line in lines:
                        inx = 0
                        items = line.split(' ')
                        for item in items:
                            if item!='':
                                inx = inx + 1
                                if inx==4 and item.isdigit() and int(left) < int(item):
                                    mp = items[len(items)-1]
                                    left = item
                    '''
                    if output == '':
                        ret['msg']="无挂载磁盘"
                        self.send_json(ret)
                        return
                    '''
                    noAndPathMap[str(obj['serialno'])] = mp
                    if obj:
                        sp_addmedias(**obj)
                    '''
                    ret['code'] = 0
                    conn = getDataBaseConnection()
                    cursor = conn.cursor()
                    sql = 'select max(media_no) from karaok.medias;'
                    n = cursor.execute(sql)
                    initNo = 0
                    for row in cursor.fetchall():
                        initNo = row[0]
                    if initNo < 9000000:
                        initNo = 9000000
                    else:
                        initNo += 1
                    ret['no'] = initNo
                    initNo += 1

                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                self.send_json(ret)

            elif op == 'deleteMusic':
                try:
                    sp_deletemedia(**obj)
                    ret['code'] = 0
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                    pass
                self.send_json(ret)

            elif op == 'addMusicType':
                try:
                    mediatypesNo = getMedia_sequenceNoPY(sp_createuniqueid(table='mediatypes', columname='MediaType'))
                    obj['mediatypesNo']=mediatypesNo
                    curid = sp_addmediatype(**obj)
                    ret['code'] = 0
                    ret['data'] = curid
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                self.send_json(ret)

            elif op == 'addActor':
                obj['actor_photo']=''
                obj['actorNo']=getMedia_sequenceNoPY(sp_GetFirstAvailableID(table='actors', columname='Actor_ID')-1)
                obj['actorSequence']=getMedia_sequenceNoPY(addActorGetNo()-1)
                if not obj.has_key('actor_no'):
                    obj['actor_no']=''
                try:
                    res = sp_AddActor(**obj)
                    if res is None:
                        ret['msg'] = '该歌星名已存在'
                    ret['code'] = 0
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                self.send_json(ret)


            elif op == 'notFindFileExport':
                text = self.request.body;
                textPath=os.path.join(os.path.dirname(__file__),'../static/text')
                if not os.path.isdir(textPath):
                    os.makedirs(textPath)
                filepath=os.path.join(textPath,'loseFile.txt')
                fl=open(filepath, 'w')
                fl.write(text)
                fl.close()
                ret['data'] = 'static/text/loseFile.txt'
                ret['code'] = 0
                self.send_json(ret)
            elif op == 'updateOrderCount':
                result = sp_updateordercount(**obj)
                if result:
                    ret['code'] = 0
                self.send_json(ret)
            elif op == 'uploadImportTxt':
                upload_path=os.path.join(os.path.dirname(__file__),'importTxt')
                if not os.path.isdir(upload_path):
                    os.makedirs(upload_path)
                fileN = self.get_argument('fileName', '')
                filepath=os.path.join(upload_path,fileN)
                file_metas=self.request.files['file']
                meta=file_metas[0]
                with open(filepath,'wb') as up:
                    up.write(meta['body'])
                up.close()
                ret['code'] = 0
                ret['path'] = filepath
                self.send_json(ret)

            elif op == 'login':
                ret = {}
                ret['code']=1
                try:
                    count = login(obj['username'],obj['password'])
                    ret['code']=0
                    ret['data']=count
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                self.send_json(ret)


parseFileDataToSQLDataState={}
def parseFileDataToSQLData(mediaArrListHaveFile,actorArrList,mediaTypeArrList,actorArrListHaveFile):
    obj = {"title":"消息提示","content":"开始导入","state":1}
    executeSendMessage(obj)
    parseFileDataToSQLDataState['state']=0
    actorTypeList = selectActorTypeList()

    allActorsData = selectAllActorsDataForUpdateMedias()

    allMediaData = selectAllMediaDataForUpdateMedias()
    allShadowData = selectAllShadowDataForUpdateMedias()

    allMediaType = selectMediaTypeForMap()

    deleteMediaData = selectAllDeleteMedia()

    songInfoOrder = {}
    uploadOrderPath=os.path.join(os.path.dirname(__file__),'songInfo')
    if not os.path.isdir(uploadOrderPath):
        os.makedirs(uploadOrderPath)
    filepath=os.path.join(uploadOrderPath,'AddSongInfo.dat')
    i = 0
    count=0
    sql=''
    for line in read_file(filepath):
        i+=1
        if i > 2:
            txt = line.split('|')
            textNo=txt[0]
            textNo=textNo[3:]
            order=txt[1]
            songInfoOrder[textNo.strip()] = order

    for mah in mediaArrListHaveFile:
        mahf = mediaArrListHaveFile[mah]
        if actorArrList.has_key(mahf['sname1']) and mahf['sname1']!="":
            actorArrListHaveFile[mahf['sname1']]=actorArrList[mahf['sname1']]
        if actorArrList.has_key(mahf['sname2']) and mahf['sname2']!="":
            actorArrListHaveFile[mahf['sname2']]=actorArrList[mahf['sname2']]
        if actorArrList.has_key(mahf['sname3']) and mahf['sname3']!="":
            actorArrListHaveFile[mahf['sname3']]=actorArrList[mahf['sname3']]
        if actorArrList.has_key(mahf['sname4']) and mahf['sname4']!="":
            actorArrListHaveFile[mahf['sname4']]=actorArrList[mahf['sname4']]
    for mTp in mediaTypeArrList:
        if not allMediaType.has_key(mediaTypeArrList[mTp]['name']):
            if mediaTypeArrList[mTp]['name']!="":
                sp_addmediatype(**mediaTypeArrList[mTp])
    for acti in actorArrListHaveFile:
        if isStopAdd[0]==True:
            break;
        act = actorArrListHaveFile[acti]
        print act['actor_name']
        if allActorsData.has_key(act['actor_name']):
            act['typeid']=actorTypeList[act['actor_typename']]
            sp_UpdateActor2(**act)
        else:
            sp_AddActor2(**act)

    shadow_list = []
    for med in mediaArrListHaveFile:
        if isStopAdd[0]==True:
            break;
        if mediaArrListHaveFile[med]['serialno'].strip().startswith("55"):
            shadow_list.append(med)
            #for shadow, just add it into cloud_musicshadow table, no any other table to deal with
            if allShadowData.has_key(mediaArrListHaveFile[med]['serialno'].strip()):
                print "updating Shadow : %s:%s" % (str(med), str(mediaArrListHaveFile[med]))
                UpdateShadow(**mediaArrListHaveFile[med])
            else:
                print "adding Shadow : %s:%s" % (str(med), str(mediaArrListHaveFile[med]))
                AddShadow(**mediaArrListHaveFile[med])
            continue

        if songInfoOrder.has_key(mediaArrListHaveFile[med]['serialno'].strip()):
            mediaArrListHaveFile[med]['orderCount']=songInfoOrder[mediaArrListHaveFile[med]['serialno']]
        else:
            mediaArrListHaveFile[med]['orderCount']=1
        if allMediaData.has_key(mediaArrListHaveFile[med]['serialno'].strip()):
            print 'update:'+mediaArrListHaveFile[med]['iname']
            mediaArrListHaveFile[med]['media_id']=allMediaData[mediaArrListHaveFile[med]['serialno'].strip()]
            mainUpdateMedias(**mediaArrListHaveFile[med])
        else:
            if deleteMediaData.has_key(mediaArrListHaveFile[med]['serialno']):
                id = deleteMediaData[mediaArrListHaveFile[med]['serialno']]
                def returnNo(id):
                    idL={}
                    idL[0]=id
                    def getreturn():
                        return idL[0]
                    return getreturn
                fn = returnNo(id)
                mediaArrListHaveFile[med]['mediasNo']=fn
                deleteDeleteMedia(id)
            print 'add:'+mediaArrListHaveFile[med]['iname']
            mainAddMedias(**mediaArrListHaveFile[med])

    print "Shadow list: %s" % str(shadow_list)
    for sh in shadow_list:
        #remove shadow musics, do not deal with them later
        mediaArrListHaveFile.pop(sh)

    if isStopAdd[0]==False:
        obj = {"title":"消息提示","content":"开始建立索引","state":1}
        executeSendMessage(obj)
        parseFileDataToSQLDataState['state']=1
        deleteAndInsertMediaManageActor()
        print 'deleteAndInsertMediaManageActor'
        parseFileDataToSQLDataState['state']=2
        executeSendMessage(obj)
        addMediaFilesForAddMedia()
        print 'addMediaFilesForAddMedia'
        parseFileDataToSQLDataState['state']=3
        startCreateManagerType()
        print 'startCreateManagerType'
        parseFileDataToSQLDataState['state']=4
        addIsNewSongForAddMedias()
        print 'addIsNewSongForAddMedias'
        parseFileDataToSQLDataState['state']=5
        deleteCloudRecordForAddMedias()
        print 'deleteCloudRecordForAddMedias'
        parseFileDataToSQLDataState['state']=6
        updatepath()
        print 'updatepath'
        parseFileDataToSQLDataState['state']=7
        setUpdateDate()
        print 'setUpdateDate'
        parseFileDataToSQLDataState['state']=8
        createMediasSequence()
        print 'createMediasSequence'
        parseFileDataToSQLDataState['state']=9
        sp_execute("call SP_SetMediaIndex()")
    #     logger.info("createMediasSequence")
        parseFileDataToSQLDataState['state']=10
        updateActorOrderCount()
        #complete shadow file path
        addShadowPath()
        isAddData[0]=False
        obj = {"title":"消息提示","content":"歌曲导入完成","state":1}
        executeSendMessage(obj)
        deleteAllAddMedias()
        try:
            os.system("cd /usr/local/coreseek/etc/ktv/; sh bin/task_media.sh")
        except:
            logger.error("缺失task_media.sh")
            pass



def addNotFindMediaThread(mediaArrList,mediaArrListHaveFile):
    notFindMediaArrList={}
    deleteNotFindMedia()
    for me in mediaArrList:
        mea=mediaArrList[me]
        if mediaArrListHaveFile.has_key(mea['serialno'])==False:
            mea['marker']=''
            mea['mediasNo']=''
            mea['mediasSequence']=''
            notFindMediaArrList[mea['serialno']]=mea

    cursorForNotFind = createConnForNotFind()
    sql = ''
    j=0
    result = []
    for i in notFindMediaArrList:
        media = notFindMediaArrList[i]
        print 'notFind'+media['iname']
        result.append([str(media['iname']),str(media['serialno']),str(media['sname1']),str(media['type1']),str(media['lname'])])
        j+=1
        if j>500:
            sql = 'INSERT INTO notfindmedia(notFindMedia_Name,notFindMedia_SerialNo,notFindMedia_Actor,notFindMedia_Type,notFindMedia_Language) \
    VALUES (%s,%s,%s,%s,%s)'
            addNotFindMedia(cursorForNotFind,sql,result)
            j=0
            del result[:]
    addNotFindMedia(cursorForNotFind,sql,result)
    closeConnForNotFind(cursorForNotFind)






















