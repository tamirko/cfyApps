#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

tomcatVersion=$(ctx node properties tomcatVersion)
ctx logger info "${currHostName}:${currFilename} :tomcatVersion ${tomcatVersion}"

installDir=~/installDir
ctx logger info "${currHostName}:${currFilename} Removing $[installDir}... "
rm -rf $installDir

tomcatHome=~/$tomcatVersion
ctx logger info "${currHostName}:${currFilename} Removing ${tomcatHome} ..."
rm -rf $tomcatHome

export JAVA_HOME=~/java
ctx logger info "${currHostName}:${currFilename} Removing ${JAVA_HOME} ..."
rm -rf $JAVA_HOME


ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"




