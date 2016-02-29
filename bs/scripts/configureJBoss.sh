#!/bin/bash

ctx logger info "Running $0 ..."
ctx logger info "pwd is `pwd` "
ctx logger info "id is `id` "

sudo yum -y -q install wget
sudo yum -y -q install curl

currHostName=`hostname`
ctx logger info "currHostName is $currHostName"
ctx logger info "Adding $currHostName to /etc/hosts"
sudo sed -i -e "s+\(127.0.0.1.*\)\(localhost \)\(.*\)+\1$currHostName \2\3+g" /etc/hosts
currStatus=$?
ctx logger info "Tried to add $currHostName to /etc/hosts. - Action status is ${currStatus}"

cd ~
ctx logger info "pwd2 is `pwd` "

jboss_ip_address=$(ctx instance host_ip)
ctx logger info "jboss_ip_address is $jboss_ip_address"

java_rpm_url=$(ctx node properties java_rpm_url)
ctx logger info "java_rpm_url is $java_rpm_url"
sudo rpm -i $java_rpm_url
currStatus=$?
ctx logger info "$java_rpm_url install status is ${currStatus}"

JBoss_download_url=$(ctx node properties JBoss_download_url)
jbossFileName=$(basename "$JBoss_download_url")
jbossHomeDir=${jbossFileName%.*}
if [ ! -f "$jbossFileName" ]; then
    ctx logger info  "$jbossFileName does not exist. Downloading it from ${JBoss_download_url}..."
    wget ${JBoss_download_url}
    currStatus=$?
    ctx logger info  "Done downloading $JBoss_download_url - previous action status is ${currStatus}"
    unzip
    if [ $? -gt 0 ]; then
        ctx logger info  "Unzip doesn't exist. Installing it ..."
        sudo yum -y -q install unzip
        currStatus=$?
        ctx logger info  "Done installing it unzip - previous action status is ${currStatus}"
    fi
    sudo unzip $jbossFileName
    currStatus=$?
    ctx logger info  "Done unzipping $jbossFileName - previous action status is ${currStatus}"
else
    ctx logger info  "JBoss is already installed"
fi


application_war_url=$(ctx node properties application_war_url)
ctx logger info "application_war_url is $application_war_url"
war_filename=$(basename "$application_war_url")
wget ${application_war_url}
deployments_folder=$jbossHomeDir/standalone/deployments/
ctx logger info "Moving $war_filename to ${deployments_folder} ..."
sudo mv $war_filename ${deployments_folder}
currStatus=$?
ctx logger info  "sudo mv $war_filename ${deployments_folder} - Action status is ${currStatus}"

ctx logger info "End of $0"

