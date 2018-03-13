import json
import struct
import pickle
import copy

class Serializable(object):
    extra_vars = []
    def __str__(self):
        '''
        default method to serializable, will call this function when use:
         - print( obj )
         - str(obj) 
        '''
        print('in func __str__()')
        return self.to_str()

    def to_str(self):
        ret = copy.deepcopy(self.__dict__)
        for key in self.extra_vars:
            ret[key] = getattr(self, key)

        res = json.dumps(ret, ensure_ascii=False)
        return res

    def to_dict(self):
        '''
        serialize to a json object, 
        we may need to return this json object to framework for http response
        '''
        print('in func to_dict()')
        ret = copy.deepcopy(self.__dict__)
        for key in self.extra_vars:
            ret[key] = getattr(self, key)

        return ret
 

class StructLayout(Serializable):
    '''
    struct_layout:
    [{variable, pack_type}, {variable2, pack_type2}, ....]
    pack_type refer to the type defines of struct.pack()
    
    refer to : http://blog.csdn.net/w83761456/article/details/21171085
    '''
    struct_layout = []
    def __bytes__(self):
        '''
        '''
        buf = b''
        #print('----', self.__dict__)
        for k, _style in self.struct_layout:
            var = getattr(self, k)
            if isinstance(var, str):
                buf += struct.pack(_style, var.encode(encoding='gbk'))
            else:
                if not _style.startswith("!"):
                    _style = '!' + _style
                #print(_style, k, var)
                buf += struct.pack(_style, var)
        return buf


if __name__ == '__main__':
    class test(StructLayout):
        struct_layout = [('id','h'), ('time', '16s'), ('Names', '16s')]
        extra_vars = ['Names']
        def __init__(self):
            self.id = 1
            self.time = '2017-04-07 09:00:00'
            self.type = 'test type'
            self.f_name = 'Shunli'
            self.l_name = 'Yi'
            pass

        @property
        def Names(self):
            return self.f_name + ',' + self.l_name


    a = test()

    a.id = 156
    #print (a.__builtins__.__dict__)
    print(a)
    print (bytes(a))
