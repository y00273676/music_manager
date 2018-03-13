#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import traceback
import commands

from orm.mm import getMedia_sequenceNoPY, sp_createuniqueid, getSequence, \
        sp_getaddmediamark, spm_getserialnoIsAdvertisement, sp_addmedias, \
        insertMeidaFilesForAddMedia

logger = logging.getLogger(__name__)

def add_music(obj):
    '''
    从web/sql.py中提出来的代码，防止调用WebAPI接口的嵌套调用（直接调用函数）
    '''
    ret = dict(code = 1, msg='ok', result=None)
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
    
    obj['mediasNo'] = mediasNo
    obj['managerNo'] = managerNo
    obj['mediadetailNo'] = mediadetailNo
    obj['mediafilesNo'] = mediafilesNo
    obj['mediasSequence'] = mediasSequence
    obj['marker'] = marker
    
    if obj.has_key("isAdvertisement") and obj["isAdvertisement"] == "1":
        obj['serialno'] = spm_getserialnoIsAdvertisement(**obj)
    else:
        if not obj.has_key('serialno') or obj['serialno'] is None:
            obj['serialno'] = spm_getserialno(**obj)
    try:
        output = commands.getoutput('df -l | grep /video/')
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
        
        if(mp==''):
            ret['msg']="无挂载磁盘"
            return ret
        
        #noAndPathMap[str(obj['serialno'])] = mp
        if obj:
            sp_addmedias(**obj)
        insertMeidaFilesForAddMedia(obj['serialno'], obj['filename'])
        ret['code'] = 0
        ret['no'] = obj['serialno']
        
    except:
        logger.error(traceback.format_exc())
        print traceback.format_exc()
        ret['error']=traceback.format_exc()
    return ret
