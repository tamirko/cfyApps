#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Starting Jenkins..."

service jenkins start
currentDate=`date`
msgID=`date|md5sum|cut -c -10`
currMsgFile=my${msgID}.msg
cp ~/my.msg $currMsgFile
sed -i -e "s/REPLACE_WITH_SUBJECT/Jenkins started $currentDate/g" $currMsgFile
sed -i -e "s/REPLACE_WITH_BODY/Jenkins is now ready for action\nHave fun/g" $currMsgFile

ctx logger info "${currHostName}:${currFilename} Sending an email from Jenkins (Jenkins started)..."

cliJar=`find / -name "jenkins-cli.jar"`

userName=$(ctx node properties jenkins_user_name)
userPassw=$(ctx node properties jenkins_user_passw)
java -jar $cliJar -s http://localhost:8080/ login --username $userName --password $userPassw
java -jar $cliJar -s http://localhost:8080/ mail < $currMsgFile
rm $currMsgFile

ctx logger info "${currHostName}:${currFilename} Jenkins has been started"
