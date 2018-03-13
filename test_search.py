#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from lib import sphinxapi

class SearchCtrl(object):

    def __init__(self, ctrl=None):
        self.ctrl = ctrl
        self.host = '127.0.0.1'
        self.port = 9312
        self.db_host = '127.0.0.1'
        self.db_port = 9302
        self.db_name = 'local'
        self.db_charset = 'utf8'
        self.cli        = None

    @property
    def sphinx(self):
        if self.cli:
            return self.cli
        self.cli = sphinxapi.SphinxClient()
        self.cli.SetServer(self.host, int(self.port))
        self.cli.SetMaxQueryTime(100)
        self.cli.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)
        self.cli.SetRankingMode(sphinxapi.SPH_RANK_SPH04)
        return self.cli

    @property
    def clear_sphinx(self):
        self.cli = None

    def test(self, kw, p=1, size=15, type=1):
        result = {}
        max_size = 100
        if p > max_size / size:
            return dict(matches=[],time=0,total=0)
        offset = (p - 1) * size
        self.sphinx.SetLimits(offset, size, max_size)
        #self.sphinx.SetFilter('music_wow', [1])
        #self.sphinx.SetFilter('type', [2])
        try:
            query = '%s' % kw
            result = self.sphinx.Query(query, 'media')
            #result = self.sphinx.Query(query, 'kcloud_musiclist_normal')
            #result = self.sphinx.Query(query, 'kcloud_musiclist_national')
            #result = self.sphinx.Query(query, 'kcloud_singerlist')
            #print ("result: %s" % result)
            return dict(matches=result['matches'],time=result['time'],total=result['total'])
        except Exception as ex:
            print 'error: %s' % ex
            return dict(matches=[],time=0,total=0)
        finally:
            self.clear_sphinx
if __name__ == '__main__':
    sc = SearchCtrl()
    res = sc.test('凉凉')
    for song in res['matches']:
        #print "%s" % song['attrs']
        print "%s;%s;%d" % (song['attrs']['music_no'],song['attrs']['music_caption'].decode('utf-8'),song['attrs']['music_wow'])
        #print "%s;%s;%d;%d" % (song['attrs']['singer_name'].decode('utf-8'),song['attrs']['singer_name2'].decode('utf-8'),song['attrs']['singer_dcount'],song['attrs']['singer_tvonline'])
    print("total: %d, time: %s" % (res['total'], res['time']))
    #print res
