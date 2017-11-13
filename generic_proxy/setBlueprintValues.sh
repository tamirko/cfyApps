#!/bin/bash

# Do not use dash (minus sign) in the these setting.
# Only underscore is allowed.
# ===================================================

# Replace the value with: the name of the your blueprint
export folderPrefix=yourBlueprintName_2_

# Replace the value with: Primary device's name
export PRIMARY_NAME=FIREWALL_99
# Replace the value with: Primary device's type
export PRIMARY_TYPE=FIREWALL

# Replace the value with: Primary device's 1st element's name
export PRIMARY_DEVICE_ELEMENT1_NAME=SSL_VPN_14
# Replace the value with: Primary device's 2nd element's name
export PRIMARY_DEVICE_ELEMENT2_NAME=ANTI_SPAM_03


# Replace the value with: Secondary device's name
export SECONDARY_NAME=ROUTER_265
# Replace the value with: Secondary device's type
export SECONDARY_TYPE=ROUTER

# Replace the value with: Secondary device's 1st element's name
export SECONDARY_DEVICE_ELEMENT1_NAME=ROUTING_TABLE_08
# Replace the value with: Secondary device's 2nd element's name
export SECONDARY_DEVICE_ELEMENT2_NAME=ROUTING_TABLE_09

