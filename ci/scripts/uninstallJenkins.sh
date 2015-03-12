#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Uninstalling Jenkins..."

apt-get -y -q purge sendmail
apt-get -y -q purge git
apt-get -y -q purge jenkins

rm -rf /var/lib/jenkins


ctx logger info "${currHostName}:${currFilename} Jenkins has been uninstalled"