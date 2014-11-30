#!/bin/bash -x

# Caxzczxncel all stlkjkhhharted executions.  
cfy deployments list | grep tamir | awk -F\| '{print $2}' | sed 's/ //g' | xargs -I file cfy executions list -d file | grep install | grep -v uninstall | grep started |  awk -F\| '{print $2}' | sed 's/ //g' |  xargs -I file cfy executions cancel -e file -f
sdfsd
# Uninstall all apps
cfy deployments list | grep tamir | awk -F\| '{print $2}' | sed 's/ //g' | xargs -I file cfy executions start -d file -f -w uninstall

# Delete all deployments
cfy deployments list | grep tamir | awk -F\| '{print $2}' | sed 's/ //g' | xargs -I file cfy deployments delete -f -d file

# Delete all blueprints
cfy blueprints list | grep ec2 | awk -F\| '{print $2}' | sed 's/ //g' | xargs -I file cfy blueprints delete -b file &






