#! /bin/bash

ctx logger info "Starting $0 ..."

current_user=`whoami`

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

COMMAND="sudo ${currVenv}/bin/python ${LOC} ${DPLID} ${allowed_hours}"
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

# ssh cfyroot@138.91.188.861
# ssh -i ~/.ssh/cloudify-manager-kp-0104.pem centos@185.98.148.832
# sudo -s
# source /root/undep10/env/bin/activate
# yum install -y gcc
# yum install -y python-setuptools
# yum install -y python-devel
# source ....bin/activate
# pip install cloudify==3.3.1
# export CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
# export BROKER_URL=amqp://guest:guest@localhost:5672//
# export CTX_SOCKET_URL=http://localhost:35321
# export MANAGEMENT_IP=localhost
# export MANAGER_REST_PORT=80


exit

When the script plugin executes the script, it updates the script process with the CTX_SOCKET_URL environment variable.

If a unix domain socket based proxy was started, its value will look like: ipc:///tmp/ctx-f3j22f.socket
export CTX_SOCKET_URL=tcp://127.0.0.1:53213
If an http socket based proxy was started, its value will look like: http://localhost:35321