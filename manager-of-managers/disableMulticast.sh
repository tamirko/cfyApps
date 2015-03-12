#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ymlPath=`find / -name "elasticsearch.yml" | grep config`
ctx logger info "${currHostName}:${currFilename} ${disableMulticast} : disabling multicast in ${ymlPath} ..."

cp $ymlPath ~/
echo 'discovery.zen.ping.multicast.port: 54329' >> $ymlPath
service elasticsearch restart 

lsl=`ls -l ~/`

ctx logger info "${currHostName}:${currFilename} End of lsl is ${lsl} ..."
ctx logger info "${currHostName}:${currFilename} End of ${disableMulticast} ..."

