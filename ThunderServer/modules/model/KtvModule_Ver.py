#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年4月13日

@author: yeyinlin
'''
from modules.model.common import *
class KtvModule_Ver(Serializable):
    def __init__(self):
        self.id=0
        self.name=""
        self.addtime=""
        self.fileurl=""
        self.unpath=""
        self.version=""
        self.isuse=""
        self.needun=""
        self.desc=""
        self.msgtime=""
        self.isshow=""
        self.bagtype=-1
        self.isdefault=""
        self.reversion=""
        self.vertype=""
    
if __name__ == '__main__':
    pass
