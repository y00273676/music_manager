#!/usr/bin/env python
# -*- coding: utf-8 -*- 大小写的问题的区别和修改了键值对的空格

import ConfigParser

class IniConfig(ConfigParser.ConfigParser):
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

if __name__ == '__main__':
    ts = IniConfig()
    ts.read('/tmp/tmp.ini')
    ts.set('Main', 'Test', 'Test')
    ts.write(open('/tmp/tmp.ini', 'wb'))

