#! /bin/bash

ctx logger info "Starting $0 ..."

current_user=`whoami`

allowed_days="$(ctx node properties allowed_days)"
ctx logger info "allowed_days = ${allowed_days}"
allowed_hours="$(ctx node properties allowed_hours)"
ctx logger info "allowed_hours = ${allowed_hours}"
DPLID=$(ctx deployment id)
currVenv=/root/${DPLID}/env
ctx logger info "deployment_id = ${DPLID}, virtual env is ${currVenv}"
pipPath=${currVenv}/bin/pip

ctx logger info "Downloading scripts/undeployer.py ..."
LOC=$(ctx download-resource scripts/undeployer.py)
status_code=$?
ctx logger info "ctx download-resource status code is ${status_code}"
ctx logger info "LOC is ${LOC}"

COMMAND="${currVenv}/bin/python ${LOC} ${DPLID} ${allowed_days} ${allowed_hours}"
crontab_file=/tmp/mycron
ctx logger info "Adding ${COMMAND} to ${crontab_file} ..."
echo "*/3 * * * * ${COMMAND}" >> ${crontab_file}
status_code=$?
ctx logger info "echo ${COMMAND} code is ${status_code}"
ctx logger info "Adding the task to the crontab : crontab ${crontab_file} ..."
sudo crontab ${crontab_file}
status_code=$?
ctx logger info "crontab ${crontab_file} status code is ${status_code}"
currCrontab=`sudo crontab -l`
ctx logger info "currCrontab is ${currCrontab}"
ctx logger info "Done adding the task to the crontab - Starting the undeployer"
