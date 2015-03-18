#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

echo "${currHostName}:${currFilename} Jenkins build $1..."

if [ "${currentTask}" == "dummy" ]; then
  msgID=`date|md5sum|cut -c -10`
  echo "${currHostName}:${currFilename} Jenkins creating /tmp/tamir$1${msgID}"
  mkdir -p /tmp/tamir$1$msgID
else  
  echo "${currHostName}:${currFilename} Jenkins creating /tmp/tamir$1${currentTask}"
  mkdir -p /tmp/tamir$1$currentTask
fi

echo "${currHostName}:${currFilename} End of Jenkins build $1"
