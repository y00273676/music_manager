#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import chardet
#from lib.iniconfig import IniConfig

#from control.ktvinfo import KTVInfo

if __name__ == '__main__':
    #k = KTVInfo()
    #print k.get_ktvinfo()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print(sys.getdefaultencoding())
    print(u'你们好，这是一个中文测试 %s' % sys.getdefaultencoding())

