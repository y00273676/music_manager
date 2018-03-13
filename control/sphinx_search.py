#!/usr/bin/env python
#-*- coding:utf-8 -*-

from lib import sphinxapi
from control.modbc import get_all_thunder_ini


class SearchCtrl(object):

    def __init__(self):
        self.host = get_all_thunder_ini()['mainserver']['DataBaseServerIp']
        if not isinstance(self.host,str):
            self.host= str(self.host)
        self.port = 9312
        self.cli = None

    @property
    def sphinx(self):
        if self.cli:
            return self.cli

        self.cli = sphinxapi.SphinxClient()
        self.cli.SetServer(self.host,int(self.port))
        self.cli.SetMaxQueryTime(100)
        self.cli.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)
        self.cli.SetRankingMode(sphinxapi.SPH_RANK_SPH04)
        return self.cli

    @property
    def clear_sphinx(self):
        self.cli=None



    def search_media(self,query,p,size):

        max_size=600
        if p > max_size/size:
            return dict(matches=[],time=0,total=0)
        tmp = self.sphinx.EscapeString(query.strip())
        #print tmp
        query = self.sphinx.EscapeString(query.strip())
        offset = (p-1)*size
        self.sphinx.SetLimits(offset,size,max_size)
        query ='"%s"'%(query+'*')
        try:
            result = self.sphinx.Query(query,'media')
            total = max_size if result['total']>max_size else result['total']
            return dict(matches=result['matches'],time=result['time'],total=total)
        except:
            return dict(mathces=[],time=0,total=0)
        finally:
            self.clear_sphinx
    
    def search_actor(self,query,p,size):

        max_size=600
        if p > max_size/size:
            return dict(matches=[],time=0,total=0)

        query = self.sphinx.EscapeString(query.strip())[0:20]
        offset = (p-1)*size
        self.sphinx.SetLimits(offset,size,max_size)
        query = query+'*'
        try:
            result = self.sphinx.Query(query,'actor')
            total = max_size if result['total']>max_size else result['total']
            return dict(matches=result['matches'],time=result['time'],total=total)
        except:
            return dict(mathces=[],time=0,total=0)
        finally:
            self.clear_sphinx

    def search_keyword(self,query,p,size):
        max_size=50
        if p > max_size/size:
            return dict(matches=[],time=0,total=0)

        query = self.sphinx.EscapeString(query.strip())[0:20]
        offset = (p-1)*size
        self.sphinx.SetLimits(offset,size,max_size)
        try:
            query ='"%s"'%(query+'*')
            result = self.sphinx.Query(query,'ma_keyword')
            total = max_size if result['total']>max_size else result['total']
            return dict(matches=result['matches'],time=result['time'],total=total)
        except:
            return dict(mathces=[],time=0,total=0)
        finally:
            self.clear_sphinx

    def buildExcerpts(self,msg,index,key):
        res =  self.sphinx.BuildExcerpts([msg],index,key,{'exact_phrase':True,'before_match':'<','after_match':'>','single_passage':True})
        res_info =res[0]
       # import re
       # ma = re.compile('<(.*)>')
       # ma_res =  ma.search(res_info)
       # if ma_res:
       #     print res_info
       #     res_info =ma.sub('<%s>'%ma_res.group(1).replace('<','').replace('>',''),res_info)
        return res_info
