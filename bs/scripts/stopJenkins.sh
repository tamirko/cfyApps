#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")


ctx logger info "${currHostName}:${currFilename} Stopping Jenkins..."

sudo service jenkins stop

ctx logger info "${currHostName}:${currFilename} Jenkins has been stopped"
