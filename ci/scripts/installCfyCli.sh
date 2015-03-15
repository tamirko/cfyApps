#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} dummy installing Cloudify CLI ..."

echo "installCfyCli ..."