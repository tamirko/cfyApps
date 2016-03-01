#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Starting Jenkins..."

sudo service jenkins start

currentDate=`date`
msgID=`date|md5sum|cut -c -10`
currMsgFile=my${msgID}.msg
cp ~/my.msg $currMsgFile
sed -i -e "s/REPLACE_WITH_SUBJECT/Jenkins started $currentDate - on $currHostName/g" $currMsgFile
sed -i -e "s/REPLACE_WITH_BODY/Jenkins is now ready for action\nHave fun/g" $currMsgFile

ctx logger info "${currHostName}:${currFilename} Sending an email from Jenkins (Jenkins started)..."

cliJar=`sudo find / -name "jenkins-cli.jar"`

userName=$(ctx node properties jenkins_user_name)
ctx logger info "Jnekins user name is ${userName}"

userPassw=$(ctx node properties jenkins_user_passw)
ctx logger info "Jnekins password is ${userPassw}"

ctx logger info "Login to Jenkins ... "
sudo java -jar $cliJar -s http://localhost:8080/ login --username $userName --password $userPassw
ctx logger info "Sending email $currMsgFile ... "
sudo java -jar $cliJar -s http://localhost:8080/ mail < $currMsgFile
ctx logger info "Logout from Jenkins ... "
sudo java -jar $cliJar -s http://localhost:8080/ logout
rm $currMsgFile

ctx logger info "${currHostName}:${currFilename} Jenkins has been started"
