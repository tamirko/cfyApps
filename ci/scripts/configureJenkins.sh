#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Configuring Jenkins..."

pushd /var/lib/jenkins/

ctx logger info "${currHostName}:${currFilename} Downloading jenkins Config Xml..."
jenkinsConfigXml=jenkins_config.xml
jenkinsConfigXmlPath=$(ctx download-resource "config/${jenkinsConfigXml}")
ctx logger info "${currHostName}:${currFilename} jenkinsConfigXmlPath downloaded to ${jenkinsConfigXmlPath}"
mv $jenkinsConfigXmlPath config.xml

newUserName=$(ctx node properties jenkins_user_name)
ctx logger info "${currHostName}:${currFilename} Creating jenkins user (${newUserName})..."
if [ ! -d "users" ]; then
  mkdir users  
fi

cd users
newUserFirstName=$(ctx node properties jenkins_user_first_name)
ctx logger info "${currHostName}:${currFilename} newUserFirstName is ${newUserFirstName}" 
mkdir -p $newUserName
cd $newUserName

newUserConfigXml=newuser_config.xml
ctx logger info "${currHostName}:${currFilename} Downloading ${newUserConfigXml}..."
newUserConfigXmlPath=$(ctx download-resource "config/${newUserConfigXml}")
ctx logger info "${currHostName}:${currFilename} newUserConfigXmlPath downloaded to ${newUserConfigXmlPath}"
mv $newUserConfigXmlPath config.xml
sed -i -e "s/James/$newUserFirstName/g" config.xml
sed -i -e "s/james/$newUserName/g" config.xml
cd ../..

export devConfigXml=dev_config.xml
ctx logger info "${currHostName}:${currFilename} Downloading ${devConfigXml}..."
devBuildXml=$(ctx download-resource "config/${devConfigXml}")
ctx logger info "${currHostName}:${currFilename} devBuildXml downloaded to ${devBuildXml}"

export buildEnvironments=$(ctx node properties build_environments)
ctx logger info "${currHostName}:${currFilename} buildEnvironments are ${buildEnvironments}"
declare -a builds=($buildEnvironments)

ctx logger info "${currHostName}:${currFilename} Iterating on the ${#builds[*]} environments : ${builds[*]}"

export devManagerIPs=$(ctx node properties cfy_managers)
ctx logger info "${currHostName}:${currFilename} devManagerIPs are ${devManagerIPs}"
declare -a devIPs=($devManagerIPs)

export buildScriptName=$(ctx node properties build_script)
ctx logger info "${currHostName}:${currFilename} buildScriptName is ${buildScriptName}"
buildScriptPath=$(ctx download-resource "config/${buildScriptName}")
ctx logger info "${currHostName}:${currFilename} buildScriptPath is ${buildScriptPath}"

export appJsonName=app.json
export origJppJsonPath=$(ctx download-resource "config/${appJsonName}")
ctx logger info "${currHostName}:${currFilename} origJppJsonPath is ${origJppJsonPath}"


export sshItemID=$(ctx node properties ssh_keys)
# Comment this line later
ctx logger info "${currHostName}:${currFilename} sshItemID is ${sshItemID}"

export privateVlan=$(ctx node properties private_vlan)
# Comment this line later
ctx logger info "${currHostName}:${currFilename} privateVlan is ${privateVlan}"


jenkinsLib=/var/lib/jenkins
ctx logger info "${currHostName}:${currFilename} Copying $buildScriptName to $jenkinsLib ..."
cp -f $buildScriptPath ${jenkinsLib}/ 
chmod +x ${jenkinsLib}/$buildScriptName

export appJsonPath=${jenkinsLib}/${appJsonName}
cp $origJppJsonPath $appJsonPath
sed -i -e "s/REPLACE_WITH_SSH_SL_ITEM_ID/$sshItemID/g" $appJsonPath
sed -i -e "s/REPLACE_WITH_VLAN_ITEM_ID/$privateVlan/g" $appJsonPath

function createBuildEnv {
  
  currentTest=$1
  buildXml=$2
  mngrIP=$3
  pushd $jenkinsLib
  ctx logger info "${currHostName}:${currFilename} Creating jenkins build (${currentTest}) ..."
  ctx logger info "${currHostName}:${currFilename} Creating jenkins buildXml (${buildXml}) ..."
  ctx logger info "${currHostName}:${currFilename} Creating jenkins mngrIP (${mngrIP}) ..."
      
  mkdir -p jobs/${currentTest}/builds
  cd jobs/${currentTest}
  ctx logger info "${currHostName}:${currFilename} Copying ${buildXml} to config.xml ... "
  cp $buildXml config.xml
  sed -i -e "s+SCRIPT+$jenkinsLib/$buildScriptName+g" config.xml
  sed -i -e "s/ENV_NAME/$currentTest/g" config.xml
  sed -i -e "s/MANAGER_IP/$mngrIP/g" config.xml
  #midDomainName=`echo $currentTest | tr [A-Z] [a-z]`
  #sed -i -e "s/REPLACE_WITH_MID_DOMAIN_NAME/$midDomainName/g" config.xml
  #sed -i -e "s/REPLACE_WITH_SSH_SL_ITEM_ID/$sshItemID/g" config.xml  
  #sed -i -e "s/REPLACE_WITH_VLAN_ITEM_ID/$privateVlan/g" config.xml  
                                            
  cd builds
  touch legacyIds
  ln -s -- -1 lastFailedBuild
  ln -s -- -1 lastStableBuild
  ln -s -- -1 lastSuccessfulBuild
  ln -s -- -1 lastUnstableBuild
  ln -s -- -1 lastUnsuccessfulBuild
  popd
}

# iterate on env and ips (devIPs) by index
for index in ${!builds[*]}
do
  currentTest=${builds[$index]}
  testManagerIP=${devIPs[$index]}
  createBuildEnv $currentTest $devBuildXml $testManagerIP
done  

export prodConfigXml=prod_config.xml
ctx logger info "${currHostName}:${currFilename} Downloading ${prodConfigXml}..."
export prodBuildXml=$(ctx download-resource "config/${prodConfigXml}")
ctx logger info "${currHostName}:${currFilename} prodBuildXml downloaded to ${prodBuildXml}"

productionEnv=$(ctx node properties prod_environment)
prodManagerIP=$(ctx node properties prod_mngr_ip)

createBuildEnv $productionEnv $prodBuildXml $prodManagerIP

ctx logger info "${currHostName}:${currFilename} Chowning jenkins folders..."
cd /var/lib/jenkins/
chown -R jenkins:jenkins *
popd

myMsgFile=my.msg
myMsgFilePath=$(ctx download-resource "config/${myMsgFile}")
ctx logger info "${currHostName}:${currFilename} myMsgFilePath downloaded to ${myMsgFilePath}"
mv $myMsgFilePath ~/my.msg

jenkinsToEmail=$(ctx node properties jenkins_to_email)
sed -i -e "s/REPLACE_WITH_MAIL_ADDRESS/$jenkinsToEmail/g" ~/my.msg

ctx logger info "${currHostName}:${currFilename} Jenkins has been configured"

