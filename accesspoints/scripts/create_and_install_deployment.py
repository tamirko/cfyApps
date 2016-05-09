#!/usr/bin/env python

import sys

from cloudify_rest_client.executions import Execution
from cloudify_cli.utils import get_rest_client
import time
import random


def check_if_deployment_is_ready(client, deployment_id):
    #print "check_if_deployment_is_ready {0}".format(deployment_id)
    _execs = client.executions.list(deployment_id=deployment_id)
    #print "Got all executions for deployment {0}".format(deployment_id)
    return all([str(_e['status']) == "terminated" for _e in _execs])


timeout = 120
sleep_time = 10
client = get_rest_client()
current_deployment_id = sys.argv[1]
blueprint_id = "accesspoints"
deployment_inputs = {
	"altitude" : 28.17-random.random(),
	"longtitude" : -2.01-random.random()
}



print 'Creating deployment {0} for blueprint {1}'.format(current_deployment_id, blueprint_id)
child_deployment = client.deployments.create(blueprint_id, current_deployment_id, 
	inputs=deployment_inputs)
print 'Waiting for deployment {0} to be ready...'.format(current_deployment_id)
start_time = time.time()
while time.time() <= start_time + timeout:
    #print "start_time {0}, current time {1}".format(start_time, time.time())
    if not check_if_deployment_is_ready(client, current_deployment_id):
    	#print "...Deployment {0} is not ready yet. Sleeping for {1} seconds".format(current_deployment_id, sleep_time)
        time.sleep(sleep_time)
    else:
    	print "Deployment {0} is ready".format(current_deployment_id)
    	break


print 'Installing deployment {0} '.format(current_deployment_id)
#client.executions.start(current_deployment_id, 'install')

print 'Done'
