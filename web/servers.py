#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import tornado
import json
import commands


from tornado import gen
from lib.http import request_json
from web.base import WebBaseHandler
from lib.types import try_to_int

from control.servers import get_all_servers,add_server,del_server,update_server,count_server,list_disk_all,list_dir
from control.serverinfo import get_server_info
from control.serverutils import stopService,restartService,lsService

logger=logging.getLogger(__name__)

serverjson = {}
serverjson['dbass'] = 'KTV数据服务'
serverjson['dhcp'] = 'DHCP服务'
serverjson['recog'] = '手写服务'
serverjson['record'] = '录音服务'
serverjson['broadcast'] = '广播服务'
serverjson['video'] = '视频服务'
serverjson['stbmodule'] = '模板同步服务'
serverjson['mainktv'] = '加密狗服务'
serverjson['twm'] = '数据管理服务'
serverjson['search'] = '搜索服务'
serverjson['transfer_vod'] = '微信点歌服务'
serverjson['wx_ngrok'] = '微信点歌连接'

class ServersHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, op):
        _res = dict(code=0, msg='ok', result=None)
        if op == 'list':
            ret = get_all_servers()
            logger.error("serverinfo: %s" % ret)
            if isinstance(ret, dict):
                _res['result'] = ret

            self.send_json(_res)
            return
        elif op == 'count':
            ret = get_all_servers()
            logger.error("serverinfo: %s" % ret)
            if isinstance(ret, dict):
                _res['result'] = ret['total']

            self.send_json(_res)
            return
        elif op == 'get':
            server_id = try_to_int(self.get_argument('server_id', '0'))
            res = get_server(server_id)
            _res['result'] = res
            self.send_json(_res)
            return
        elif op == 'ls':
            #获取服务器信息
            server_ip = self.get_argument('server_ip', '')
            print 'x' * 76
            #需要去调用获取服务的信息
            mjson={}
            mjson['server'] = lsService()
            #result = get_server_info(server_ip)
            result = None
            if result == 0:
                mjson['sbtinfo'] = result
            else:
                mjson['sbtinfo']={}
            _res = {}
            _res['msg'] = "获取成功"
            _res['code'] = 0
            _res['data'] = mjson
            self.send_json(_res)
            return
        elif op == 'filecount':
            ret = {}
            ret['code'] = 1
            ret['data'] = 0
            output = commands.getoutput('find /video -iname "*.ts" -o -iname "*.mpg" | wc -l')
            if output.isdigit():
                ret['code'] = 0
                ret['data'] = int(output)
            self.send_json(ret)
        elif op == 'listdisk':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            res = list_disk_all()
            if res:
                ret['code'] = 0
                ret['data'] = res
            self.send_json(ret)

        elif op == 'listdir':
            ret = {}
            ret['code'] = 1
            ret['data'] = None
            fpath = self.get_argument('path', '')
            if fpath:
                res = list_dir(fpath)
                ret['code'] = 0
                ret['data'] = res
            self.send_json(ret)
        else:
            raise tornado.web.HTTPError(405)
            #self.render('fangtaiset.html')

    @gen.coroutine
    def post(self, op):
        if op == 'update':
            '''
            '''
            sinfo = json.loads(self.request.body)
            _res = dict(code=0, msg='修改成功！', result=None)
            ret = update_server(sinfo)
            if ret:
                pass
            else:
                _res['code'] = 1
                _res['msg'] = "保存失败!"

            self.send_json(_res)
            return
        elif op == 'add':
            '''
            '''
            sinfo = json.loads(self.request.body)
            _res = dict(code=0, msg='保存成功！', result=None)
            ret = add_server(sinfo)
            if ret:
                pass
            else:
                _res['code'] = 1
                _res['msg'] = "保存失败!"
            self.send_json(_res)
            return
        elif op == 'del':
            _res = dict(code=0, msg='删除成功！', result=None)
            svrid = try_to_int(self.get_argument('server_id', '0'))
            ret = del_server(svrid)
            if ret:
                pass
            else:
                _res['code'] = 1
                _res['msg'] = "删除失败!"

            self.send_json(_res)
            return
        elif op == 'servicerestart':
            mjsondata = json.loads(self.request.body)
            _res = {}
            _res['msg']=''
            try:
                for sign in mjsondata:
                    if  restartService(sign) == 0:
                        if _res['msg']=='':
                            _res['msg'] = serverjson[sign] + "操作成功！"
                        else:
                            _res['msg'] = _res['msg'] + "\n" + serverjson[sign]+"操作成功！"
                    else:
                        
                        if _res['msg'] == '':
                            _res['msg'] = serverjson[sign] + "操作失败！"
                        else:
                            _res['msg'] = _res['msg'] + "\n" + serverjson[sign]+"操作失败！"
            except:
                _res['msg'] = "启动失败！"
            _res['code'] = 0
            
            self.send_json(_res)
            return
        elif op == 'servicestop':
            mjsondata = json.loads(self.request.body)
            #elif updatatype=="stopserver":
            _res = {}
            _res['msg']=''
            for sign in mjsondata:
                if sign=="twm":
                    continue
                if stopService(sign) == 0:
                    if _res['msg']=='':
                        _res['msg'] = serverjson[sign] + "停止服务成功！"
                    else:
                        _res['msg'] = _res['msg'] + "\n" + serverjson[sign] + "停止服务成功！"
                else:
                    
                    if _res['msg'] == '':
                        _res['msg'] = serverjson[sign] + "停止失败！"
                    else:
                        _res['msg'] = _res['msg'] + "\n" + serverjson[sign] + "停止失败！"
            _res['code'] = 0
            self.send_json(_res)
            return
        else:
            raise tornado.web.HTTPError(405)

