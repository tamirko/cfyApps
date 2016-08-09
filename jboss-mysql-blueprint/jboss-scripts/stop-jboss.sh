#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

#tomcat_version=$(ctx node properties tomcat_version)

jboss_root_folder=$(ctx instance runtime_properties jboss_root_folder)
ctx logger info "${currHostName}:${currFilename} jboss_root_folder is ${jboss_root_folder$}"


script="${jboss_root_folder}/bin/jboss-cli.sh"
COMMAND="./${script} --connect command=:shutdown"
ctx logger info "Running ${COMMAND} ..."
nohup ${COMMAND} > /dev/null 2>&1 &

sleep 20s
ps -ef | grep -i jboss | grep -ivE "cfy|cloudify|grep|celery"

