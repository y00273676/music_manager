'''
Created on 2017年4月28日

@author: yeyinlin
'''
import os
class localfileutils(object):
    
    def __init__(self):
        pass
    
    #删除文件夹下 与本次不同的文件 报错文件夹的干净
    def dellocalfile(self,path,filelist):
        for root , dirs, files in os.walk(path):
            print (files)
            for name in files:
                print (name)
                if  name not in filelist:
                    os.remove(os.path.join(path, name))

if __name__ == '__main__':
    pass