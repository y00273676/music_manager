#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basetest import APITest
import sys
sys.path.append('../')
from lib.defines import user_types

import unittest 
import hashlib
import random
import time

class thundersirTest(APITest): 
    mark = ''
    ##初始化工作 
    def setUp(self): 
        self.appkey = '6f9c625e6b9c11e3bb1b94de806d865'
        self.path = 'thundersir.aspx'
        self.mark = 'test authtication log by yishunli'
        self.dev_tukl = None
        self.rel_tukl = None
        pass

    #退出清理工作 
    def tearDown(self): 
        pass

    def test_alterktvauth(self):
        """编辑ktv使用的授权服务
        """
        return
        params = {
            'op': 'alterktvauth',
            'storeid': 187,
            'programid': 8,
            'type': 0,  # 1 for add, 0 for delete
            }
        self.cmp_api(self.path, params, None, 'GET', 'key')
        params['type'] = 1
        self.cmp_api(self.path, params, None, 'GET', 'key')

    def test_addktvauthtime(self):
        """添加ktv服务授权时间
        """
        #--------------addktvauthtime: normal case-----------------------
        params = {
            'op': 'addktvauthtime',
            'storeid': 187,
            'bdate': '2017-08-08 00:00:00',
            'edate': '2017-09-09 23:59:59',
            'aduser': 8,
            'isover': 0,
            'usemode': 2,
            'contract_state': 1,
            'validity': 1,
            'roomcount': 8,
            'department': 8,
            'sale': '',
            'price': 100,
            'paycycle': 8,
            'mark': self.mark,
            }
        dev_res1 = self.single_api(self.path, params, None, 'GET', 'DEV')
        rel_res1 = self.single_api(self.path, params, None, 'GET', 'REL')
        self._assert_similar_result(dev_res1, rel_res1, params['op'], 100)

        #--------------addktvauthtime: query the new data, used in later case-----------------------
        params = {
            'op': 'getktvauthtime',
            'storeid': 187,
            'dogname': '',
        }
        dev_res = self.single_api(self.path, params, None, 'GET', 'DEV')
        if dev_res1['code'] == 1:
            for au in dev_res['list']:
                if (au['mark'] == self.mark):
                    self.dev_tukl = au
        rel_res = self.single_api(self.path, params, None, 'GET', 'REL')
        if rel_res1['code'] == 1:
            for au in rel_res['list']:
                if (au['mark'] == self.mark):
                    self.rel_tukl = au
        self._assert_similar_result(self.dev_tukl, self.rel_tukl, params['op'], 100)
        #--------------updatektvauthtime: query the new data, used in later case-----------------------
        params = {
            'op': 'updatektvauthtime',
            'id': 0,
            'storeid': 187,
            'usemode': 2,
            'validity': 1,
            'roomcount': 90,
            'department': 8,
            'sale': '',
            'price': 100,
            'paycycle': 8,
            'mark': self.mark,
            }
        if self.dev_tukl:
            params['id'] = self.dev_tukl['Tuklid']
            dev_res = self.single_api(self.path, params, None, 'GET', 'DEV')
        if self.rel_tukl:
            params['id'] = self.rel_tukl['Tuklid']
            rel_res = self.single_api(self.path, params, None, 'GET', 'REL')
        #--------------updatektvauthtime: query again, to check the updates-----------------------
        params = {
            'op': 'getktvauthtime',
            'storeid': 187,
            'dogname': '',
        }
        dev_res = self.single_api(self.path, params, None, 'GET', 'DEV')
        if dev_res1['code'] == 1:
            for au in dev_res['list']:
                if (au['mark'] == self.mark):
                    self.dev_tukl = au
        rel_res = self.single_api(self.path, params, None, 'GET', 'REL')
        if rel_res1['code'] == 1:
            for au in rel_res['list']:
                if (au['mark'] == self.mark):
                    self.rel_tukl = au
        self._assert_similar_result(self.dev_tukl, self.rel_tukl, params['op'], 100)
        #we updated this data
        self.assertEqual(self.dev_tukl['roomcount'], 90)
        #--------------delktvauthtime: Try the delete method-----------------------
        params = {
            'op': 'delktvauthtime',
            'tuklid': 0,
            'storeid': 187,
            'adduser': 1,
            'mark': self.mark,
            }
        if self.dev_tukl:
            params['tuklid'] = self.dev_tukl['Tuklid']
            dev_res = self.single_api(self.path, params, None, 'GET', 'DEV')
        if self.rel_tukl:
            params['tuklid'] = self.rel_tukl['Tuklid']
            rel_res = self.single_api(self.path, params, None, 'GET', 'REL')
        if self.dev_tukl and self.rel_tukl:
            self._assert_similar_result(self.dev_tukl, self.rel_tukl, params['op'], 100)
 
    #def test_updatektvauthtime(self):
        """更新ktv服务授权时间
        """
        pass

    #def test_delktvauthtime(self):
        """删除ktv服务授权
        """
        pass
        #self.fail('Not implement yet')

    #def test_updatastore(self):
        """刷新ktv相关缓存
        """
        pass
        #self.fail('Not implement yet')

    #def test_addlog(self):
        """添加用户访问日志
        """
        #self.fail('Not implement yet')

if __name__ =='__main__': 
    unittest.main()

