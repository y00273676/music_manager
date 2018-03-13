#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-18 15:22:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


from lib import http
from orm import orm as _mysql
import ConfigParser
from lib.iniconfig import IniConfig
import chardet
import codecs


def update_setting(ShowName,AppValue, IsString,result, optionvalue, optionname, addflag):
    params = {}
    params['ShowName'] = ShowName
    params['AppValue'] = AppValue
    params['IsString'] = IsString
    params['result'] = result
    params['optionvalue'] = optionvalue
    params['optionname'] = optionname
    params['addflag'] = addflag

    return _mysql.boxset.update(AppValue, params)

def update_set(AppValue,result, optionvalue):
    params = {}
    params['AppValue'] = AppValue
    params['result'] = result
    params['optionvalue'] = optionvalue

    return _mysql.boxset.update(AppValue, params)
def update_flag(flag):
    return _mysql.boxset.updateflag(flag)

def get_all_set_list():
    res = _mysql.boxset.get_all()
    if isinstance(res, list) and len(res) > 0:
        return res
    return None
#写入文件
def update_set_ini(filename,option):
    cf = IniConfig()
    cf.read(filename)
    for item in option:
        if item['optionvalue']=="":
            if  get_all_config_no_filename(item['appvalue']):
                cf.set("PROSET", item['appvalue'], '1')
        else:
            cf.set("PROSET", item['appvalue'], item['optionvalue'])
    cf.write(open(filename, "w"))

def remove_set_ini(filename,section):
    cf = IniConfig()
    cf.read(filename)
    sections = cf.sections()
    if len(sections)==1:
        cf.add_section("PROSET")
    else:
        cf.remove_section(section)
        cf.add_section(section)
    cf.write(open(filename, "w"))
def remove_update_ini(filename,section,option,args):
    cf = IniConfig()
    cf.read(filename)

    cf.set("STB", "IP", args['ipaddress'])
    cf.set("STB", "NMASK", args['subnetmask'])
    cf.set("STB", "SERVER", args['serviceip'])
    cf.set("STB", "STBType", args['devicetype'])
    cf.set("STB", "RecordSvr", args['iprecond'])
    cf.set("STB", "Name", args['name'])
    
    sections = cf.sections()
    if len(sections)==1:
        cf.add_section("PROSET")
    else:
        cf.remove_section(section)
        cf.add_section(section)
        
    for item in option:
        if item['optionvalue']=="":
            if  get_all_config_no_filename(item['appvalue']):
                cf.set("PROSET", item['appvalue'], '1')
        else:
            cf.set("PROSET", item['appvalue'], item['optionvalue'])
    cf.write(open(filename, "w"))
    
    
    
    






def get_all_set_list_ini(filename):
    datajson={}
    cf = IniConfig()
    cf.read(filename)
    stb=cf.items("STB")
    proset=cf.items("PROSET")
    _mjson={}
    _mprjson={}
    for colum in stb:
        _mjson[colum[0]]=(colum[1])#.decode('gb2312').encode('utf8')
    for columone in proset:
        _mprjson[columone[0]]=columone[1]

    #需要转换编码
    datajson['box']=_mjson
    datajson['option']=_mprjson
    return datajson

def get_all_config_no_filename(valuestr):
    filename="/opt/thunder/bin/dhcp/Config.ini"
    config=get_all_config_ini(filename)
    print config
    for signcon in config:
        print   signcon
        if signcon['AppValue'] ==valuestr:
            if signcon['IsString']=="0":
                return True
            else:
                return False
    
    
    return False
        
    
    

def get_all_config_ini(filename):
    item=[]
    cf = open(filename,"r")
    data = cf.read()
    print chardet.detect(data)
    f = codecs.open(filename, "r",chardet.detect(data)['encoding'])
#     f.readfp(codecs.open(filename, "r", chardet.detect(data)['encoding']))
    while True:
        line = f.readline()
        if line:
            pass    # do something here
            line=line.strip()
            if(line=='[ITEM]'):
                datajson={}
                item.append(datajson)
            else:
                key_val=line.split("=")
                if(len(key_val)>1):
                    datajson[key_val[0]]=key_val[1]
                else:
                    datajson["select"]=key_val[0]
        else:
            break
    f.close()
    return item

def add_config_ini(filename,mdata,mencode):
    try:
        f = codecs.open(filename, "a",mencode)
        f.write(("[ITEM]"+'\r\n'))
        f.write("ShowName="+mdata['ShowName']+'\r\n')
        f.write("AppValue="+mdata['AppValue']+'\r\n')
        f.write("IsString="+mdata['IsString']+'\r\n')
        f.write("result="+mdata['result']+'\r\n')
        if mdata['result']=="1":
            f.write((mdata['select']+'\r\n'))
        f.close()
       
    except Exception, e:
        raise e
    
def add_defuct_config_ini(filename,data):
    try:
        f = codecs.open(filename, "a",'gbk')
        f.write("[ITEM]"+'\r\n')
        f.write("ShowName="+data['ShowName']+'\r\n')
        f.write("AppValue="+data['AppValue']+'\r\n')
        f.write("IsString="+str(data['IsString'])+'\r\n')
        f.write("result="+str(data['result'])+'\r\n')
        if str(data['result'])=="1":
            f.write((data['select']+'\r\n'))
        f.close()
    except Exception, e:
        raise e


def updata_config_ini(filename,data):
    try:
        alldata=get_all_config_ini(filename)
        #删除所有文件
        delete_all_config_ini(filename)
        
        cf = open(filename,"r")
        tdata = cf.read()
        encode=chardet.detect(tdata)['encoding']
        
        for mdata in alldata:
            if mdata['AppValue']==data['AppValue']:
                add_config_ini(filename,data,encode)
            else:
                add_config_ini(filename,mdata,encode)
        
    except Exception, e:
        raise e
    
def updata_defuct_config_ini(filename,data):
    try:
        alldata=get_all_config_ini(filename)
        delete_all_config_ini(filename)
        for mdata in alldata:
            if mdata['AppValue']==data['AppValue']:
                add_config_ini(filename,data)

            else:
                add_config_ini(filename,mdata)
    except Exception, e:
        raise e

def delete_all_config_ini(filename):
    try:
        cf = open(filename,"r")
        data = cf.read()
        print chardet.detect(data)
        f = codecs.open(filename, "w",chardet.detect(data)['encoding'])
        f.write('')
        f.close()
    except Exception, e:
        raise e

def delete_config_ini(filename,data):
    try:
        alldata=get_all_config_ini(filename)
        delete_all_config_ini(filename)
        for mdata in alldata:
            if mdata['AppValue']==data['AppValue']:
                pass
            else:
                print mdata
                add_config_ini(filename,mdata)

                
        
    except Exception, e:
        raise e
    
def delete_defuct_config_ini(filename,data):
    try:
        alldata=get_all_config_ini(filename)
        delete_all_config_ini(filename)
        for mdata in alldata:
            if mdata['AppValue']==data['AppValue']:
                pass
            else:
                add_config_ini(filename,mdata)
    except Exception, e:
        raise e
    






