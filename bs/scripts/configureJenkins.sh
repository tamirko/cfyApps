#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Configuring Jenkins..."

pushd /var/lib/jenkins/
currStatus=$?

ctx logger info "${currHostName}:${currFilename} Downloading jenkins Config Xml..."
jenkinsConfigXml=jenkins_config.xml
jenkinsConfigXmlPath=$(ctx download-resource "config/${jenkinsConfigXml}")
ctx logger info "${currHostName}:${currFilename} jenkinsConfigXmlPath downloaded to ${jenkinsConfigXmlPath}"
sudo mv $jenkinsConfigXmlPath config.xml

newUserName=$(ctx node properties jenkins_user_name)
ctx logger info "${currHostName}:${currFilename} Creating jenkins user (${newUserName})..."
if [ ! -d "users" ]; then
  sudo mkdir -p users
  currStatus=$?
  ctx logger info "${currHostName}:${currFilename} Ran mkdir -p users - Action status is ${currStatus}"
fi

cd users
newUserFirstName=$(ctx node properties jenkins_user_first_name)
ctx logger info "${currHostName}:${currFilename} newUserFirstName is ${newUserFirstName}" 
sudo mkdir -p $newUserName
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran mkdir -p $newUserName - Action status is ${currStatus}"
cd $newUserName

newUserConfigXml=newuser_config.xml
ctx logger info "${currHostName}:${currFilename} Downloading ${newUserConfigXml}..."
newUserConfigXmlPath=$(ctx download-resource "config/${newUserConfigXml}")
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran ctx download-resource config/${newUserConfigXml} - Action status is ${currStatus}"
ctx logger info "${currHostName}:${currFilename} newUserConfigXmlPath downloaded to ${newUserConfigXmlPath}"
sudo mv $newUserConfigXmlPath config.xml

sudo sed -i -e "s/James/$newUserFirstName/g" config.xml
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran sudo sed -i -e James $newUserFirstName g config.xml - Action status is ${currStatus}"

sudo sed -i -e "s/james/$newUserName/g" config.xml
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran sudo sed -i -e james $newUserName g config.xml - Action status is ${currStatus}"

cd ../..

export buildScriptName=$(ctx node properties build_script)
ctx logger info "${currHostName}:${currFilename} buildScriptName is ${buildScriptName}"
buildScriptPath=$(ctx download-resource "config/${buildScriptName}")
ctx logger info "${currHostName}:${currFilename} buildScriptPath is ${buildScriptPath}"

jenkinsLib=/var/lib/jenkins
ctx logger info "${currHostName}:${currFilename} Copying $buildScriptName to $jenkinsLib ..."
sudo cp -f $buildScriptPath ${jenkinsLib}/
ctx logger info "${currHostName}:${currFilename} Ran sudo cp -f $buildScriptPath ${jenkinsLib}/ - Action status is ${currStatus}"

sudo chmod +x ${jenkinsLib}/$buildScriptName
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran sudo chmod +x ${jenkinsLib}/$buildScriptName - Action status is ${currStatus}"

ctx logger info "${currHostName}:${currFilename} Chowning jenkins folders..."
cd /var/lib/jenkins/
sudo chown -R jenkins:jenkins *
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran sudo chown -R jenkins:jenkins * - Action status is ${currStatus}"

popd

myMsgFile=my.msg
myMsgFilePath=$(ctx download-resource "config/${myMsgFile}")
ctx logger info "${currHostName}:${currFilename} myMsgFilePath downloaded to ${myMsgFilePath}"
mv $myMsgFilePath ~/my.msg
currStatus=$?
ctx logger info "${currHostName}:${currFilename} Ran mv $myMsgFilePath ... my.msg - Action status is ${currStatus}"


jenkinsToEmail=$(ctx node properties jenkins_to_email)
sed -i -e "s/REPLACE_WITH_MAIL_ADDRESS/$jenkinsToEmail/g" ~/my.msg

ctx logger info "${currHostName}:${currFilename} Jenkins has been configured"

