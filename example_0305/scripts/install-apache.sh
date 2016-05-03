#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	ctx logger info "${currHostName}:${currFilename} $2 : error code: $1"
	exit ${1}
}


function killApacheProcess {
	ps -ef | grep -iE "apache2" | grep -viE "grep|cfy|cloudify"
	if [ $? -eq 0 ] ; then 
		ps -ef | grep -iE "apache2" | grep -viE "grep|cfy|cloudify" | awk '{print $2}' | xargs sudo kill -9
	fi  
}


export PATH=$PATH:/usr/sbin:/sbin:/usr/bin || error_exit $? "Failed on: export PATH=$PATH:/usr/sbin:/sbin"


ctx logger info "${currHostName}:${currFilename} apt-get -y -q update..."
sudo apt-get -y -q update || error_exit $? "Failed on: sudo apt-get -y update"

ctx logger info "${currHostName}:${currFilename} apt-get -y -q unzip..."
sudo apt-get -y -q install unzip

#sudo /etc/init.d/apache2 stop
# Just in case the above doesn't work
ctx logger info "${currHostName}:${currFilename} Killing old apache #1 if exists..."
killApacheProcess

ctx logger info "${currHostName}:${currFilename} Removing previous php installations if exist ..."
sudo apt-get --purge -q -y remove php5* php*
sudo rm -rf  /etc/php* || error_exit $? "Failed on: sudo rm -rf  /etc/php*"
sudo rm -rf  /usr/bin/php* || error_exit $? "Failed on: sudo rm -rf  /usr/bin/php"
sudo rm -rf  /usr/share/php* || error_exit $? "Failed on: sudo rm -rf /usr/share/php"

# Removing previous apache2 installations if exist
ctx logger info "${currHostName}:${currFilename} Removing previous apache2 installations if exist ..."
sudo apt-get -y -q purge apache2.2-common apache2* || error_exit $? "Failed on: sudo apt-get -y -q purge apache2*"

# The following statements are used since in some cases, there are leftovers after uninstall
sudo rm -rf /etc/apache2 || error_exit $? "Failed on: sudo rm -rf /etc/apache2"
sudo rm -rf /usr/sbin/apache2 || error_exit $? "Failed on: sudo rm -rf /usr/sbin/apache2"
sudo rm -rf /usr/lib/apache2 || error_exit $? "Failed on: sudo rm -rf /usr/lib/apache2"
sudo rm -rf /usr/share/apache2 || error_exit $? "Failed on: sudo rm -rf /usr/share/apache2"


ctx logger info "${currHostName}:${currFilename} apt-getting install -y -q apache2 ..."
sudo apt-get install -y -q apache2 || error_exit $? "Failed on: sudo apt-get install -y -q apache2"

#sudo /etc/init.d/apache2 stop
# Just in case the above doesn't work
ctx logger info "${currHostName}:${currFilename} Killing old apache #2 if exists..."
killApacheProcess


needPhpdb=""
needPhpdb="php5-mysql"
ctx logger info "${currHostName}:${currFilename} will install ${needPhpdb} ..."

ctx logger info "${currHostName}:${currFilename} apt-getting -y -q install php5 ..."
sudo apt-get -y -q install php5 libapache2-mod-php5 php5-common php5-curl php5-cli php-pear $needPhpdb php5-gd php5-mcrypt php5-xmlrpc php5-sqlite php-xml-parser
currStat=$?
ctx logger info "${currHostName}:${currFilename} :sudo apt-getting -y -q install php5 currStat ${currStat}"

ctx logger info "${currHostName}:${currFilename} Killing old apache #3 if exist..."
killApacheProcess

apache2Location=`whereis apache2`
for i in ${apache2Location}
do    
	if [ -d "$i" ] ; then
		portsConf="$i/ports.conf"		
		if [ -f "${portsConf}" ] ; then
			ctx logger info "${currHostName}:${currFilename} portsConf is in ${portsConf}"					

			defaultFile="$i/sites-available/default"
			ctx logger info "${currHostName}:${currFilename} Replacing $origPort with $newPort in ${defaultFile}..."
			ctx logger info "${currHostName}:${currFilename} Replacing AllowOverride None with AllowOverride All in ${defaultFile}..."
			sudo sed -i -e "s/AllowOverride None/AllowOverride All/g" ${defaultFile} || error_exit $? "Failed on: sudo sed -i -e AllowOverride None/AllowOverride All in ${defaultFile}"				
			ctx logger info "${currHostName}:${currFilename} End of ${defaultFile} replacements"			
			
			ctx logger info "${currHostName}:${currFilename} :sudo a2enmod rewrite"
			sudo a2enmod rewrite
			currStat=$?
			ctx logger info "${currHostName}:${currFilename} :sudo a2enmod rewrite currStat ${currStat}"
			
			ctx logger info "${currHostName}:${currFilename} :sudo a2enmod php5"
			sudo a2enmod php5
			currStat=$?
			ctx logger info "${currHostName}:${currFilename} :sudo a2enmod php5 currStat ${currStat}"
		fi
	fi
done

ctx logger info "${currHostName}:${currFilename} End of ${currFilename}"
echo "End of ${currFilename}"




