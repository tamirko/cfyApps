#!/bin/bash -x

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

export PATH=$PATH:/usr/sbin:/sbin:/usr/bin || error_exit $? "Failed on: export PATH=$PATH:/usr/sbin:/sbin"

ctx logger info "xxx ${currHostName}:${currFilename} :sudo service memcached start..."
sudo service memcached start || error_exit $? "Failed on: sudo service memcached start"

memcachePsEf=`ps -ef | grep -iE "memcache" | grep -ivE "cfy|cloudify|grep|${currFilename}"`
ctx logger info "xxx ${currHostName}:${currFilename} :curr memcached memcachePsEf ${memcachePsEf}"


#/usr/bin/memcached -m 64 -p 11211 -u memcache -l 127.0.0.1