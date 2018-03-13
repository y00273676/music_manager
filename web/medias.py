#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import setting
import logging
import tornado
import traceback
import shutil
import os
import json
from tornado import gen
#from mqtt import dmsapi
#from control import api as _apictl
from lib.types import try_to_int
from web.base import WebBaseHandler
from control.medias import get_all_medias,get_media_count,get_by_lang,get_by_tag,update_media,\
        export_medias, get_lost_files,get_useless_files
from sql import parseFileDataToSQLDataState

logger = logging.getLogger(__name__)
        
class medias(WebBaseHandler):
    @gen.coroutine
    def get(self,op):
        if op == 'list':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            result['data'] = None
            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))
     
            #get date from controller:
            res = get_all_medias(page, psize)
            if isinstance(res, dict):
                result['data'] = res
            self.send_json(result)
            
        elif op == 'count':
            result = {}
            result['code'] = 1
            result['msg'] = ''
            text = self.get_argument('text', '')
            res = get_media_count(text)
            result['data']=res
            result['state']=parseFileDataToSQLDataState
            self.send_json(result)

        elif op == 'bylang':
            result = dict(code=0, msg='ok', result=None)

            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))
            lname = self.get_argument('lang', '')

            result['result']= get_by_lang(lname, page, psize)
            self.send_json(result)
        elif op == 'bytag':
            result = dict(code=0, msg='ok', result=None)

            #get arguments
            page = try_to_int(self.get_argument('page', '0'))
            psize = try_to_int(self.get_argument('psize', '15'))
            tag = self.get_argument('type', '')

            result['result']= get_by_tag(tag, page, psize)
            self.send_json(result)
        elif op == 'export':
            result = dict(code=0, msg='ok', result=None)
            textPath = os.path.join(os.path.dirname(__file__),'../static/text')
            if not os.path.isdir(textPath):
                os.makedirs(textPath)
            fpath = os.path.join(textPath,'export.txt')
            if os.path.exists(fpath):
                os.remove(fpath)
            scope = self.get_argument('scope', 'all')
            if scope == 'all':
                ret = export_medias(fpath)
            else:
                ret = export_medias(fpath, True)
            if ret:
                result['code'] = 0
                result['msg'] = '导出成功'
                result['data'] = 'static/text/export.txt'
            else:
                result['code'] = 1
                result['msg'] = '导出失败'
                result['data'] = 'static/text/export.txt'
                if os.path.exists(fpath):
                    os.remove(fpath)
            self.send_json(result)
            return
        elif op == 'lostfiles':
            result = {}
            result['code'] = 1
            result['data'] = None
            res = get_lost_files()
            if res:
                result['code'] = 0
                result['data'] = res

        elif op == 'uselessfiles':
            result = {}
            result['code'] = 1
            result['data'] = None
            res = get_useless_files()
            if res:
                result['code'] = 0
                result['data'] = res
        else:
            raise tornado.web.HTTPError(405)

    @gen.coroutine
    def post(self,op):
        if op == 'click':
            result = dict(code=0, msg='ok', result=None)

            try:
                #get arguments
                info = json.loads(self.request.body)
            except Exception as ex:
                result['code'] = 1
                result['msg'] = '参数错误'
                self.send_json(result)
                return

            #get date from controller:
            ret = update_media(info)
            if ret:
                result['msg'] = '更新成功'
            else:
                result['code'] = 1
                result['msg'] = '更新失败'
            self.send_json(result)
 
        raise tornado.web.HTTPError(405)

    def export_data(self, op):
        return ret
        '''
        if op == 'all':
            text = '雷石KTV41.6'
            text += '\r\n\r\n'
            if op == 'all':
                try:
                    deleteFromMediafilesview()
                    insertIntoMediafilesview()
                    exportdataAll = sp_getexportdataAll()
                    for m_exportdata in exportdataAll:
                        m_exportdata['isAllData']=1
                        actorList = sp_getacotr(**m_exportdata)
                        mediaType = sp_getmediatype(**m_exportdata)
                        isNewSong = sp_isnewsong(**m_exportdata)
                        text+=str('歌曲')
                        text+='|'
                        if m_exportdata.has_key('Media_Name'):
                            text+=str(m_exportdata['Media_Name'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Language_Name'):
                            text+=str(m_exportdata['Language_Name'])
                        else:
                            text+=''
                        text+='|'
                        for i in range(len(mediaType)):
                            text+=str(mediaType[i]['MediaType_Name'])
                            if i<len(mediaType)-1:
                                text+=','
                        text+='|'
                        for i in range(len(actorList)):
                            text+=str(actorList[i]['Actor_Name'])+','
                            text+=str(actorList[i]['ActorType_Name'])+','
                            text+=str(actorList[i]['Actor_HeaderSoundSequence'])+','
                            text+=str(actorList[i]['Actor_AllSoundSequence'])
                            if i<len(actorList)-1:
                                text+=','
                        text+='|'
                        if m_exportdata.has_key('Carrier_Name'):
                            text+=str(m_exportdata['Carrier_Name'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('MediaManage_OriginalTrack'):
                            text+=str(m_exportdata['MediaManage_OriginalTrack'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('MediaManage_AccompanyTrack'):
                            text+=str(m_exportdata['MediaManage_AccompanyTrack'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_SerialNo'):
                            text+=str(m_exportdata['Media_SerialNo'])+".mpg"
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_IsReserved3'):
                            text+=str(m_exportdata['Media_IsReserved3'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_IsReserved2'):
                            text+=str(m_exportdata['Media_IsReserved2'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Audio_Name'):
                            text+=str(m_exportdata['Audio_Name'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_HeaderSoundSequence'):
                            text+=str(m_exportdata['Media_HeaderSoundSequence'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_IsReserved5'):
                            text+=str(m_exportdata['Media_IsReserved5'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_StrokeNum'):
                            text+=str(m_exportdata['Media_StrokeNum'])
                        else:
                            text+=''
                        text+='|'
                        if m_exportdata.has_key('Media_HeadStroke'):
                            text+=str(m_exportdata['Media_HeadStroke'])
                        else:
                            text+=''
                        text+='|'
                        text+=str(isNewSong)
                        text+='|'
                        text+='0'
                        text+='|'
                        text+='0'
                        text+='|'
                        if m_exportdata.has_key('Media_AllSoundSequence'):
                            text+=str(m_exportdata['Media_AllSoundSequence'])
                        else:
                            text+=''
                        text+='|'
                        text+='0'
                        text+='|'
                        for i in range(len(actorList)):
                            text+=str(actorList[i]['Actor_No'])
                            if i<len(actorList)-1:
                                text+=';'

                        text+='\r\n'
                except:
                    logger.error(traceback.format_exc())
                    print traceback.format_exc()
                    ret['error']=traceback.format_exc()
                    pass
            else:
                for no in obj:
                    media={}
                    media['Media_SerialNo']=no
                    res = sp_getexportdata(**media)
                    m_exportdata = res[0]
                    actorList = sp_getacotr(**m_exportdata)
                    mediaType = sp_getmediatype(**m_exportdata)
                    isNewSong = sp_isnewsong(**m_exportdata)
                    text+=str('歌曲')
                    text+='|'
                    if m_exportdata.has_key('Media_Name'):
                        text+=str(m_exportdata['Media_Name'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Language_Name'):
                        text+=str(m_exportdata['Language_Name'])
                    else:
                        text+=''
                    text+='|'
                    for i in range(len(mediaType)):
                        text+=str(mediaType[i]['MediaType_Name'])
                        if i<len(mediaType)-1:
                            text+=','
                    text+='|'
                    for i in range(len(actorList)):
                        text+=str(actorList[i]['Actor_Name'])+','
                        text+=str(actorList[i]['ActorType_Name'])+','
                        text+=str(actorList[i]['Actor_HeaderSoundSequence'])+','
                        text+=str(actorList[i]['Actor_AllSoundSequence'])
                        if i<len(actorList)-1:
                            text+=','
                    text+='|'
                    if m_exportdata.has_key('Carrier_Name'):
                        text+=str(m_exportdata['Carrier_Name'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('MediaManage_OriginalTrack'):
                        text+=str(m_exportdata['MediaManage_OriginalTrack'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('MediaManage_AccompanyTrack'):
                        text+=str(m_exportdata['MediaManage_AccompanyTrack'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_SerialNo'):
                        text+=str(m_exportdata['Media_SerialNo'])+".mpg"
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_IsReserved3'):
                        text+=str(m_exportdata['Media_IsReserved3'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_IsReserved2'):
                        text+=str(m_exportdata['Media_IsReserved2'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Audio_Name'):
                        text+=str(m_exportdata['Audio_Name'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_HeaderSoundSequence'):
                        text+=str(m_exportdata['Media_HeaderSoundSequence'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_IsReserved5'):
                        text+=str(m_exportdata['Media_IsReserved5'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_StrokeNum'):
                        text+=str(m_exportdata['Media_StrokeNum'])
                    else:
                        text+=''
                    text+='|'
                    if m_exportdata.has_key('Media_HeadStroke'):
                        text+=str(m_exportdata['Media_HeadStroke'])
                    else:
                        text+=''
                    text+='|'
                    text+=str(isNewSong)
                    text+='|'
                    text+='0'
                    text+='|'
                    text+='0'
                    text+='|'
                    if m_exportdata.has_key('Media_AllSoundSequence'):
                        text+=str(m_exportdata['Media_AllSoundSequence'])
                    else:
                        text+=''
                    text+='|'
                    text+='0'
                    text+='|'
                    for i in range(len(actorList)):
                        text+=str(actorList[i]['Actor_No'])
                        if i<len(actorList)-1:
                            text+=';'

                    text+='\r\n'
            textPath=os.path.join(os.path.dirname(__file__),'../static/text')
            if not os.path.isdir(textPath):
                os.makedirs(textPath)
            filepath=os.path.join(textPath,'export.txt')
            fl=open(filepath, 'w')
            fl.write(text)
            fl.close()
            ret['data'] = 'static/text/export.txt'
            self.send_json(ret)
        '''
        pass


