'''
Created on 2017年4月18日

@author: yeyinlin
'''
import json
class interfaceBase():
    def __init__(self):
        pass
    def SendListToStb(self,receivecmd,socketclient,dict):
        if list:
            json_str=json.dumps(dict)
            data=json_str.encode('utf-8')
            self.SendToStb(receivecmd,socketclient,data,len(data))
    #发送数据
    def SendToStb(self,receivecmd,socketclient,data,total):
        print("SendToStb")
        
    
if __name__ == '__main__':
    pass