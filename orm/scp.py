#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import getpass
#import pexpect
import logging
import paramiko
import multiprocessing 
import time 
import datetime
import sys
import commands
from threading import Thread

logger = logging.getLogger(__name__)


host = '10.0.4.51'
port = 22
username = 'thunder'
password ='Thunder#123'

home_dir = os.getenv('HOME')
id_rsa_pub = '%s/.ssh/id_rsa.pub' %home_dir

if not  id_rsa_pub:
    print 'id_rsa.pub Does not exist!'
    sys.exit(0)

# file_object = open('%s/.ssh/config' %home_dir ,'w')
# file_object.write('StrictHostKeyChecking no\n')
# file_object.write('UserKnownHostsFile /dev/null')
# file_object.close()
#os.chmod('%s/.ssh/config' % home_dir, 600)

def up_key(host, port, user, passwd):
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, port, user, passwd)

        t = paramiko.Transport((host, port))
        #connect(self, hostkey=None, username='', password=None, pkey=None)
        t.connect(username=user, password=passwd)
        sftp =paramiko.SFTPClient.from_transport(t)

        print 'create Host:%s .ssh dir......' %host
        stdin,stdout,stderr=s.exec_command('mkdir ~/.ssh/')
        print 'upload id_rsa.pub to Host:%s......' %host
        sftp.put(id_rsa_pub, "/tmp/temp_key")
        stdin,stdout,stderr=s.exec_command('cat /tmp/temp_key >> ~/.ssh/authorized_keys && rm -rf /tmp/temp_key')
        stdin,stdout,stderr=s.exec_command('chmod 600 ~/.ssh/authorized_keys')
        print 'host:%s@%s auth success!\n' %(user, host)
        s.close()
        t.close()
    except Exception, e:
        import traceback
        traceback.print_exc()
        print 'connect error...'
        print 'delete ' + host  + ' from database...'
        #delip(host)
        #delete from mysql****
        try: 
            s.close()
            t.close()
        except:
            pass

def view_bar(num=1, sum=100, bar_word=":"):
    rate = float(num) / float(sum)
    rate_num = int(rate * 100)
    print '\r%d%% :' %(rate_num),
    for i in range(int(num)/10):
        os.write(1, bar_word)
    sys.stdout.flush()

def scopy(sfile, dfile):
    #ls -R
    raise TypeError
    output = commands.getoutput('scp -r -p '+ sfile + ' ' + username + '@' + host + ':' + dfile)
    
    ld=pexpect.spawn('scp -r -p '+ sfile + ' ' + username + '@' + host + ':' + dfile)
    ld.expect('password:',timeout=None)
    ld.sendline(password)
    ld.expect(pexpect.EOF,timeout=None)
    ld.read()


def rfile(dfile):
    try:
        ssh=paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(host, port, username, password)
        #stdin,stdout,stderr=ssh.exec_command('ls /home')
        stdin,stdout,stderr=ssh.exec_command('du -s ' + dfile)
        abc=stdout.readlines()[0].split()[0]
        return abc
    except Exception,e:
        return 0

def progress_bar(transferred, toBeTransferred, suffix=''):
    # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
    bar_len = 60
    filled_len = int(round(bar_len * transferred/float(toBeTransferred)))
    percents = round(100.0 * transferred/float(toBeTransferred), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def scpFile(sfile, dfile):
    t=paramiko.Transport((host, port)) 
    t.connect(username=username, password=password) 
    sftp=paramiko.SFTPClient.from_transport(t) 
    print '####################################################' 
    print 'Begin to upload file  to %s ' % host 
    print 'Uploading ', sfile 
    
    print datetime.datetime.now() 
    sftp.put(sfile, dfile, callback=progress_bar) 
    print datetime.datetime.now() 
    print '####################################################' 
    t.close() 

def scpDir(local_dir, remote_dir):
    t=paramiko.Transport((host, port)) 
    t.connect(username=username, password=password) 
    sftp=paramiko.SFTPClient.from_transport(t) 
    files=os.listdir(local_dir) 
    print files 
    for f in files: 
        print '####################################################' 
        print 'Begin to upload file  to %s ' % host 
        print 'Uploading ',os.path.join(local_dir,f) 

        print datetime.datetime.now() 
        sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir, f), callback=progress_bar) 
        print datetime.datetime.now() 
        print '####################################################' 
        t.close() 
        
def scopyIp(ip,file):
    #ls -R
    linuxCommand = 'docker exec -t thunder ssh '+str(ip)+' mkdir -p '+str(file[0:file.rfind('/')+1])
    print linuxCommand
    ret, out = commands.getstatusoutput(linuxCommand)
    if ret == 0:
        linuxCommand = 'docker exec -t thunder scp -r -p '+str(file)+' '+str(ip)+':'+str(file)
        print linuxCommand
        ret, out = commands.getstatusoutput(linuxCommand)
        if ret == 0:
            return 'success'
        else:
            logger.error('Error,command: %s , output: %s' % (linuxCommand, out))
            return 'error'
    else:
        logger.error('Error,command: %s , output: %s' % (linuxCommand, out))
        return 'error'
    

if __name__=='__main__':
#    host = raw_input('Please input the host: ')
#    port = raw_input('Please input the port(default 22): ')
#    if port.isdigit():
#        port = int(port)
#    else:
#        port = 22
#    uname = raw_input('Username: ')
#    pswd = getpass.getpass('password: ')
	
#    print host, port, username, password
#    up_key(host, port, username, password)
    
    sfile = '/video/disk-01/v38.4/v38.4-HD/6907215.ts'
    dfile = '/video/disk-01/v38.4/v38.4-HD/6907215.ts'
    scopy(sfile, dfile)
#     scpFile(sfile, dfile);


