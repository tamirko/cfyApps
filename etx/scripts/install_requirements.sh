#!/bin/bash

ctx logger info "$0 : Installing pysnmp 4.2.5 ...."
pip install pysnmp==4.2.5
ctx logger info "$0 : Done installing pysnmp 4.2.5"

ctx logger info "$0 : Running sudo apt-get install -y -q libsnmp-dev ...."
sudo apt-get install -y -q libsnmp-dev

ctx logger info "$0 : Running sudo apt-get install -y -q snmp...."
sudo apt-get install -y -q snmp


# sudo apt-get install snmp
# snmpwalk -c public -v 1 185.98.150.93
# snmpwalk -v2c -c public F 1.3.6.1.4.1.12356