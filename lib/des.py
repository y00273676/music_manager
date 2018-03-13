#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@author: rui.xu
#这里使用pycrypto
#按照方法:easy_install pycrypto
 
from Crypto.Cipher import DES,AES
import hashlib
from binascii import b2a_hex,a2b_hex

class DESEncrypt(object):
    def __init__(self):
        self.key = 'qierxiche@1351900'
        #self.PADDING = '\0'
        #self.pad_it = lambda s:s+(16-len(s)%16)*self.PADDING
        #self.pad_it = lambda s:s+(8-len(s)%8)*self.PADDING

    def encrypt(self,text,key=None, mode=2):
        key = key if key else self.key
        key = hashlib.md5(key).hexdigest().upper()[0:8]
        #obj = DES.new(key, DES.MODE_CBC, key)
        obj = DES.new(key, mode, key)
        length = 8
        count = len(text)
        if count < length:
            add = (length-count)
            text = text + (' ' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\x08' * add)

        crypt = obj.encrypt(text)
        return b2a_hex(crypt)
	
    def decrypt(self,text,key=None):
        key = key if key else self.key
        key = hashlib.md5(key).hexdigest().upper()[0:8]
        obj = DES.new(key,DES.MODE_CBC,key)
        get_cryp = a2b_hex(text)
        after_text = obj.decrypt(get_cryp)
        return after_text.strip('\x08')
        #return after_text.strip('\x02')


if __name__ == '__main__':
    import sys
    t = sys.argv[1]
    v = sys.argv[2]
    k = None
    if len(sys.argv) == 4:
        k = sys.argv[3]
    des = DESEncrypt()
    if t == '1':
        print '*q2qvot7 -> 2179856D06B3B4A6'
        for mode in [1,2,3,5,7]:
            print "%s -> %s" % (v, des.encrypt(v, k, mode))
    elif t== '2':
        print des.decrypt(v,k)
    else:
        print 'argv error'
