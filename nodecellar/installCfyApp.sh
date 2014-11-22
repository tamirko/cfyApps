#!/bin/bash
export blueprintID=ec2mysql12_11_e$1
export deploymentID=tamirmysql12_11_e$1
cfy blueprints upload -p ec2-blueprint.yaml -b $blueprintID
cfy deployments create -d $deploymentID -b $blueprintID -v
cfy executions start -d $deploymentID -w install
#cat out.txt > `awk -F\' '{print $2}'`
#grep "on port" out.txt
echo $deploymentID > currDeploymentID

