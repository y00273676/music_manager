#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os

username ='mengda'
password ='mengda'

def scopy(filepath):
    #ls -R
    output = os.system("\"C:\\thunder\\winscp\\WinSCP.exe\" /script="+str(filepath))
    print ("\"C:\\thunder\\winscp\\WinSCP.exe\" /console /script="+str(filepath))
    if os.path.exists(filepath):
        os.remove(filepath)
    
def writefile(filepath,user,pwd,ipinfo,redir,todir):
    f = open(filepath, 'w')
    print (filepath)
    f.write("option confirm off"+'\n')
    for item in ipinfo:
        f.write("open "+str(user)+":"+str(pwd)+"@"+str(item))
        f.write(" -hostkey=*"+'\n')
        f.write("call mkdir -p "+str(todir)+'\n')
        f.write("put "+str(redir)+" "+str(todir)+'\n')
        f.write("close"+'\n')
    f.write("exit"+'\n')
    f.close()
    scopy(filepath)
    
def deletefile(filepath,user,pwd,ipinfo,todir):
    f = open(filepath, 'w')
    print (filepath)
    f.write("option confirm off"+'\n')
    for item in ipinfo:
        f.write("open "+str(user)+":"+str(pwd)+"@"+str(item))
        f.write(" -hostkey=*"+'\n')
        f.write("call rm -rf "+str(todir)+'\n')
        f.write("close"+'\n')
    f.write("exit"+'\n')
    f.close()
    scopy(filepath)
    
if __name__ == '__main__':
    writefile('e:\willrun.txt',username,password,['10.0.3.111:222'],"E:/videos","/home/mengda/videos/video")
    
