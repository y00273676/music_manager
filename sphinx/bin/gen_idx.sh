#!/bin/sh

[ $# -lt 1 ] && { echo -e "Usage:\n \t$0 index_name1 index_name2 ...\n"; exit 1; }

WorkDir="/usr/local/coreseek"
IdxDir=$WorkDir"/var/data"
CONF_FILE="etc/searchd_9312.conf"

if [ ! -d "$IdxDir" ]; then
    mkdir $IdxDir; [ $? -ne 0 ] && { echo "mkdir $IdxDir failed"; exit -1; }
    chown root:root $IdxDir; [ $? -ne 0 ] && { echo "chonw $IdxDir failed"; exit -1; }
fi

cd $WorkDir
[ ! -f "$WorkDir/$CONF_FILE" ] && { echo "$WorkDir/$CONF_FILE do not exist"; exit -1; }
for idx in $@
do
    echo "bin/indexer -c $CONF_FILE $idx --rotate > var/log/${idx}.log 2>&1 &"
    bin/indexer -c $CONF_FILE $idx --verbose --rotate > var/log/${idx}.log 2>&1 &
done
