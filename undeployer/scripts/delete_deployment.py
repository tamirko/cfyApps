#!/usr/bin/env python

import sys
import time
from cloudify_rest_client.executions import Execution
from cloudify_cli.utils import get_rest_client

client = get_rest_client()

deployment_id = sys.argv[1]

print 'Uninstalling deployment {0}'.format(deployment_id)
#client.executions.start(deployment_id, 'uninstall')

#time.sleep(30)

print 'Canceling bad executions for deployment {0}'.format(deployment_id)

for execution in client.executions.list(deployment_id=deployment_id):
    if execution.status not in Execution.END_STATES:
        print 'Updating execution {0} to state {1}'.format(execution.id, Execution.CANCELLED)
        client.executions.update(execution.id, Execution.CANCELLED)

print 'Deleting deployment: {0}'.format(deployment_id)
client.deployments.delete(deployment_id)

print 'Deployment deleted successfully'
