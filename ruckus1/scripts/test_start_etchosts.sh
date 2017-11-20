#!/bin/bash

DPLID=$(ctx deployment id)
ctx logger info "++++ Start ${DPLID} +++"
export etchosts=`cat /etc/hosts`
ctx logger info " ++++ etchosts is ${etchosts}"
export xxxls=`ls -l`
ctx logger info " ++++ ls is ${xxxls}"

export date1=`date +%d_%m_%Y_%H_%M_%S`
device_id="device_${date1}"
ctx instance runtime-properties device_id "${device_id}"
ctx logger info " ++++ End +++"



#export dep=${bp}_dep_v1&&cfy bl upl -b $bp ~/cloudify-cosmo/cfyApps/ruckus1/text_blueprint.yaml&&cfy dep cr -b $bp --skip-plugins-validation $dep&&cfy exe start install -d $dep&&cfy dep out $dep