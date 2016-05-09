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


def check_deployments(current_deployment_id, allowed_hours):
    log_file = open(LOG_FILE_PATH + current_deployment_id + '.log', 'w')
    try: 
        log_file.write('check_deployments:\n')
        cloudify_client = CloudifyClient('localhost')
        allowed_seconds = (int(allowed_hours) * 3600)
        log_file.write("allowed_hours {0} = allowed_seconds {1}\n".
                       format(allowed_hours, allowed_seconds))

        for deployment in cloudify_client.deployments.list():
            deployment_id = deployment.id
            if deployment_id != current_deployment_id:
                all_executions = cloudify_client.executions.list(deployment_id=deployment_id)
                all_executions_ended = all([str(_e['status']) in Execution.END_STATES for _e in all_executions])
                if all_executions_ended:
                    log_file.write("Deployment {0} has no live executions\n".format(deployment_id))

                deployment_installed = False
                deployment_should_b_deleted = False
                for execution in all_executions:
                    wf_Id = execution.workflow_id
                    if wf_Id == "install":
                        deployment_installed = True

                    if wf_Id == "create_deployment_environment":
                        time_diff = get_time_diff(execution.created_at)
                        days_diff = time_diff.days
                        hours_diff = (time_diff.seconds/3600)
                        seconds_diff = time_diff.total_seconds()
                        log_file.write('Deployment {0} created_at: {1}, - {2} days and {3} hours ago. '
                                       'A total of {4} seconds ago\n'.format(deployment_id, execution.created_at,
                                                                             days_diff, hours_diff, seconds_diff))
                    
                        if allowed_seconds < seconds_diff:
                            log_file.write("Deployment {0} should be deleted ....\n".format(deployment_id))
                            deployment_should_b_deleted = True

                if deployment_should_b_deleted:
                    if deployment_installed:
                        log_file.write("Uninstalling deployment {0}...\n".format(deployment_id))
                        curr_status = cloudify_client.executions.start(deployment_id, 'uninstall')
                        log_file.write("Uninstall status for deployment {0} is {1}...\n".
                                       format(deployment_id, curr_status))
                        time.sleep(60)
                    log_file.write("Deleting deployment {0}...\n".format(deployment_id))
                    cloudify_client.deployments.delete(deployment_id)
                else:
                    log_file.write("Leave deployment {0} alive\n".format(deployment_id))


        log_file.write("------------------------------------------------------\n")

    except Exception as e:
         log_file.write(str(e))


def main(argv):
    for i in range(len(argv)):
        print ("argv={0}\n".format(argv[i]))
    current_deployment_id = argv[1]
    pid_file = open(PID_FILE_PATH + current_deployment_id, 'w')
    pid_file.write('%i' % getpid())
    pid_file.close()

    allowed_hours = argv[2]
    check_deployments(current_deployment_id, allowed_hours)

if __name__ == '__main__':
    main(sys.argv)
