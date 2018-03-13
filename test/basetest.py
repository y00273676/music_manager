#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import hashlib

import unittest 
from config import ONLINECFG, DEVCFG
#from lib.http import request_json
import time
import copy


import json
import logging
from urllib import urlencode

from pprint import pprint
from pprint import pformat

from tornado import httpclient
from tornado.httputil import url_concat
#from tornado.escape import json_encode

#appkey = '6f9c625e6b9c11e3bb1b94de806d865'
appkey = ''


logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='test.log',
        filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.WARN)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger('unittest')

TIMEOUT = 30
def request_json(url, params={}, timeout=TIMEOUT, method='GET'):
    res = None
    if method == 'POST':
        body = urlencode(params)
    else:
        url = url_concat(url, params)
        body = None

    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(url,
                                     method=method,
                                     request_timeout=timeout,
                                     body=body
                                     )
        logger.info(url)
    except httpclient.HTTPError as e:
        logger.error('%s\n%s\n', url, e)
    else:
        jstr = response.body
        try:
            res = json.loads(jstr)
            logger.debug(pformat(res))
        except ValueError as e:
            logger.debug(jstr)
            #C# code return non-standard json string
            res =  eval(jstr, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())
            if isinstance(res, dict):
                return res
            else:
                logger.error(e)
        return res
    finally:
        http_client.close()

