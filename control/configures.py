#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-22 11:22:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from lib import http
from orm import orm as _mysql

def get_all_config_info():
    res = _mysql.configs.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None

def update_setconfig(id,mediordertype,ipaddress,orderdrinkset,skinname,ordercontrol,Isspecialeffect,config58,config59,config60):
    params = {}
    params['Configure_Set17'] = mediordertype  #点歌缺省方式

    params['Configure_Set51'] = ipaddress

    params['Configure_Set23'] = orderdrinkset  #密码设置
    params['Configure_Set52'] = skinname  #皮肤
    params['Configure_OrderControl'] = ordercontrol  #是否开台唱歌
    params['Configure_IsSpecialEffect'] = Isspecialeffect  #暂且认为 其他选项

    params['Configure_Set58'] = config58  #暂且认为 其他选项
    params['Configure_Set59'] = config59  #暂且认为 其他选项
    params['Configure_Set60'] = config60  #暂且认为 其他选项

    return _mysql.configures.update(id, params)
