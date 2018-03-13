#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月19日

@author: yeyinlin
'''

class Ktvmodule_theme(object):
    '''
    classdocs
    '''
    
#         public int theme_id { get; set; }
#         /// <summary>
#         /// 主题名
#         /// </summary>
#         public string theme_name { get; set; }
#         /// <summary>
#         /// 描述 
#         /// </summary>
#         public string theme_desc { get; set; }
#         /// <summary>
#         /// 目录
#         /// </summary>
#         public string theme_path { get; set; }
#         /// <summary>
#         /// --主题类型 0：自由主题  1、特定主题 
#         /// </summary>
#         public int theme_type { get; set; }
#         /// <summary>
#         /// 
#         /// </summary>
#         public string theme_date { get; set; }
#         /// <summary>
#         /// 过期时间
#         /// </summary>
#         public string theme_exptime { get; set; }
#         /// <summary>
#         /// 作者
#         /// </summary>
#         public string theme_author { get; set; }
#         /// <summary>
#         /// 状态
#         /// </summary>
#         public int theme_state { get; set; }
#         /// <summary>
#         ///  --主题包类型 1：横版 2 竖版
#         /// </summary>
#         public int theme_bagtype { get; set; }
#         /// <summary>
#         /// -主题解压后的目录
#         /// </summary>
#         public string theme_unpath { get; set; }
#         /// <summary>
#         /// 授权 0:所有用户 1:指定用户 2：指定地区
#         /// </summary>
#         public int theme_authorize { get; set; }

    def __init__(self):
        '''
        Constructor
        '''
        self.theme_id=None
        #/// 主题名
        self.theme_name=None
        #描述 
        self.theme_desc=None
        #目录
        self.theme_path=None
        #--主题类型 0：自由主题  1、特定主题 
        self.theme_type=None
        self.theme_date=None
        #过期时间
        self.theme_exptime=None
        #作者
        self.theme_author=None
        #状态
        self.theme_state=None
        #-主题包类型 1：横版 2 竖版
        self.theme_bagtype=None
        #-主题解压后的目录
        self.theme_unpath=None
        #授权 0:所有用户 1:指定用户 2：指定地区
        self.theme_authorize=None
        
class moduleerror():
    def __init__(self):
        self.moduleid=None
        self.exectime=None
        self.trytime=None
        self.canceltime=None
    
    