class APITest(unittest.TestCase): 
    not_cmp_keys = ['msg','result', 'list', 'data']
    ##初始化工作 
    def setUp(self): 
        self.log = logger
        self.maxDiff = None
        pass

    #退出清理工作 
    def tearDown(self): 
        pass

    def _cmp_api_result_keyonly(self, d1, d2, msg = ''):
        ks1 = copy.deepcopy(d1.keys())
        ks2 = copy.deepcopy(d2.keys())
        ks1.sort()
        ks2.sort()
        self.assertListEqual(ks1, ks2, 'Got different result items' \
                '(%s) != (%s) \n%s' % (ks1, ks2, msg))

    def _assert_same_result(self, R1, R2, msg = '', ttl=0):
        self.assertTrue(type(R1) == type(R2))
        if isinstance(R1, dict):
            self._assert_same_dict(R1, R2, '', ttl - 1)
        elif isinstance(R1, list):
            self._assert_same_list(R1, R2, '', ttl - 1)
        else:
            pass

    def _assert_same_list(self, L1, L2, msg = '', ttl=0):
        '''to list has the same type elements
        this was have impoemented by self.assertEqual(),
        but for Thunder's API, the return result(json) is not so standard,
        to rewrite these methods to add some special judgements here.
        
        so just implement the 
        _assert_similar_<xxx>()
        _assert_same_<xxx>()
        to check the API result
        '''
        self.assertIsInstance(L1, list)
        self.assertIsInstance(L2, list)
        e1 = L1[0]
        e2 = L2[0]
        self.assertTrue(type(e1) == type(e2))
        if ttl >= 0:
            if isinstance(e1, dict):
                self._assert_same_dict(e1, e2, '', ttl - 1)
            elif isinstance(e1, list):
                self._assert_same_list(e1, e2, '', ttl - 1)
            elif isinstance(e1, tuple):
                self.assertTupleEqual(e1, e2)
            else:
                self.assertTrue(e1 == e2)
 
    def _assert_same_dict(self, d1, d2, msg='', ttl=0):
        ''' two dict has the same keys
        ttl: to control the deepth of compare, each level ttl -1,
              if ttl <= 0, then don't care the more detailed elements any more.
        '''
        self.assertIsInstance(d1, dict)
        self.assertIsInstance(d2, dict)
        k1 = copy.deepcopy(d1.keys())
        k2 = copy.deepcopy(d2.keys())
        k1.sort()
        k2.sort()
        self.assertListEqual(k1, k2)
        if ttl >= 0:
            for k in d1.keys():
                e1 = d1[k]
                e2 = d2[k]
                if isinstance(e1, dict):
                    self._assert_same_dict(e1, e2, '', ttl - 1)
                elif isinstance(e1, list):
                    self._assert_same_list(e1, e2, '', ttl - 1)
                elif isinstance(e1, tuple):
                    self.assertTupleEqual(e1, e2)
                else:
                    self.assertTrue(e1 == e2)
 

    def _assert_similar_result(self, R1, R2, msg = '', ttl=0):
        self.assertTrue(type(R1) == type(R2))
        if isinstance(R1, dict):
            self._assert_similar_dict(R1, R2, '', ttl - 1)
        elif isinstance(R1, list):
            self._assert_similar_list(R1, R2, '', ttl - 1)
        else:
            pass

    def _assert_similar_list(self, L1, L2, msg = '', ttl=0):
        '''to list has the same type elements
        '''
        self.assertIsInstance(L1, list)
        self.assertIsInstance(L2, list)
        e1 = L1[0]
        e2 = L2[0]
        self.assertTrue(type(e1) == type(e2))
        if ttl >= 0:
            if isinstance(e1, dict):
                self._assert_similar_dict(e1, e2, '', ttl - 1)
            elif isinstance(e1, list):
                self._assert_similar_list(e1, e2, '', ttl - 1)
            else:
                pass
 
    def _assert_similar_dict(self, d1, d2, msg='', ttl=0):
        ''' two dict has the same keys
        ttl: to control the deepth of compare, each level ttl -1,
              if ttl <= 0, then don't care the more detailed elements any more.
        '''
        self.assertIsInstance(d1, dict)
        self.assertIsInstance(d2, dict)
        k1 = copy.deepcopy(d1.keys())
        k2 = copy.deepcopy(d2.keys())
        k1.sort()
        k2.sort()
        self.assertListEqual(k1, k2)
        if ttl >= 0:
            for k in d1.keys():
                e1 = d1[k]
                e2 = d2[k]
                if isinstance(e1, dict):
                    self._assert_similar_dict(e1, e2, '', ttl - 1)
                elif isinstance(e1, list):
                    self._assert_similar_list(e1, e2, '', ttl - 1)
                else:
                    pass
 
    def _cmp_api_result(self, d1, d2, msg = ''):
        ks1 = d1.keys()
        ks2 = d2.keys()
        ks1.sort()
        ks2.sort()
        self.assertListEqual(ks1, ks2, 'Got different result items' \
                '(%s) != (%s) \n%s' % (ks1, ks2, msg))

        for k in ks1:
            if k == 'result':
                if isinstance(d1[k], dict):
                    rs1 = d1[k].keys()
                    rs2 = d2[k].keys()
                    rs1.sort()
                    rs2.sort()
                    self.assertListEqual(rs1, rs2, 'Result has different data structure')
                elif isinstance(d1[k], list):
                    pass
                else:
                    self.assertEqual(d1[k], d2[k])
            elif k in self.not_cmp_keys:
                #ignore the detaild data info
                continue
                self.assertEqual(d1[k], d2[k], 'Got different result data.' \
                        'key=(%s), total:(%s) != (%s) \n%s' % 
                        (k, d1[k]['total'], d2[k]['total'], msg))
            else:
                self.assertEqual(d1[k], d2[k], 'Got different result data.' \
                        'key=(%s), (%s) != (%s) \n%s' % (k, d1[k], d2[k], msg))

    def single_api(self, path, params, sign=None, method='GET', ver='DEV'):
        if sign:
            self.assertFalse('nosign' in params.keys())
            if 'time' in params.keys():
                params['time'] = "%d" % int(time.time())
            keys = params.keys()
            keys.sort()
            pstr = ''
            for k in sign:
                pstr = pstr + '%s=%s&' % (k, params[k])
            pstr = pstr.rstrip('&')
            pstr = pstr + appkey
            params['sign'] = hashlib.md5(pstr).hexdigest()
            logger.info('%s, sign=%s' % (pstr, params['sign']))
            pstr = pstr + '&sign=%s' % params['sign']

        if ver == 'REL':
            my_url = '%s/%s' % (ONLINECFG['url'], path)
        else:
            my_url = '%s/%s' % (DEVCFG['url'], path)
        res = request_json(my_url, params, 120, method)
        return res

    def cmp_api(self, path, params, sign=None, method='GET', check='key'):
        if isinstance(sign, list) and len(sign) > 0:
            self.assertFalse('nosign' in params.keys())
            if 'time' in params.keys():
                params['time'] = "%d" % int(time.time())
            keys = params.keys()
            #keys.sort()
            pstr = ''
            for k in sign:
                pstr = pstr + '%s=%s&' % (k, params[k])
            pstr = pstr.rstrip('&')
            pstr = pstr + appkey
            params['sign'] = hashlib.md5(pstr).hexdigest()
            logger.info('%s, sign=%s' % (pstr, params['sign']))
            pstr = pstr + '&sign=%s' % params['sign']

        rel_url = '%s/%s' % (ONLINECFG['url'], path)
        dev_url = '%s/%s' % (DEVCFG['url'], path)

        dev_json = request_json(dev_url, params, 120, method)
        rel_json = request_json(rel_url, params, 120, method)

        #self.assertIsInstance(rel_json, dict)
        #self.assertIsInstance(dev_json, dict)
        #self.assertDictEqual(rel_json, dev_json, 
        #       'Dev code got different result with the online deployment')
        if check == 'value':
            self._assert_same_result(rel_json, dev_json, '%s\n%s' % 
                    (url_concat(rel_url, params), url_concat(dev_url, params)), 100)
        elif check == 'key':
            self._assert_similar_result(rel_json, dev_json, '%s\n%s' % 
                (url_concat(rel_url, params), url_concat(dev_url, params)), 100)
        else:
            self.fail("not support check type:%s" % check)

