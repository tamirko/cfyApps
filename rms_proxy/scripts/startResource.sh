#! /bin/bash

resourceID="$(ctx node properties resourceID)"
resourceName="$(ctx node properties resourceName)"
ctx logger info "resourceID ${resourceID} ..."
ctx logger info "resourceName ${resourceName} ..."

curr_date=`date +%d_%m_%Y_%H_%M_%S`
curr_instanceID="$(ctx instance id)"
requestid="${curr_instanceID}_${curr_date}"
ctx instance runtime-properties requestid ${requestid}
