#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import commands
import subprocess

def shell(**kwargs):
    p = subprocess.Popen([kwargs['shell'], kwargs['params']], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #???ݸ?shell??ַ???
    output = p.communicate('foo')[0]
    print (output)


def getnetworkparams():
    thefile = '/etc/network/interfaces'
    file_object = open(thefile)
    inx = 0
    dict={}
    for line in file_object:
        line = line.strip()
        if line.startswith('auto lo'):
            print('lo')
        elif line.startswith('iface em1 inet static'):
            inx = 1
        elif line.startswith('iface em2 inet static'):
            inx = 2
        elif line.startswith('iface em3 inet static'):
            inx = 3
        elif line.startswith('iface em4 inet static'):
            inx = 4
        elif line.startswith('address'):
            dict['em' + str(inx) + '_address']=line[8]
        elif line.startswith('netmask'):
            dict['em' + str(inx) + '_netmask']=line[8]
        elif line.startswith('broadcast'):
            dict['em' + str(inx) + '_broadcast']=line[9]
        elif line.startswith('gateway'):
            dict['em' + str(inx) + '_gateway']=line[7]
        elif line.startswith('dns-nameservers'):
            dict['em' + str(inx) + '_nameservers']=line[15]
        file_object.close()

    return dict;

def setnetworkparams(kwargs):
    #save2file
    thefile = '/home/mengda/interfaces.2'
    file_object = open(thefile, 'w')

    file_object.write('auto lo\n')
    file_object.write('iface lo inet loopback\n')
    file_object.write('\n')

    for inx in range(14):
        if kwargs['em' + str(inx) + '_address']!='':
            file_object.write('iface em' + str(inx) + ' inet static\n')
            file_object.write('\taddress ' + kwargs['em' + str(inx) + '_address'] + '\n')

            if kwargs['em' + str(inx) + '_netmask']!='':
                file_object.write('\tnetmask ' + kwargs['em' + str(inx) + '_netmask'] + '\n')
            if kwargs['em' + str(inx) + '_broadcast']!='':
                file_object.write('\tbroadcast ' + kwargs['em' + str(inx) + '_broadcast'] + '\n')
            if kwargs['em' + str(inx) + '_gateway']!='':
                file_object.write('\tgateway ' + kwargs['em' + str(inx) + '_gateway'] + '\n')
            if kwargs['em' + str(inx) + '_nameservers']!='':
                file_object.write('\tdns-nameservers ' + kwargs['em' + str(inx) + '_nameservers'] + '\n')




        file_object.write('\n')

    file_object.close()

if __name__ == '__main__':

    params = getnetworkparams()

    setnetworkparams(params)
