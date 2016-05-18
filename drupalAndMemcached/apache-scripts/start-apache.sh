#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	echo "$2 : error code: $1"
	exit ${1}
}

export PATH=$PATH:/usr/sbin:/sbin || error_exit $? "Failed on: export PATH=$PATH:/usr/sbin:/sbin"

ctx logger info "${currHostName}:${currFilename} Starting apache..."
sudo /etc/init.d/apache2 start || error_exit $? "Failed on: sudo /etc/init.d/apache2 start"

ps -ef | grep -i apache2 | grep -v grep


host_id2=$(ctx instance host_id)
#ctx logger info "aaa host_id2 is ${host_id2}"
host_id3=$(ctx instance runtime_properties host_id)
#ctx logger info "aaa host_id3 is ${host_id3}"
host_id4=$(ctx _node_instance host_id)
#ctx logger info "aaa host_id4 is ${host_id4}"
host_id=$(ctx instance _node_instance host_id)
ctx logger info "aaa host_id is ${host_id}"
all_logs=`sudo find / -name "*.log" | grep -E "${host_id}/work/${host_id}"`
ctx logger info "aaa all_logs is ${all_logs}"
mngr_ip_addr=`sudo find / -name "*.log" | grep -E "${host_id}/work/${host_id}" | xargs -I file grep -E "Connecting to.*5672" file | tail -1 | xargs -I file echo file | sed -e "s+\(.*\)\(Connecting to \)\(.*\)\(:5672\)+\3+g"`
ctx logger info "aaa mngr_ip_addr is ${mngr_ip_addr}"

ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"