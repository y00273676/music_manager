'''
Created on 2017年4月7日

@author: yeyinlin
'''
import json
from common.KtvInfo import KtvInfo
from common.yhttp import yhttp
from modules.jobmanager.control.getupver import getupver
class upappver():
    def __init__(self):
        self.ktvinfo=KtvInfo()._info
        self.cks_ver=getupver().getversion()
    def upapp_version(self,jsonstr):
        paramname=yhttp().UrlEncode('r='+(jsonstr))
        strurl='http://tj.ktvdaren.com/log/app_ver'
        res=yhttp().get_y(strurl+"?"+paramname, 10)
    def getjson(self):
        info=self.ktvinfo
        #需要去获取版本号
        cks_ver=self.cks_ver
        data={}
        data['ktv_id']=info._ktvid
        data['ktv_name']=info._ktvname
        data['province']=info._provincename
        data['city']=info._city
        data['jwd']=str(info._jd) + "," + str(info._wd)
        data['appname']="thunderservice"
        data['app_ver']=cks_ver
        res=self.upapp_version(json.dumps(data))
        

if __name__ == '__main__':
    up=upappver().getjson()
    