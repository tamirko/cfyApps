#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Configuring Jenkins..."

pushd /var/lib/jenkins/

ctx logger info "${currHostName}:${currFilename} Downloading jenkins Config Xml..."
jenkinsConfigXml=jenkins_config.xml
ctx download-resource "config/${jenkinsConfigXml}"
find / -name "${jenkinsConfigXml}" | xargs -I file mv file config.xml

newUserName=$(ctx node properties jenkins_user_name)
ctx logger info "${currHostName}:${currFilename} Creating jenkins user (${newUserName})..."
if [ ! -d "users" ]; then
  mkdir users  
fi

cd users
newUserFirstName=$(ctx node properties jenkins_user_first_name)

mkdir $newUserName
cd $newUserName

newUserConfigXml=newuser_config.xml
ctx download-resource "config/${newUserConfigXml}"
find / -name "${newUserConfigXml}" | xargs -I file mv file config.xml
sed -i -e "s/James/$newUserFirstName/g" config.xml
sed -i -e "s/james/$newUserName/g" config.xml
cd ../..


currentEnv=Dev
ctx logger info "${currHostName}:${currFilename} Creating jenkins build (${currentEnv}) ..."
mkdir -p jobs/${currentEnv}/builds
cd jobs/${currentEnv}
devConfigXml=dev_config.xml
ctx download-resource "config/${devConfigXml}"
find / -name "${devConfigXml}" | xargs -I file mv file config.xml

cd builds
touch legacyIds
ln -s -- -1 lastFailedBuild
ln -s -- -1 lastStableBuild
ln -s -- -1 lastSuccessfulBuild
ln -s -- -1 lastUnstableBuild
ln -s -- -1 lastUnsuccessfulBuild

ctx logger info "${currHostName}:${currFilename} Chowning jenkins folders..."
cd /var/lib/jenkins/
chown -R jenkins:jenkins *
popd

myMsgFile=my.msg
ctx download-resource "config/${myMsgFile}"
find / -name "${myMsgFile}" | xargs -I file mv file ~/my.msg
jenkinsToEmail=$(ctx node properties jenkins_to_email)
sed -i -e "s/REPLACE_WITH_MAIL_ADDRESS/$jenkinsToEmail/g" ~/my.msg

ctx logger info "${currHostName}:${currFilename} Jenkins has been configured"

