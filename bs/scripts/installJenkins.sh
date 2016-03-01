#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "currHostName is $currHostName"
ctx logger info "Adding $currHostName to /etc/hosts"
set +e
sudo sed -i -e "s+\(127.0.0.1\)\([ ]*\)\(localhost.*\)+\1\2$currHostName \3+g" /etc/hosts
currStatus=$?
ctx logger info "Tried to add $currHostName to /etc/hosts. - Action status is ${currStatus}"
set -e

sudo chmod -R 777 /etc/apt/sources.list.d
currStatus=$?
ctx logger info "Tried to chmod -R 777 /etc/apt/sources.list.d. - Action status is ${currStatus}"

sudo apt-get -y -q --force-yes install wget
currStatus=$?
ctx logger info "Ran sudo apt-get -y -q --force-yes install wget - Action status is ${currStatus}"

sudo apt-get -y -q --force-yes install curl
currStatus=$?
ctx logger info "Ran sudo apt-get -y -q --force-yes install curl - Action status is ${currStatus}"

ctx logger info "${currHostName}:${currFilename} Getting jenkins-ci.org.key..."

wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
currStatus=$?
ctx logger info "Ran wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key ... sudo apt-key add - Action status is ${currStatus}"

echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list
currStatus=$?
ctx logger info "Ran deb http://pkg.jenkins-ci.org/debian binary/ /etc/apt/sources.list.d/jenkins.list ... - Action status is ${currStatus}"

sudo apt-get --force-yes update
currStatus=$?
ctx logger info "Ran sudo apt-get --force-yes update - Action status is ${currStatus}"

sudo apt-get -y --force-yes clean
currStatus=$?
ctx logger info "Ran sudo apt-get -y --force-yes clean - Action status is ${currStatus}"

set +e
sudo apt-get purge -y --force-yes jenkins-common
currStatus=$?
ctx logger info "Ran sudo apt-get purge -y --force-yes jenkins-common - Action status is ${currStatus}"
set -e

sudo apt-get install -y -q --force-yes jenkins
currStatus=$?
ctx logger info "Ran sudo apt-get install -y -q --force-yes jenkins - Action status is ${currStatus}"

ctx logger info "${currHostName}:${currFilename} Installing git..."
sudo apt-get install -y -q --force-yes git
currStatus=$?
ctx logger info "Ran sudo apt-get install -y -q --force-yes git - Action status is ${currStatus}"

ctx logger info "${currHostName}:${currFilename} Installing sendmail..."
sudo apt-get install -y -q --force-yes sendmail
currStatus=$?
ctx logger info "Ran sudo apt-get install -y -q --force-yes sendmail - Action status is ${currStatus}"

sudo chmod -R 755 /etc/apt/sources.list.d
currStatus=$?
ctx logger info "Tried to chmod -R 755 /etc/apt/sources.list.d. - Action status is ${currStatus}"

sudo service jenkins stop
currStatus=$?
ctx logger info "Ran sudo nohup service jenkins stop - Action status is ${currStatus}"

