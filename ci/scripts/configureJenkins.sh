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

devConfigXml=dev_config.xml
ctx download-resource "config/${devConfigXml}"
buildXml=`find / -name "${devConfigXml}"`

declare -a builds=("AB1stTest" "AB2ndTest")

ctx logger info "${currHostName}:${currFilename} Iterating on the ${#builds[*]} environments : ${builds[*]}"

buildScriptName=$(ctx node properties build_script)
ctx logger info "${currHostName}:${currFilename} buildScriptName is ${buildScriptName)"
ctx download-resource "config/${buildScriptName}"
buildScriptPath=`find / -name "${buildScriptName}"`

jenkinsLib=/var/lib/jenkins
ctx logger info "${currHostName}:${currFilename} Copying $buildScriptName to $jenkinsLib ..."
cp $buildScriptPath ${jenkinsLib}/ 
chmod +x ${jenkinsLib}/$buildScriptName

for currentTest in "${builds[@]}"
do
  pushd $jenkinsLib
  ctx logger info "${currHostName}:${currFilename} Creating jenkins build (${currentTest}) ..."
      
  mkdir -p jobs/${currentTest}/builds
  cd jobs/${currentTest}   
  cp $buildXml config.xml
  sed -i -e "s+SCRIPT+$jenkinsLib/$buildScriptName+g" config.xml 
  sed -i -e "s/ARG1/$currentTest/g" config.xml

  cd builds
  touch legacyIds
  ln -s -- -1 lastFailedBuild
  ln -s -- -1 lastStableBuild
  ln -s -- -1 lastSuccessfulBuild
  ln -s -- -1 lastUnstableBuild
  ln -s -- -1 lastUnsuccessfulBuild
  popd
done  

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

