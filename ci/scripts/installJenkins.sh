#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")


ctx logger info "${currHostName}:${currFilename} Installing Jenkins..."

wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list
apt-get update
apt-get install -y -q jenkins

ctx logger info "${currHostName}:${currFilename} Installing git..."
apt-get install -y -q git

ctx logger info "${currHostName}:${currFilename} Installing sendmail..."
apt-get install -y -q sendmail

service jenkins stop

exit 


# Some docs and examples from here ....

http://119.81.178.101:8080/cli/

currentUser=james
#cliJar=/var/cache/jenkins/war/WEB-INF/jenkins-cli.jar
cliJar=`find / -name "jenkins-cli.jar"`

java -jar $cliJar -s http://localhost:8080/ login --username $currentUser --password 1234
java -jar $cliJar -s http://localhost:8080/ who-am-i
Authenticated as: tamir
Authorities:
  authenticated
java -jar $cliJar -s http://localhost:8080/ who-am-i |& grep $currentUser

java -jar $cliJar -s http://localhost:8080/ build 'my-project-build'

java -jar $cliJar -s http://localhost:8080/ disable-job build3
java -jar $cliJar -s http://localhost:8080/ enable-job build3
java -jar $cliJar -s http://localhost:8080/ version
1.601

# Get the builds's definition(xml) : 
java -jar $cliJar -s http://localhost:8080/ get-job build3

java -jar $cliJar -s http://localhost:8080/ console
java -jar $cliJar -s http://localhost:8080/ list-jobs
java -jar $cliJar -s http://localhost:8080/ list-plugins
java -jar $cliJar -s http://localhost:8080/ list-changes build3 26-30 -format XML

java -jar $cliJar -s http://localhost:8080/ mail < my.msg

exec sh -c "x=`date +%s` && touch /tmp/xxx/file${x}"
exec sh -c "y=`date +%s` && touch /tmp/xxx/dev${y}"

http://techieroop.com/run-jenkins-build-from-command-line/#.VOxPlC5WJFs


https://wiki.jenkins-ci.org/display/JENKINS/Jenkins+CLI

https://wiki.jenkins-ci.org/display/JENKINS/Remote+access+API

https://wiki.jenkins-ci.org/display/JENKINS/Monitoring+external+jobs

http://stackoverflow.com/questions/20379202/running-the-exec-command-in-jenkins-execute-shell

#https://www.digitalocean.com/community/tutorials/how-to-install-and-use-jenkins-on-ubuntu-12-04