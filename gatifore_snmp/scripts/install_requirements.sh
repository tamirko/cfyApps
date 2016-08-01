#!/bin/bash

ctx logger info "$0 : Installing pysnmp 4.2.5 ...."

pip install pysnmp==4.2.5

ctx logger info "$0 : Done installing pysnmp 4.2.5"


# sudo apt-get install snmp
# snmpwalk -c public -v 1 10.0.0.139

