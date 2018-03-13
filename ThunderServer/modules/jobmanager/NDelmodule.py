'''
Created on 2017年5月3日
删除模板
@author: yeyinlin
'''
from modules.bll.KtvModuleVerBLL import KtvModuleVerBll
import os
from asyncio.log import logger
import time
from config.appConfig import AppSet
import traceback
class NDelmodule():
    def __init__(self):
        #能够删除的集合
        self.candelect=[]
        #模板主题删除的集合
        self.candel_v2=[]
        #标记一下文件夹下应该有的
        self.nodel_path=[]
        
        self.ApacheDocsPath=AppSet().GetCloudKtvIniValue('ApacheDocsPath')
        #模板所处的位置
        self._modulepath=os.path.join(self.ApacheDocsPath,"modules")
        
        self._bll=KtvModuleVerBll()
        
    def dellocalmodule(self):
        #拿到本地的模板 数据库查询
        res_list=KtvModuleVerBll().GetModuleVer()
        # 按最新的版本号排列
        res_list.sort(key=lambda obj:obj.revision, reverse=True)
        if res_list:
            if len(res_list)>0:
                for i in range(0,len(res_list)):
                    if i>14 and (not res_list[i].isdefault) and (res_list[i].isuse!=1):
                        self.candelect.append(res_list[i])
                    else:
                        fileName=os.path.basename(res_list[i].fileurl)
                        fileName=os.path.join(self._modulepath,fileName).lower()
                        self.nodel_path.append(fileName)
                        
        #获取模板主题
        themeList=self._bll.GetAllKtvModule_Theme(1)
        if themeList:
            if len(themeList)>0:
                for theme in themeList:
                    if int(theme.theme_state)==1:
                        self.nodel_path.append(theme.theme_path)
                    else:
                        if os.path.exists(theme.theme_path):
                            #如果给了只读权限，需要去给予可读写权限 并删除
                            if os.stat(fileName).st_mode==os.stat.S_IREAD:
                                os.chmod(os.stat.S_IRWXU)
                            os.remove(fileName)
        #删除掉超过15条的数据
        self.DeleteVLocalModule(self.candelect)
        #删除数据库里不存在的
        self.DeleteNoLocal(self.nodel_path)
        
    def DeleteVLocalModule(self,list):
        
        for item in list:
            fileName=os.path.basename(item.fileurl)
            fileName=os.path.join(self.ApacheDocsPath, "modules",fileName)
            #权限设置
            if os.stat(fileName).st_mode==os.stat.S_IREAD:
                os.chmod(os.stat.S_IRWXU)
            if os.path.exists(fileName):
                os.remove(fileName)
                logger.debug("删除文件",fileName)
                #TODO 删除
                bll=KtvModuleVerBll()
                bll.DeleteVer(item.id)
                
            dir=item.uppath
            mtime=time.strftime('%m',os.path.getmtime(dir))
            ctime=time.strftime('%m',time.localtime(time.time()))
            if os.path.exists(dir) and (int(ctime)-int(mtime)>=1):
                os.remove(dir)
    def DeleteNoLocal(self,_nodellist):
        try:
            if not _nodellist and len(_nodellist)<=0:
                return
            
            module_path=os.path.join(self.ApacheDocsPath,"modules")
            if os.path.exists(module_path):
                m_paths=getListFiles(module_path)
                for path in m_paths:
                    if not (path.lower() in _nodellist):
                        os.remove(path)
                        logger.debug("删除文件",path)
                
                if os.path.exists(module_path):
                    m_dirs=getListDirs(module_path)
                    pathstr="C:\\thunder\\Apache\\htdocs\\modules\\moduledatatype"
                    for dir in m_dirs:
                        print(dir)
                        if pathstr.lower()==dir.lower():
                            continue
                        if not (dir in _nodellist):
                            print(os.path.getmtime(dir))
                            mtime=time.strftime('%m',time.localtime(os.path.getmtime(dir)))
                            ctime=time.strftime('%m',time.localtime(time.time()))
                            if os.path.exists(dir) and (int(ctime)-int(mtime)>=1):
                                try:
                                    os.remove(dir)
                                except:
                                    pass
        except Exception as e:
            print("traceback.format_exc()",traceback.format_exc())


def getListFiles(path): 
    ret = [] 
    for root, dirs, files in os.walk(path): 
        for filespath in dirs: 
            if  filespath:
                ret.append(os.path.join(root,filespath)) 
    return ret

def getListDirs(path): 
    ret = [] 
    for root, dirs, files in os.walk(path): 
        for filespath in dirs: 
            ret.append(os.path.join(root,filespath)) 
    return ret
if __name__ == '__main__':
    mo=NDelmodule()
    mo.dellocalmodule()