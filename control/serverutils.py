import commands
import os  
import platform  
import subprocess  
import signal  
import time  

#SUPERVISORCTL = "supervisorctl -c /opt/etc/supervisor/supervisord.conf"
SUPERVISORCTL = "supervisorctl"

def lsPath(path):
    output = commands.getoutput('ls -R ' + path + '')
    #print status, output
    files = output.split('\n');
    for file in files:
        if file.startswith('/'):
            path = file[1 : len(file)-1]
        else:
            print file + '    ' + path + '/' + file

def lsService():
    output = commands.getoutput('%s status' % SUPERVISORCTL)
    #rint(output)
    lines = output.split('\n')
    jsondata=[]
    
    index = 0
    for line in lines:
        mydata={}
        items = line.split(' ')
        index = 0
        pname = items[0]
        mydata['pname']=pname
        for item in items:
            if index>0 and item!='':
                status= item
                mydata['status']=status
                break
            index = index + 1
        jsondata.append(mydata)
    return jsondata
        
def actionCommand(localpath,ip):
    comstr='docker exec thunder rsync -avz --delete '+localpath +' root@'+ip+':'+localpath
    print "xxxxx",comstr
    output = commands.getoutput(comstr)
    return output     

def action_config_command(localpath,ip):  
    comstr='docker exec thunder rsync -avz '+localpath +' root@'+ip+':'+localpath
    print "xxxxx",comstr
    output = commands.getoutput(comstr)
    return 0 

def action_other_command_docker(localpath,ip):  
    comstr='docker exec thunder rsync -avz '+localpath +' root@'+ip+':'+localpath
    print "xxxxx",comstr
    output = commands.getoutput(comstr)
    if 'level=fatal' in output or 'No route to host' in output:
        print "xxexcptionxxx",output
        return 1 
    print "xxoutputxxx",output
    return 0 

def action_delete_command(localpath,ip):  
    comstr='docker exec thunder rsync --delete  root@'+ip+':'+localpath
    print "xxxxx",comstr
    output = commands.getoutput(comstr)
    return 0     

def actionService(service, action):
    output = commands.getoutput('%s %s %s' % (SUPERVISORCTL, action, service))
    print(output)
    if "unrecognized" in output:
        return 1
    else:
        return 0
   

def stopService(service):
    return actionwithoutTime(service, 'stop')

def startService(service):
    return actionwithoutTime(service, 'start')

def restartService(service):
    try:
        return actionwithoutTime(service, 'restart')
    except:
        return 1
def startServiceOut(service):
    return actionwithoutTime(service, 'start')

def stopServiceOut(service):
    return actionwithoutTime(service, 'stop')
    
def actionwithoutTime(service, action):
    output = commands.getoutput('%s %s %s' % (SUPERVISORCTL, action, service), timeout=5)
    if "unrecognized" in output:
        return 1
    else:
        return 0  


def statusService(service):
    return actionService(service, 'status')

def command(cmd, timeout=60):  
    is_linux = platform.system() == 'Linux'  
      
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid if is_linux else None)  
    t_beginning = time.time()  
    seconds_passed = 0  
    while True:  
        if p.poll() is not None:  
            break  
        seconds_passed = time.time() - t_beginning  
        if timeout and seconds_passed > timeout:  
            if is_linux:  
                os.killpg(p.pid, signal.SIGTERM)  
            else:  
                p.terminate()  
            raise TimeoutError(cmd, timeout)  
        time.sleep(0.1)  
    return p.stdout.read()  

if __name__=='__main__':
#     lsService()
    restartService("dbass")
