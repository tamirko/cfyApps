#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

envName=$1
echo "${currHostName}:${currFilename} Jenkins build ${envName}..."

if [ "${currentTask}" == "dummy" ]; then
  if [[ "${envName}" =~ "1stTest" ]]; then
    currentTheme="bluez"
  else
    currentTheme="selecta"
  fi
  msgID=`date|md5sum|cut -c -10`
  newDir=/tmp/tamir${envName}${msgID}  
else
  currentTheme=${currentTask}
  newDir=/tmp/tamir${envName}$currentTask
fi


echo "${currHostName}:${currFilename} Jenkins creating ${newDir}"
mkdir -p ${newDir}

echo "${currHostName}:${currFilename} Jenkins currentTheme is ${currentTheme}"

managerIP=$2
cfy --v
cfy use -t $managerIP
cfy deployments list

echo "${currHostName}:${currFilename} Jenkins orig app.json is:"
cat app.json

midDomainName=`echo $envName | tr [A-Z] [a-z]`
newAppJson=app${midDomainName}.json
cp -f app.json $newAppJson

sed -i -e "s/REPLACE_WITH_MID_DOMAIN_NAME/$midDomainName/g" $newAppJson

echo "${currHostName}:${currFilename} Jenkins newAppJson is:"
cat $newAppJson

echo "${currHostName}:${currFilename} End of Jenkins build $1"
