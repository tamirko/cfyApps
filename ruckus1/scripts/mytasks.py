#!/usr/bin/env python

from fabric.api import run
from cloudify import ctx


def retrieve_file_content(file_name):
    ctx.logger.info("In retrieve_file_content file_name is {0} ...".format(file_name))
    command = "cat {0}".format(file_name)
    ctx.logger.info("Command is {0}".format(command))
    curr_output = run(command)
    ctx.logger.info("Command output is {0}".format(curr_output))
    ctx.instance.runtime_properties[file_name] = curr_output
    ctx.logger.info("Command output is stored in rt.{0} {1}".format(file_name, curr_output))
    ctx.logger.info("End of retrieve_file_content ...")


# https://github.com/cloudify-examples/clearwater-nfv-blueprint/blob/e004a11122398f1b38f3e5187362b25059dd4aa2/types/clearwater.yaml
#https://github.com/cloudify-examples/simple-kubernetes-blueprint/blob/a5ea7c3a81241f0350d7c25112bdfe930b7c5384/imports/kubernetes.yaml

#ssh -i ~/.ssh/nec_aws15_11.pem -o 'IdentitiesOnly yes' centos@13.125.3.21

#cfy exe start execute_operation -d $dep -p operation=utils.get_file_content --allow-custom-parameters -p node_ids=CentOS7
#cfy exe start execute_operation -d $dep -p operation=utils.get_file_content --allow-custom-parameters -p node_ids=CentOS7 -p "{'operation_kwargs':{'task_properties':{'file_name':'/home/centos/111.222'}}}" -p allow_kwargs_override=true
#export file_name=/home/centos/111.222
#cfy exe start execute_operation -d $dep -p operation=utils.get_file_content --allow-custom-parameters -p node_ids=CentOS7 -p "{'operation_kwargs':{'task_properties':{'file_name':'${file_name}'}}}" -p allow_kwargs_override=true