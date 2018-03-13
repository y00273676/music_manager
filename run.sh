#!/bin/bash 
bak_tmp=/data/tmp/
bak_dir=/data/mysqlbak/

# yishunli@thunder.com.cn:
#we need to stop mysql when back db, while the service stop may broken 
#  twm's initial connection(also db initialize).
#To solve this conflict, we inject the 'dbbackup' code before twm manager
#remember to restart other services which depends on mysql db ( say, dbass etc...)

day_files=3
week_files=4

mkdir -p $bak_tmp
mkdir -p $bak_dir
#mkdir -p $week_dir

chk_err()
{
  ret=$?
  if [ -z "$1" ];then
    msg="unspecified"
  else
    msg="$1"
  fi
  if [ $ret -ne 0 ];then
    echo "Failed: $msg"
  else
    echo "Success: $msg"
  fi
}

stop_mysql()
{
  systemctl stop mysql
  pid=`ps aux | grep mysqld | grep datadir | awk '{print $2}'`
  echo "mysqld pid: $pid"
  kill -15 $pid
  sleep 3
  ps aux | grep mysqld 
}

start_mysql()
{
  systemctl start mysql
}

sync_db_slaveserver()
{
  #should do this in cron jobs:
  docker exec -t thunder rsync -av $master_ip:$bak_dir/ $bak_dir
}

backup_db()
{
  t_date=`date "+%Y-%m-%d"`
  t_year=`date "+%Y"`
  t_weeks=`date "+%Y-%W"`
  dbf="mysql-$t_date.tar.gz"
  wbf="mysql-$t_weeks.tar.gz"

  if [ -f $bak_dir/$dbf ];then
    echo "no need backup again"
    return 0
  fi

  echo "Stopping mysql services..."
  stop_mysql
  cd /var/lib && tar zcf $bak_tmp/$dbf mysql
  chk_err "backup mysql db files to $bak_tmp/$dbf"
  md5=$(md5sum $bak_tmp/$dbf | awk '{print $1}')
  chk_err "generate md5 info $bak_tmp/$dbf"
  mv $bak_tmp/$dbf $bak_dir/$dbf
  chk_err "move to backup dir $bak_dir/$dbf"
  echo "$md5  $dbf" >> $bak_dir/md5sum.txt
  chk_err "write down the md5 info $md5"
  if [ ! -e $bak_dir/$wbf ]; then
    ln -f $bak_dir/$dbf $bak_dir/$wbf
    echo "$md5  $wbf" >> $bak_dir/md5sum.txt
  fi
  #Already have backup for today
  echo "Starting mysql services..."
  start_mysql
  clean_old_file
  #Since we restarted the mysqld, restart services also
  supervisorctl restart dbass
  #make sure videoserver get the lunbo list
  supervisorctl restart video
  #recog/stbmodule service also needs db service
  supervisorctl restart recog
  supervisorctl restart stbmodule
}

clean_old_file()
{
  #clean daily backup 
  i=1
  for file in `ls -t $bak_dir/mysql-????-??-??.tar.gz`
  do
    if [ $i -gt $day_files ]
    then
        rm -f $file
        echo "cleanning $file"
    fi
    i=`expr $i + 1`
  done

  #clean weekly backup 
  i=1
  for file in `ls -t $bak_dir/mysql-????-??.tar.gz`
  do
    if [ $i -gt $week_files ]
    then
        rm -f $file
        echo "cleanning $file"
    fi
    i=`expr $i + 1`
  done

  tmpfile=`mktemp`
  #Filter out useless md5sum info:
  echo > $tmpfile
  while read line
  do
    file=`echo $line | awk '{print $2}'`
    if [ -e $bak_dir/$file ];then
      echo $line >> $tmpfile
    fi
  done < $bak_dir/md5sum.txt
  mv $tmpfile $bak_dir/md5sum.txt
 
}

read_config() {
  INIFILE=/opt/thunder/thunder.ini
  SECTION=$1
  ITEM=$2
  _readIni=`awk -F '=' '/\['$SECTION'\]/{a=1}a==1&&$1~/'$ITEM'/{print $2;exit}' $INIFILE`
  echo ${_readIni}
}

back_db_main()
{
    up=`cat /proc/uptime | awk -F'.' '{print $1}'`
    #if not in just bootup, don't backup the db, we may do upgrading now.
    if [ $up -gt 600 ]
    then
        echo "Not in booting process, ignore the db backup"
        return
    fi
    #Try to backup mysql db at first
    #db_ip=`cat /opt/thunder/thunder.ini | grep "DataBaseServerIp" | awk -F'=' '{print $2}'`
    echo "Checking whether we need to backup mysql db..."
    db_ip=$(read_config "MainServer" "DataBaseServerIp")
    db_ip=`echo $db_ip | sed -e "s/\r//g" | sed -e "s/\n//g"`
    echo "dbip: ($db_ip)"
    echo $db_ip | grep -q "^127.0"
    if [ $? -eq 0 ]
    then
        echo "Warning: main db server not configured yet. Do nothing!"
        return 0
    fi
    ip addr show | grep -q "$db_ip/"
    if [ $? -ne 0 ]
    then
      echo "main db ip($db_ip)"
      echo "Warning: not running on main db server. Do nothing!"
      return 0
    fi
    echo "call backup mysql db"
    backup_db
}


Set_MediaIndex()
{
    up_secs=`cat /proc/uptime | awk -F'.' '{print $1}'`
    if [ $up_secs -gt 600 ]
    then
        echo "Not in boot up sphase, skip SetMediaIndex"
        return
    fi
    sleep 3
    echo "call sp_SetMediaIndex()"
    i=1
    while [ $i -lt 10 ]
    do
        mysql -h 127.0.0.1 -uroot -pThunder#123 karaok -e "call sp_SetMediaIndex()"
        ret=$?
        echo "$i, call sp_SetMediaIndex() returns: $ret"
        if [ $ret -eq 0 ]
        then
            echo "${i}th call sp_SetMediaIndex() success, will restart dbass."
            supervisorctl restart dbass
            return
            i=20
        else
            i=`expr $i + 1`
            sleep 1
        fi
    done
    echo "Failed to run sp_SetMediaIndex() after $i retries"
}


back_db_main
Set_MediaIndex
#Start twm console at finnal
cd /opt/thunder/twm
exec python /opt/thunder/twm/initweb.py --port=8888 --debug=False --log_file_prefix=/opt/logs/twm.log
