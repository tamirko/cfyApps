#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

#https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu

apt-get update
apt-get install -y -q wget
apt-get install -y -q ca-certificates

java_url=https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/com/oracle/java/1.7.0_21/jdk-7u21-linux-x64.tar.gz
javaTarGZ=java.tar.gz
wget -O $javaTarGZ --no-check-certificate $java_url
tar -xvf $javaTarGZ
rm $javaTarGZ
export JAVA_HOME=~/java
mv `ls | grep jdk` $JAVA_HOME
export PATH=$JAVA_HOME/bin:$PATH

wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key |  apt-key add -
sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
apt-get install -y -q jenkins
apt-get install -y -q aptitude
aptitude -y install nginx
cd /etc/nginx/sites-available
rm default ../sites-enabled/default

cat >jenkins <<XXX
upstream app_server {
    server 127.0.0.1:8080 fail_timeout=0;
}

server {
    listen 80;
    listen [::]:80 default ipv6only=on;
    server_name ci.yourcompany.com;

    location / {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$http_host;
        proxy_redirect off;

        if (!-f \$request_filename) {
            proxy_pass http://app_server;
            break;
        }
    }
}
XXX



ln -s /etc/nginx/sites-available/jenkins /etc/nginx/sites-enabled/

apt-get install -y -q php5 php5-cgi php5-fpm
service nginx restart

