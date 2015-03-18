#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Installing Cloudify CLI ..."

apt-get -y -q update
ctx logger info "${currHostName}:${currFilename} update ... "
apt-get install -y -q wget
ctx logger info "${currHostName}:${currFilename} wget ... "
apt-get install -y -q curl
ctx logger info "${currHostName}:${currFilename} curl ... "
apt-get install -y -q unzip
ctx logger info "${currHostName}:${currFilename} unzip ..."

apt-get install -y -q python-dev
ctx logger info "${currHostName}:${currFilename} python-dev ..."
apt-get install -y -q python-virtualenv
ctx logger info "${currHostName}:${currFilename} python-virtualenv..."
apt-get install -y -q git
ctx logger info "${currHostName}:${currFilename} git..."

export virtualEnvName=myenv
export currVersion=3.1
virtualenv $virtualEnvName
ctx logger info "${currHostName}:${currFilename}  virtualenv ... "
source $virtualEnvName/bin/activate
ctx logger info "${currHostName}:${currFilename} activate ..."
pip install cloudify==${currVersion}
ctx logger info "${currHostName}:${currFilename} pip install cloudify ..."

jenkinsLib=/var/lib/jenkins
buildScriptName=$(ctx node properties build_environments)
ctx logger info "${currHostName}:${currFilename} buildScriptName is ${buildScriptName}"
declare -a builds=($buildEnvironments)
for currentTest in "${builds[@]}"
do
  mkdir $jenkinsLib/$currentTest
done

ctx logger info "${currHostName}:${currFilename} End of Cloudify CLI installation"