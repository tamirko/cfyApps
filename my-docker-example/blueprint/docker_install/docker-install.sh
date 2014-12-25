#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} installing curl just in case ..."
apt-get install -y -q curl

curl -s https://raw.githubusercontent.com/cloudify-cosmo/cloudify-docker-plugin/master/docker_installation/resources/install_docker.sh | bash
ctx logger info "${currHostName}:${currFilename} Installing docker ..."

ctx logger info "${currHostName}:${currFilename} :End of ${currHostName}:$0"
echo "End of ${currHostName}:$0"
