'''
Created on 2017年4月19日

@author: yeyinlin
'''
import zipfile

class moduleoperation(object):
    '''
    classdocs
    '''
    _ins = None
    @staticmethod
    def Ins():
        if not moduleoperation._ins:
            moduleoperation._ins = moduleoperation()
        return moduleoperation._ins

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def canimport(self,trytime,  exectime,  cur_time):
        can = True
        if (trytime > 5):
            can = False
        if (trytime == 1 and (exectime + 60) > cur_time):
            can = False;
        if (trytime == 2 and (exectime + 10 * 60) > cur_time):
            can = False;
        if (trytime == 3 and (exectime + 30 * 60) > cur_time):
            can = False;
        if (trytime >= 4 and (exectime + 90 * 60) > cur_time):
            can = False;
        return can;
    def unzip(self,path,pathone):
        zfile = zipfile.ZipFile(path,'r')
        for filename in zfile.namelist():
            data = zfile.read(filename)
            file = open(filename, 'w+b')
            file.write(data)
            file.close()
        return True