#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月28日

@author: yeyinlin
'''
from modules.model.common import StructLayout

class SynFileStatus(StructLayout):
    struct_layout = [('tagpath', '256s'),('status', 'I'),('remark', '256s')]
    def __init__(self):
        self.tagpath=''
        self.status=-1
        self.remark=''

if __name__ == '__main__':
    sn=SynFileStatus()
    sn.tagpath='sjkfjal'
    sn.status=1
    sn.remark='lallal'
    print(type(sn))
    print(type(str(sn)))
    print(sn)
    
