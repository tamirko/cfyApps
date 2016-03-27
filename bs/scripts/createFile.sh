#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")
currentDate=`date`

ctx logger info "${currHostName}:${currFilename} Start ... "
DPLID=$(ctx deployment id)
ctx logger info "${currHostName}:${currFilename} deployment id is ${DPLID}"

export file_name_to_create=$1
ctx logger info "${currHostName}:${currFilename} About to create ${file_name_to_create} ... "
ctx logger info "${currHostName}:${currFilename} pwd is `pwd` "
touch ~/$file_name_to_create
currStatus=$?
ctx logger info "${currHostName}:${currFilename} action status: $currStatus"

ctx logger info "${currHostName}:${currFilename} End"

exit

# This command will create a file named "file1" in the VM of the JBOSS_AFP_APPLICATION :
cfy executions start -d $dep -w create_new_File -p '{"file_name":"file1","input_str":"JBOSS_AFP_APPLICATION","input_type":"name"}'

# This command will create a file named "file2" in all the VMs that contain a JBoss whose Cloudify type is JBossApplicationServer :
cfy executions start -d $dep -w create_new_File -p '{"file_name":"file2","input_str":"JBossApplicationServer","input_type":"type"}'


