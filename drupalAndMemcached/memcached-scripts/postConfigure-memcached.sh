#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

export PATH=$PATH:/usr/sbin:/sbin:/usr/bin

memcachedPort=$(ctx target node properties port)
ctx logger info "xxx ${currHostName}:${currFilename} :memcached port ${memcachedPort}"

memcachedHost=$(ctx target instance host_ip)
ctx logger info "xxx ${currHostName}:${currFilename} :memcached host ${memcachedHost}"

currRequiredmemory=$(ctx target node properties requiredmemory)
ctx logger info "xxx ${currHostName}:${currFilename} :Setting memory value to ${currRequiredmemory} in /etc/memcached.conf"
sudo sed -i -e "s/64/${currRequiredmemory}/g" /etc/memcached.conf

ctx logger info "xxx ${currHostName}:${currFilename} :Configuring the listening host ${memcachedHost} in /etc/memcached.conf"
origIP=127.0.0.1
sudo sed -i -e "s/${origIP}/${memcachedHost}/g" /etc/memcached.conf

memcachePsEf=`ps -ef | grep -iE "memcache" | grep -ivE "cfy|cloudify|grep|${currFilename}"`
ctx logger info "xxx ${currHostName}:${currFilename} :curr memcached memcachePsEf ${memcachePsEf}"

echo "xxx ${currHostName}:${currFilename} End of ${currFilename}"
ctx logger info "xxx ${currHostName}:${currFilename} End of ${currFilename}"