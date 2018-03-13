#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-02 13:45:20
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import codecs
import IniConfig

class  EcodeIni:
    config=None
    fileName=''


    def  _init_(self,filename,strcode="gbk"):
        self.config=IniConfig()
        self.fileName=filename
        if not strcode:
            self.config.read(self.fileName)
        else:
            if strcode.lower()=="gbk":
                fp=codecs.open(filename,"r",strcode)
                if not fp:
                    raise "config file maybe not exist."
                else:
                    self.config.readfp(fp)
            else:
                self.config.read(self.fileName)

        def writeIni(self,sectionName,keyName,value):
            if sectionName not in self.config.sections():
                self.config.add_section(sectionName)

            self.config.set(sectionName,keyName,value)
            self.config.write(open(self.fileName,"w"))


        def readIniStr(self,sectionsName,keyName):
            if sectionName in self.config.sections()/
                and keyName in self.config.options(sectionName):
                    return self.config.get(sectionName,keyName)
            else:
                return None

        def readIniInt(self, sectionName, keyName):
            keyName = keyName.lower()
            try:
                if sectionName in self.config.sections()/
                    and keyName in self.config.options(sectionName):
                    return self.config.getint(sectionName, keyName)
                else:
                    return None
            except Exception, e:
                print '    Exception: ', e
                return None







