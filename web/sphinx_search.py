#!/usr/bin/env python
#-*- coding:utf-8 -*-


import logging
from control import ctrl
from base import WebBaseHandler
import re
from lib import pinyin

logger = logging.getLogger(__name__)
'''
    if len(name) <= len(jp):
            py = jp[0:len(name)]
        else:
            py = pinyin.convert(name)
        py_res = ctrl.search.buildExcerpts(py,index,query)
        if py_res.find('<')>=0:
            ps_items = py_res.split('<')
            point= 0
            name_res=  ''
            for row,item in enumerate(ps_items):
                if (row+1) %2 ==0:
                    pe_items = item.split('>')
                    for prow,pitem in enumerate(pe_items):
                        if (prow+1)%2==1:
                            name_res = name_res+'%s>' % name[point:point+len(pitem)]
                        else:
                            name_res = name_res+'%s' % name[point:point+len(pitem)]
                        point+=len(pitem)
                else:
                    name_res = name_res+'%s<'%name[point:point+len(item)]
                    point+= len(item)
            return name_res.encode('utf-8')
        else:
            return name.encode('utf-8')
    else:

'''
def light(name,jp,index,query):
    if not name:
        return ''
    m = re.search('^[A-Z|a-z|0-9]*$',query)                    
    if m and m.group():
        if jp.find(query) != -1:
            return name,name
        return name,''
    else:
        res_name = ctrl.search.buildExcerpts(name,index,query)
        logger.info("xxx %s"%res_name)
        m = re.match('.*<(.*)>.*',res_name)
        if m:
            logger.info(m.group(1))
            return res_name.replace('<','').replace('>',''),m.group(1).replace('<','').replace('>','')
        return res_name.replace('<','').replace('>',''),''


class MediaHandler(WebBaseHandler):

    def get(self):
        result,code,msg=dict(),'200','OK'
        query = self.get_argument('query','')
        p = int(self.get_argument('p','1'))
        size = int(self.get_argument('size','50'))
        if query:
            result = ctrl.search.search_media(query,p,size)
            m_matches =[match['attrs'] for match in result['matches']]
            result['matches'] = []
            if m_matches:
                for match in m_matches:
                    logger.info("aaa %s"%match['name'])
                    match['name'],match['key'] = light(match['name'],match['jp'],'media',query)
                    match['keytype']=0
                    if  not match['key'] and match['sname1']:
                        match['sname1'],match['key']= light(match['sname1'],match['sjp1'],'media',query)
                        if  not match['key'] and match['sname2']:
                            match['sname2'],match['key'] = light(match['sname2'],match['sjp2'],'media',query)
                        if  not match['key'] and match['sname3']:
                            match['sname3'],match['key']= light(match['sname3'],match['sjp3'],'media',query)
                        if  not match['key'] and match['sname4']:
                            match['sname4'],match['key']= light(match['sname4'],match['sjp4'],'media',query)
                        if match['key']:
                            match['keytype']=1
                    if  not match['key']:
                        if match['lyric']:
                            for line in match['lyric'].split('\r\n'):
                                temp = ctrl.search.buildExcerpts(line,'media',query)
                                if '<' in temp:
                                    print temp
                                    match['keytype']=2
                                    match['lyric'] = temp
                                    break
                    else:
                        l_len = len(match['lyric'])
                        match['lyric'] = match['lyric'].split('\r\n')[0]

                    result['matches'].append(match)
        self.send_json(dict(result=result,code=code,msg=msg))

class ActorHandler(WebBaseHandler):

    def get(self):
        result,code,msg=dict(),'200','OK'
        query = self.get_argument('query','')
        p = int(self.get_argument('p','1'))
        size = int(self.get_argument('size','10'))
        if query:
            result = ctrl.search.search_actor(query,p,size)
            matches =[match['attrs'] for match in result['matches']]
            result['matches'] = []
            if matches:
                for match in matches:
                    match['name'] = light(match['name'],match['jp'],'actor',query)
                    result['matches'].append(match)
            
            
        self.send_json(dict(result=result,code=code,msg=msg))

class KeywordHandler(WebBaseHandler):

    def get(self):
        result,code,msg=dict(),'200','OK'
        query = self.get_argument('query','')
        p = int(self.get_argument('p','1'))
        size = int(self.get_argument('size','10'))
        if query:
            result = ctrl.search.search_keyword(query,p,size)
            result['matches']=[match['attrs'] for match in result['matches']]
            
        self.send_json(dict(result=result,code=code,msg=msg))
