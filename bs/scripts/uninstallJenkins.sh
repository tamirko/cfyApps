#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Uninstalling Jenkins..."

sudo apt-get -y -q purge sendmail
sudo apt-get -y -q purge git
sudo apt-get -y -q purge jenkins

sudo rm -rf /var/lib/jenkins


ctx logger info "${currHostName}:${currFilename} Jenkins has been uninstalled"