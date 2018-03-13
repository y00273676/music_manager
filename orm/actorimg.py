#!/usr/bin/env python
#coding=utf8
from io import BytesIO
import socket
import struct
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
DBASS_IP = '127.0.0.1'
# DBASS_IP = '192.168.1.210'

def get_actor_pic(aid=0, aname=''):
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket.connect((DBASS_IP,3233))
    query="Get_H_Actor_Photo3D 1:%s 2:NULL 3:NULL 4:NULL 5:NULL 6:NULL 7:NULL 8:NULL 9:NULL 10:NULL 11:NULL 12:NULL STB_IP:127.0.0.1\r\n\r\n" % str(aid)
    mysocket.send(query)
    head=mysocket.recv(4)
    (length,)=struct.unpack("i", head)
    #not sure why, but need to skip 4 byte for the real bmp file content
    skip=4
    head=mysocket.recv(skip)
    length -= skip

    buf=""
    while length:
        if length >= 1024:
            data=mysocket.recv(1024)
        else:
            data=mysocket.recv(length)
        if data:
           buf += data
           length -= len(data)
        else:
            break
    mysocket.close()
    bio = BytesIO(buf)
    im = Image.open(bio)
#     print "actor_id: %d" % (aid)
    #im = Image.frombuffer('RGB', (150,150), buf)
    #im = Image.frombytes('RGB', (150,150), buf)
    #im = Image.open(bio)
    #im.load()
    n = im.rotate(180)
    imgio = BytesIO()
    n.save(imgio, 'bmp')
    #n_buff = n.tobytes()
    return imgio.getvalue()

#     n.save("/tmp/actor_%d_r.jpg" % aid)

if __name__ == '__main__':
    aid=33
    aname=""
    for i in range(100, 120):
        get_actor_pic(i, aname)
