#! /bin/bash

ctx logger info "Starting $0 ..."

current_user=`whoami`

altitude="$(ctx node properties altitude)"
ctx logger info "altitude = ${altitude}"
altitude="$(ctx node properties altitude)"
ctx logger info "altitude = ${altitude}"
DPLID=$(ctx deployment id)
currVenv=/root/${DPLID}/env
ctx logger info "deployment_id = ${DPLID}, virtual env is ${currVenv}"
pipPath=${currVenv}/bin/pip
COMMAND="sudo ${currVenv}/bin/python ${LOC} ${DPLID} ${altitude} ${altitude}"
ctx logger info "Adding ${COMMAND} to ..."
ctx logger info "$0 Done"
