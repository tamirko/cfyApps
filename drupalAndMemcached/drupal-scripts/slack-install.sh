#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

documentRoot=$(ctx node properties docRoot)
ctx logger info "${currHostName}:${currFilename} :documentRoot ${documentRoot}"

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	echo "$2 : error code: $1"
	exit ${1}
}

sitesFolder="${documentRoot}/sites"
pushd $sitesFolder


drush en -y entity entity_token rules rules_admin

drush dis -y overlay

modules="slack features"
for currModule in `echo $modules`; do
  ctx logger info "${currHostName}:${currFilename} Invoking drush dl ${currModule}"
  drush dl ${currModule}
  currStatus=$?
  ctx logger info "${currHostName}:${currFilename} Invoked drush dl ${currModule} - currStatus is ${currStatus}"
  ctx logger info "${currHostName}:${currFilename} Invoking drush en -y ${currModule}"
  drush en -y ${currModule}
  currStatus=$?
  ctx logger info "${currHostName}:${currFilename} Invoked drush en -y ${currModule} - currStatus is ${currStatus}"
done

slackRule1Url=$(ctx node properties slackRule1Url)
slackRule1ModuleName=$(ctx node properties slackRule1ModuleName)
slackRule1TarFile=rule1.tar

currStatus=$?
ctx logger info "${currHostName}:${currFilename} slackRule1Url is ${slackRule1Url}"
ctx logger info "${currHostName}:${currFilename} slackRule1ModuleName is ${slackRule1ModuleName}"
ctx logger info "${currHostName}:${currFilename} slackRule1TarFile is ${slackRule1TarFile}"


pushd all/modules
wget -O ${slackRule1TarFile} ${slackRule1Url}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} wget -O ${slackRule1TarFile} ${slackRule1Url} - currStatus is ${currStatus}"
tar -xvf ${slackRule1TarFile}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} tar -xvf ${slackRule1TarFile} - currStatus is ${currStatus}"
rm ${slackRule1TarFile}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} rm ${slackRule1TarFile} - currStatus is ${currStatus}"
popd

drush en -y ${slackRule1ModuleName}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} drush en -y ${slackRule1ModuleName} - currStatus is ${currStatus}"

# Set the site name to deployment ID
deployment_id=$(ctx deployment id)
drush vset site_name ${deployment_id} --always-set

ctx logger info "${currHostName}:${currFilename} Invoking drush cc all ..."
drush cc all
popd 

ctx logger info "${currHostName}:${currFilename} :End of ${currHostName}:${currFilename}"
echo "End of ${currHostName}:${currFilename}"


exit

export dep=myDeployment
export myTheme=mayo
cfy executions start -d $dep  -w drush_install -p "project_name=${myTheme}"

This is how you invoke it from the drush_setvar workflow from the CFY CLI :

cfy executions start -d $dep  -w drush_setvar -p "variable_name=theme_default;variable_value=${myTheme}"