#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")
currentDate=`date`

ctx logger info "${currHostName}:${currFilename} Start ... "
DPLID=$(ctx deployment id)
ctx logger info "${currHostName}:${currFilename} Deployment id is ${DPLID}"

export security_update_number=$1
ctx logger info "${currHostName}:${currFilename} About to run security update: ${security_update_number} ... "
ctx logger info "${currHostName}:${currFilename} Current working directory is `pwd` "
touch ~/$security_update_number
currStatus=$?
ctx logger info "${currHostName}:${currFilename} action status: $currStatus"

ctx logger info "${currHostName}:${currFilename} End"

exit

# This command will perform security update "SU1355ASD" in the VM of the JBOSS_AFP_APPLICATION :
cfy executions start -d $dep -w security_update -p '{"security_update_number":"SU1355ASD","input_str":"JBOSS_AFP_APPLICATION","input_type":"name"}' -l

# This command will perform security update "SU981155TR" in all the VMs that contain a JBoss whose Cloudify type is JBossApplicationServer :
cfy executions start -d $dep -w security_update -p '{"security_update_number":"SU981155TR","input_str":"JBossApplicationServer","input_type":"type"}' -l


