#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月27日

@author: yeyinlin
'''
from modules.model.common import Serializable

# 
#        public int paper_id { get; set; }
#         public string paper_name { get; set; }
#         public string paper_url { get; set; }
#         /// <summary>
#         /// 1横板,2竖版
#         /// </summary>
#         public int paper_bagtype { get; set; }
#         public DateTime paper_time { get; set; }
#         public int paper_state { get; set; }
#         public int paper_sort { get; set; }
#         public DateTime paper_invalidtime { get; set; }
#         public List<string> monitor_url;

class WallpaperInfo(Serializable):
    def __init__(self):
        self.paper_id=None
        self.paper_name=None
        self.paper_url=None
        #1横板,2竖版
        self.paper_bagtype=None
        self.paper_time=None
        self.paper_state=None
        self.paper_sort=None
        self.paper_invalidtime=None
        self.monitor_url=[]
 

if __name__ == '__main__':
    pass
