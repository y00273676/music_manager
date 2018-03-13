#!/usr/bin/python
# -*- coding: UTF-8 -*-

class PublicFunc():
    def GetStrValue(self, strSource, targets):
        strSource = strSource[strSource.index(' ') + 1:]
        name = None
        str_items = strSource.split(':')
        i = 0
        for res in str_items:
            index = res.rindex(' ')
            last_value = ""
            if i < len(str_items) - 1:
                n = 0
                if index>0:
                    n = index+1
                
                name = res[n:]
                u = 0
                if index > 0:
                    u = index
                last_value = res[:u]
            else:
                last_value = res[0:]
            if i > 0 and len(targets) >= i:
                targets[i - 1] = last_value
            i += 1
    