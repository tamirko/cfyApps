#!/bin/bash -x

currHostName=`hostname`

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	echo "$2 : error code: $1"
	exit ${1}
}

export PATH=$PATH:/usr/sbin:/sbin:/usr/bin || error_exit $? "Failed on: export PATH=$PATH:/usr/sbin:/sbin"

pushd ~
export currSchema=$(ctx source node properties schemaurl)
ctx logger info "schemaurl of the source node is ${currSchema} ... "

export currLoc=`pwd`
export currZip=currZip.zip
ctx logger info "${currHostName}:$0 :Wgetting ${currSchema} to ${currLoc}/${currZip}..."

wget -O $currZip $currSchema
ctx logger info "${currHostName}:$0 :Wgot ${currSchema} to ${currLoc}/${currZip}"

type unzip
retVal=$?
ctx logger info "${currHostName}:$0 :retVal is ${retVal}..."
if [ $retVal -ne 0 ]; then
  ctx logger info "${currHostName}:$0 :Apt-getting unzip ..."
  sudo apt-get install -y -q unzip
  ctx logger info "${currHostName}:$0 :Apt-got unzip ..."
fi

ctx logger info "${currHostName}:$0 :Unzipping ${currZip} ..."
unzip -o $currZip

ctx logger info "${currHostName}:$0 :Deleting ${currZip} ..."
rm $currZip
currSQL=`ls *.sql`


dbName=$(ctx source node properties dbName)
ctx logger info "${currHostName}:$0 :Creating db ${dbName} with root..."
mysqladmin -u root create $dbName
      
dbUser=$(ctx source node properties dbUserName)
dbPassW=$(ctx source node properties dbUserPassword)


createLocalUser="CREATE USER '${dbUser}'@'localhost' IDENTIFIED BY '${dbPassW}';"
currQuery="mysql -u root ${dbName} -e ${createLocalUser}"
ctx logger info "${currHostName}:$0 :currQuery is: ${currQuery}"
queryOutput=`mysql -u root $dbName -e "${createLocalUser}"`
ctx logger info "${currHostName}:$0 :createLocalUser output is:\r\n${queryOutput}"

createGlobalUser="CREATE USER '${dbUser}'@'%' IDENTIFIED BY '${dbPassW}';"
currQuery="mysql -u root ${dbName} -e ${createGlobalUser}"
ctx logger info "${currHostName}:$0 :currQuery is: ${currQuery}"	
queryOutput=`mysql -u root $dbName -e "${createGlobalUser}"`
ctx logger info "${currHostName}:$0 :createGlobalUser output is:\r\n${queryOutput}"

grantUsageLocalUser="grant usage on *.* to ${dbUser}@localhost identified by '${dbPassW}';"
currQuery="mysql -u root ${dbName} -e ${grantUsageLocalUser}"
ctx logger info "${currHostName}:$0 :currQuery is: ${currQuery}"	
queryOutput=`mysql -u root $dbName -e "${grantUsageLocalUser}"`
ctx logger info "${currHostName}:$0 :grantUsageLocalUser output is:\r\n${queryOutput}"

grantUsageGlobalUser="grant usage on *.* to ${dbUser}@'%' identified by '${dbPassW}';"
currQuery="mysql -u root ${dbName} -e ${grantUsageGlobalUser}"
ctx logger info "${currHostName}:$0 :currQuery is: ${currQuery}"	
queryOutput=`mysql -u root $dbName -e "${grantUsageGlobalUser}"`
ctx logger info "${currHostName}:$0 :grantUsageGlobalUser output is:\r\n${queryOutput}"

grantPrivLocalUser="grant all privileges on *.* to ${dbUser}@'localhost' with grant option;"				
currQuery="mysql -u root ${dbName} -e ${grantPrivLocalUser}"
ctx logger info "${currHostName}:$0 :currQuery is: ${currQuery}"
queryOutput=`mysql -u root $dbName -e "${grantPrivLocalUser}"`
ctx logger info "${currHostName}:$0 :grantPrivLocalUser output is:\r\n${queryOutput}"

grantPrivGlobalUser="grant all privileges on *.* to ${dbUser}@'%' with grant option;"
currQuery="mysql -u root ${dbName} -e ${grantPrivGlobalUser}"
ctx logger info "${currHostName}:$0 :currQuery is: ${currQuery}"
queryOutput=`mysql -u root $dbName -e "${grantPrivGlobalUser}"`
ctx logger info "${currHostName}:$0 :grantPrivGlobalUser output is:\r\n${queryOutput}"
		
ctx logger info "${currHostName}:$0 :Importing ${currSQL} to ${dbName} with root..."
mysql -u root $dbName < $currSQL

export dbQuery=$(ctx source node properties query)
ctx logger info "${currHostName}:$0 :Running ${dbQuery} on ${dbName} with root..."

queryOutput=`mysql -u root $dbName -e "${dbQuery}"`
ctx logger info "${currHostName}:$0 :Query output is:\r\n${queryOutput}"

popd
ctx logger info "${currHostName}:$0 :End of ${currHostName}:$0"
echo "End of ${currHostName}:$0"
