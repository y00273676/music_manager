#!/usr/bin/env python
# -*- coding: utf-8 -*- 大小写的问题的区别和修改了键值对的空格

import sys
import codecs
import logging
import traceback
if sys.version_info < (3,):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser
#from setting import SETTING_DEBUG
SETTING_DEBUG = 1


class IniConfig(ConfigParser):
    def __init__(self, inifile):
        super(IniConfig, self).__init__()
        self.fpath = inifile
        #fp = open(self.fpath, encoding='utf_8_sig')
        if SETTING_DEBUG:
            fp = codecs.open(self.fpath, "r", encoding="utf-8-sig")
        else:
            fp = codecs.open(self.fpath, "r", encoding="gbk")
        self.readfp(fp)

    def optionxform(self, optionstr):
        return optionstr

    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s=%s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = "=".join((key, str(value).replace('\n', '\n\t')))
                fp.write("%s\n" % (key))
            fp.write("\n")

    def ReadString(self, section, option, def_val):
        ret = self.get(section, option)
        if ret == None:
            return def_val
        else:
            return ret

    def WriteInteger(self, section, option, int_val):
        try:
            if isinstance(int_val, int):
                #re-load again
                self.read(self.fpath, encoding='utf_8_sig')
                self.set(section, option, str(int_val))
            else:
                raise TypeError('call WriteInteger with non-integer parameters')
        except TypeError as ex:
            raise ex
        except Exception as ex:
            logging.error(traceback.format_exc())
            return False

if __name__ == '__main__':
    ts = IniConfig()
    ts.read('/tmp/tmp.ini')
    ts.set('Main', 'Test', 'Test')
    ts.write(open('/tmp/tmp.ini', 'wb'))

