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

ctx logger info "Stopping JBoss in $jbossHomeDir/bin..."
ctx logger info "Running sudo ./jboss-cli.sh --connect command=:shutdown ..."
sudo ./jboss-cli.sh --connect command=:shutdown

ctx logger info "End of $0"

