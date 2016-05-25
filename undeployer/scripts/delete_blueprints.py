import sys
from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
import json 
from os import utime
from os import getpid 
from os import path
import time
import datetime
from datetime import datetime

LOG_FILE_PATH = '/tmp/undeployer_'
PID_FILE_PATH = '/tmp/pid_file_'


def get_time_diff(orig_time):
    d2 = datetime.now()
    d1 = datetime.strptime(orig_time, '%Y-%m-%d %H:%M:%S.%f')
    time_diff = d2 - d1
    return time_diff


def check_blueprints(allowed_seconds):
    cloudify_client = CloudifyClient('localhost')
    for blueprint in cloudify_client.blueprints.list():
        deployment_list = cloudify_client.deployments.list(blueprint_id=blueprint.id)
        if deployment_list is None or len(deployment_list) == 0:
            print "There are no deployments for blueprint {0}".format(blueprint.id)
            time_diff = get_time_diff(blueprint.created_at)
            seconds_diff = time_diff.total_seconds()
            if allowed_seconds < seconds_diff:
                print "Deleting blueprint {0} ...".format(blueprint.id)
                cloudify_client.blueprints.delete(blueprint.id)
        #else:
            #for deployment in deployment_list:
                #print "deployment_id is {0}".format(deployment.id)


def main(argv):
    for i in range(len(argv)):
        print ("argv={0}\n".format(argv[i]))
    current_deployment_id = argv[1]
    pid_file = open(PID_FILE_PATH + current_deployment_id, 'w')
    pid_file.write('%i' % getpid())
    pid_file.close()

    allowed_hours = argv[2]
    check_blueprints(allowed_hours)

if __name__ == '__main__':
    main(sys.argv)
