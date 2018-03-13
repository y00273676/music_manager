#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basetest import APITest

import unittest 
import hashlib
import time
import json

class KtvTest(APITest): 
    ##初始化工作 
    def setUp(self): 
        self.appkey = '6f9c625e6b9c11e3bb1b94de806d865'
        self.path = 'KtvService.aspx'
        pass

    #退出清理工作 
    def tearDown(self): 
        pass


    def test_ansyreleaseimages(self):
        return
        body = {'a':'A','b':'B','c':{'ca':'CA'}}
        params = {
            'op': 'ansyreleaseimages',
            }
        self.cmp_api(self.path, params, None, 'POST', 'key')
        pass


    def test_updatahost(self):
        return
        params = {
            'op': 'updatahost',
            'hostaddress': '127.0.0.1',
            #'hostaddress': 'http://k.kdaren.com',
            'dogname': '王晶云测试3',
            }
        self.cmp_api(self.path, params, None)
        pass

    def test_addktvinfo(self):
        self.fail('Not implement yet')
        pass

    def test_addstorefoodlog(self):
        return
        params = {
            'op': 'addstorefoodlog',
            'userid': '7f7bfc0a85e07f1e2b308c3eeb9ee89e',
            'storeid': 187,
            'roomip': '192.168.122.1',
            'foodname': '酒水1伊顺利',
            'fcount': 1,
            'foodtype': '',
            }
        self.cmp_api(self.path, params, None)
        pass

    def test_addjxsscbuy(self):
        return
        data = {
                'shopID': 187,
                'roomID': '192.168.122.1',
                'issue': '20160314',
                'gameCode': 130,
                'manner': 12,
                'chipinNumber': 0,
                'multipt': 1,
                'ticketCount': 1,
                'totalAmount': 1,
                'roomSerialNo': 'asdfasdfasdfasdfasdfasdfasdf',
                'result': '0000',
                'msg': '',
                'orderNo': 'what does this mean?',
                'payType': 'www',
                'payURL': 'www.bukengnikengshui.com',
                'status': 0,
                'origin': 1,
                'ticketSN': '',
                'money': 2,
                'channelid': '',
                'subChannelid': '',
                'version': '',
                'time': '',
                'errorMessage': '',
                }

        params = {
            'op': 'addjxsscbuy',
            'ktvid': 187,
            'data': json.dumps(data),
            'time': 0,
            }
        #self.single_api(self.path, params, ['ktvid','data','time'], 'POST', 'DEV')
        self.cmp_api(self.path, params, ['data', 'ktvid', 'op', 'time'])
        pass

    def test_addjxsscaccount(self):
        data = {
                'adminuser': 171,
                'ktvid': 187,
                'code': '000000',
                'enable': 1,
                'pwd': '123456',
                'verifyCode': 'abcdefg',
                'rebate': '0.1',
                'mark': '测试用',
                'lotteryArea': '{ "11" : "北京" }'
                }
        
        params = {
            'op': 'addjxsscaccount',
            'adminuser': 1,
            'data': json.dumps(data),
            'time': 0,
            }
        #self.single_api(self.path, params, ['ktvid','data','time'], 'POST', 'DEV')
        self.cmp_api(self.path, params, ['adminuser', 'data', 'op', 'time'])

    def test_jxsscnotice(self):
        self.fail('Not implement yet')
        pass

if __name__ =='__main__': 
  unittest.main()
