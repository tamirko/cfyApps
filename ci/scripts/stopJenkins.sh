#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")


ctx logger info "${currHostName}:${currFilename} Stopping Jenkins..."

service jenkins stop

ctx logger info "${currHostName}:${currFilename} Jenkins has been stopped"
