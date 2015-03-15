#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")



cliJar=`find / -name "jenkins-cli.jar"`

userName=$(ctx node properties jenkins_user_name)
ctx logger info "${currHostName}:${currFilename} :userName ${userName}"
userPassw=$(ctx node properties jenkins_user_passw)
java -jar $cliJar -s http://localhost:8080/ login --username $userName --password $userPassw

currCmd=$1
ctx logger info "${currHostName}:${currFilename} Running Jenkins cmd : ${currCmd} ..."
java -jar $cliJar -s http://localhost:8080/ $currCmd


currentDate=`date`
msgID=`date|md5sum|cut -c -10`
currMsgFile=my${msgID}.msg
cp ~/my.msg $currMsgFile
sed -i -e "s/REPLACE_WITH_SUBJECT/Jenkins ran $currCmd $currentDate/g" $currMsgFile
sed -i -e "s/REPLACE_WITH_BODY/Cloudify ran Jenkins ${currCmd}/g" $currMsgFile

ctx logger info "${currHostName}:${currFilename} Sending an email from Jenkins - Cloudify ran Jenkins ${currCmd} ..."

java -jar $cliJar -s http://localhost:8080/ mail < $currMsgFile

java -jar $cliJar -s http://localhost:8080/ logout
rm $currMsgFile

ctx logger info "${currHostName}:${currFilename} End of run-jenkins-cmd"


exit 

java -jar $cliJar -s http://localhost:8080/ build JOB_NAME -p KEY1=VAL1 -p KEY2=VAL2 -p KEY3=VAL3



