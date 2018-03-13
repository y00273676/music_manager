#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from urllib import urlencode
from functools import partial

from tornado import gen
from tornado import httpclient
from tornado.httputil import url_concat
from tornado.escape import json_encode

logger = logging.getLogger(__name__)

TIMEOUT = 10

def make_url(base, params={}):
    str_params = dict((k, unicode(v).encode('utf8')) for k, v in params.iteritems())
    url = url_concat(base, str_params)
    return url

def request_http(url, params={}, timeout=TIMEOUT, method='POST'):
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
    except httpclient.HTTPError as e:
        logger.error('%s\n%s\n', url, e)
        return ''
    else:
        res = response.body
        return res
    finally:
        http_client.close()

def request_json(url, params={}, timeout=TIMEOUT, method='POST'):
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
                                     body=body,
                                     validate_cert=False
                                     )
    except httpclient.HTTPError as e:
        logger.error('%s\n%s\n', url, e)
    else:
        #logger.info('http request: [%s]: %s' % (url, response.body))
        try:
            res = json.loads(response.body)
            return res
        except ValueError as e:
            jstr = response.body
            #logger.debug(jstr)
            #C# code return non-standard json string
            res =  eval(jstr, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())
            if isinstance(res, dict):
                return res
            else:
                logger.error(e)
    finally:
        http_client.close()

def sync_request(api_uri, params={}):
    '''
    params is a dict of remote method's arguments
    example:
        sync_request('activity', {'ActivityName:'每日登录送积分''})
    '''
    url = make_url(api_uri, params)
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(url,
                                     method='GET',
                                     request_timeout=TIMEOUT
                                     )
    except httpclient.HTTPError as e:
        logger.error('%s\n%s\n', url, str(e))
    else:
        res = json.loads(response.body)
        if res['error'] == 'E_OK':
            return res['result']
        else:
            logger.error('%s\n%s\n', url, res['msg'])
    finally:
        http_client.close()


def handle_json_request(response, callback=None, exc_message=None):
    url = response.request.url
    if response.error:
        logger.error('Backend network error:%s\n%s\n', url, response.error)
        response.rethrow()
    else:
        if response.body:
            res = json.loads(response.body)
        else:
            res = {'response' : response.body}
        if callback:
            callback(res)
        else:
            logger.error('Backend return error:%s\n%s\n', url, res.get('msg'))


def _async_json_request(api_uri,
                       method='POST',
                       params={},
                       headers = None,
                       callback=None,
                       exc_message=None):
    '''
    params is a dict of url params
    example:
        yield async_json_request('/activity', {'ActivityName:'每日登录送积分''})
    '''
    if method == 'POST':
        body = json_encode(params)
        url = api_uri
    else:
        body = None
        url = make_url(api_uri, params)
    headers = headers if headers else { 'Content-Type':'application/json'}
    http_client = httpclient.AsyncHTTPClient()
    handle_req = partial(handle_json_request, callback=callback, exc_message=exc_message)
    return http_client.fetch(url,
                             method=method,
                             connect_timeout=5,
                             request_timeout=5,
                             body=body,
                             callback=handle_req,
                             headers=headers)

async_json_request = partial(gen.Task, _async_json_request)

