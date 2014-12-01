#!/bin/bash -x

currHostName=`hostname`
currFilename=$(basename "$0")

documentRoot=$(ctx source node properties docRoot)
ctx logger info "${currHostName}:${currFilename} :documentRoot ${documentRoot}"

dbPort=$(ctx target node properties port)
ctx logger info "xxx memcache ? ${currHostName}:${currFilename} :dbPort ${dbPort}"
ctx logger info "xxx memcache need to add iterations over all instances ports"

dbHost=$(ctx target instance host_ip)
ctx logger info "xxx memcache ? ${currHostName}:${currFilename} :dbHost ${dbHost}"
ctx logger info "xxx memcache need to add iterations over all instances host ips"


# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	echo "$2 : error code: $1"
	exit ${1}
}


export PATH=$PATH:/usr/sbin:/sbin || error_exit $? "Failed on: export PATH=$PATH:/usr/sbin:/sbin"

sitesFolder="${documentRoot}/sites"
drupalDefaultFolder="${sitesFolder}/default"

drupalDefaultSettingsFilePath="${drupalDefaultFolder}/default.settings.php"
drupalSettingsFilePath="${drupalDefaultFolder}/settings.php"

pushd $drupalDefaultFolder
drush dl memcache
drush en -y memcache,memcache_admin
currPWD=`pwd`
echo "xxx currPWD is ${currPWD}"
ctx logger info "${currHostName}:${currFilename} xxx currPWD is ${currPWD}"

memcacheSettings="memcache_settings.php"
cp memcache_template_for_settings.php $memcacheSettings
sed -i -e "s%MEMCACHE_HOST_IP\:MEMCACHE_PORT%$dbHost\:$dbPort%g" $memcachesettings
cat $memcacheSettings >> $drupalSettingsFilePath
 	
ctx logger info "${currHostName}:${currFilename} Clearing cache"
drush cc all
popd
	
ctx logger info "${currHostName}:${currFilename} :End of ${currHostName}:$0"
echo "End of ${currHostName}:$0"
