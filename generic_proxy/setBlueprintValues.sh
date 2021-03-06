#!/bin/bash

# Do not use dash (minus sign) in the these setting.
# Only underscore is allowed.
# ===================================================

# Replace the value with: the name of the your blueprint
export folderPrefix=BP_

# Replace the value with: Primary device's name
export PRIMARY_NAME=FIREWALL_1911_v6
# Replace the value with: Primary device's type
export PRIMARY_TYPE=FIREWALL

# Replace the value with: Primary device's 1st element's name
export PRIMARY_DEVICE_ELEMENT1_NAME=SSL_VPN_2A
# Replace the value with: Primary device's 2nd element's name
export PRIMARY_DEVICE_ELEMENT2_NAME=ANTI_SPAM_1g7


# Replace the value with: Secondary device's name
export SECONDARY_NAME=ROUTER_1911_v6
# Replace the value with: Secondary device's type
export SECONDARY_TYPE=ROUTER

# Replace the value with: Secondary device's 1st element's name
export SECONDARY_DEVICE_ELEMENT1_NAME=ROUTING_TABLE_8A01
# Replace the value with: Secondary device's 2nd element's name
export SECONDARY_DEVICE_ELEMENT2_NAME=ROUTING_TABLE_339

