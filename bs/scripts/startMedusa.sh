#!/bin/bash

ctx logger info "Running $0 ..."
ctx logger info "pwd is `pwd` "
ctx logger info "id is `id` "

cd ~
ctx logger info "pwd2 is `pwd` "
ctx logger info "hostname is `hostname` "
JBoss_download_url=$(ctx node properties JBoss_download_url)
jbossFileName=$(basename "$JBoss_download_url")
jbossHomeDir=${jbossFileName%.*}
cd $jbossHomeDir/bin
currStatus=$?
ctx logger info "Starting JBoss in $jbossHomeDir/bin... - previous action status is ${currStatus}"

nohup sudo ./standalone.sh -Djboss.bind.address=0.0.0.0 -Djboss.bind.address.management=0.0.0.0 > ~/jboss_start.log 2>&1 &
currStatus=$?
ctx logger info "Ran nohup sudo ./standalone.sh - previous action status is ${currStatus}"
ctx logger info "End of $0"

