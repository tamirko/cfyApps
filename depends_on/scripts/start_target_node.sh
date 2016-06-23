#! /bin/bash

ctx logger info "Starting $0 ..."

myHostIP="$(ctx instance host_ip)"
PUBLIC_IP_ADDR=$(wget -qO- ipinfo.io/ip)
ctx logger info "myHostIP = ${myHostIP}"
ctx instance runtime_properties myStuffID ${PUBLIC_IP_ADDR}
ctx instance runtime_properties blablax bloobloo1
ctx instance runtime_properties blablay bloobloo2
ctx logger info "myStuffID = ${PUBLIC_IP_ADDR}"


