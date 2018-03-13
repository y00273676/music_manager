#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urllib import quote
from hashlib import md5
import logging

logger = logging.getLogger(__name__)

def generator_query_string_and_signature(parameters = {}, app_key = '', app_secret = ''):
    q_str = ''
    q_sign = ''
    if len(parameters)>0 :
        parameters = sorted(parameters.iteritems(), key=lambda parameter: parameter[0], reverse=False)
        q_sign = ''
        for p,v in parameters:
            q_sign += p + str(v)
            q_str += '{0}={1}'.format(p, quote(str(v)))
            q_str += '&'
        q_str = q_str[:-1]
        q_sign += app_secret
        m = md5()
        m.update(q_sign)
        q_sign = m.hexdigest()

    else:
        q_sign = ''
    return q_str, q_sign

def gen_sign_for_kcloud(parameters = {}, app_key = '', app_secret = ''):
    q_str = ''
    q_sign = ''
    if len(parameters)>0 :
        parameters = sorted(parameters.iteritems(), key=lambda parameter: parameter[0], reverse=False)
        q_sign = ''
        for p,v in parameters:
            q_str += '{0}={1}&'.format(p, quote(str(v)))
            q_sign += '{0}={1}&'.format(p, str(v))
        q_sign = q_sign[:-1]
        q_str = q_str[:-1]
        q_sign += app_secret
        m = md5()
        m.update(q_sign)
        q_sign = m.hexdigest()
    else:
        q_sign = ''
    return '%s&sign=%s' % (q_str, q_sign)

def check_parameter_signature(paras = {}):
    q_sign = p_sign = ''
    if len(paras)>0 :
        paras = sorted(paras.iteritems(), key=lambda parameter: parameter[0], reverse=False)
        for p,v in paras:
            if p == 'sign':
                p_sign = v[0]
            else:
                q_sign += '{0}:{1}||'.format(p, quote(str(v[0])))
        q_sign = q_sign[:-2]
        m = md5()
        m.update(q_sign)
        q_sign = m.hexdigest()
        return True
        return q_sign == p_sign
