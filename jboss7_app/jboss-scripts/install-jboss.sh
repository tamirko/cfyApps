#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

type unzip
if [ $? -ne 0 ] ; then
  ctx logger info "${currHostName}:${currFilename} installing unzip ..."
  sudo yum -y -q install unzip || exit $?
fi

type wget
if [ $? -ne 0 ] ; then
  ctx logger info "${currHostName}:${currFilename} installing wget ..."
  sudo yum -y -q install wget || exit $?
fi

DIR=/tmp
if [ ! -d $DIR/jboss ]; then
  mkdir $DIR/jboss
fi

cd $DIR/jboss

jboss_download_url=$(ctx node properties jboss_download_url)
jbossZip=jboss.zip
ctx logger info "${currHostName}:${currFilename} Downloading Jboss from ${jboss_download_url} ..."
wget -O $jbossZip ${jboss_download_url}

ctx logger info "${currHostName}:${currFilename} Unzipping Jboss ..."
unzip ${jbossZip}

rm ${jbossZip}
jboss_unzipped_folder=`ls -1`
cd $jboss_unzipped_folder
jboss_root_folder=`pwd`
ctx logger info "${currHostName}:${currFilename} jboss_root_folder is ${jboss_root_folder} ..."
ctx instance runtime_properties jboss_root_folder ${jboss_root_folder}

ctx logger info "${currHostName}:${currFilename} installing java-1.7.0-openjdk ..."
sudo yum -y -q install java-1.7.0-openjdk || exit $?

