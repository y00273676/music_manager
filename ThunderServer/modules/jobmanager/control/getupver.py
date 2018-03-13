'''
Created on 2017年4月19日

@author: yeyinlin
'''
import win32api
import os
from config.appConfig import AppSet
class getupver(object):
    def __init__(self):
        pass

    def getversion(self):
        file_name=self.getpath()
        info = win32api.GetFileVersionInfo(file_name, os.sep)
        print(info)
        ms = info['FileVersionMS']    
        ls = info['FileVersionLS']
        version = '%d.%d.%d.%d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls),win32api.LOWORD(ls))  
        print(version)
        return version

    def getpath(self):
        cwd=os.path.dirname(os.getcwd())
        start=cwd.split("ThunderServer")[0]
        filename = os.path.join(start+"ThunderServer", 'lib\ktvmoduleservice.exe')
        print(filename)
        return filename

if __name__ == '__main__':
    pass
