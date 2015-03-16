#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

echo "${currHostName}:${currFilename} Jenkins build $1..."

mkdir -p /tmp/tamir$1

echo "${currHostName}:${currFilename} End of Jenkins build $1"
