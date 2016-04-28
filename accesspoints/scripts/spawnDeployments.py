import sys
from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
from os import getpid

def check_deployments(current_deployment_id, allowed_days, allowed_hours):
    try:
        cloudify_client = CloudifyClient('localhost')

        blueprint_id = "sfsdfdxxxx"
        deployment_inputs = {
            "xxx" : "yyyxxx",
            "zzzxxx" : "wwwxxx"
        }
        child_deployment = cloudify_client.deployments.create(blueprint_id, current_deployment_id, inputs=deployment_inputs)
        cloudify_client.executions.start(current_deployment_id, 'install')
    except Exception as e:
         print str(e)


def main(argv):
    for i in range(len(argv)):
        print ("argv={0}\n".format(argv[i]))
    current_deployment_id = argv[1]
    check_deployments(current_deployment_id, xxx, yyy)

if __name__ == '__main__':
    main(sys.argv)
