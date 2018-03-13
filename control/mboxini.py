from lib import http
import ConfigParser
from lib.iniconfig import IniConfig
import os
import os.path
import chardet
import codecs


def read_path_ini():
    mydata={}
    cf = ConfigParser.ConfigParser()
    cf.read('path.ini')
    str_a = cf.get("sec_a", "boxtypepath")
    mydata['boxtypepath']=str_a
    return mydata

def get_box_type_ini():
    f = open(read_path_ini()['boxtypepath'],"r")
    data = f.read()
    return read_all_info_init(read_path_ini()['boxtypepath'],chardet.detect(data)['encoding'])

def read_all_info_init(filename,strcode):
    datajson={}
    cf = IniConfig()
    # cf.read(filename)
    cf.readfp(codecs.open(filename, "r", strcode))
    sections = cf.sections()
    mainserver=cf.items("Boxtype")
    
    _mjson={}
    for colum in mainserver:
        _mjson[colum[0]]=colum[1]
    
    return  _mjson
    
   
