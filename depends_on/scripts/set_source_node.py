from cloudify import ctx


# If this runs on a host agent, this may work or be needed
#from cloudify_cli.utils import get_rest_client
# client = get_rest_client()

from cloudify_rest_client import CloudifyClient


client = CloudifyClient('localhost')

ctx.logger.info("xxx Iterating over nodes and nodes instances:")

deployment_id = ctx.deployment.id
ctx.logger.info(" xxx deployment is {0}".format(deployment_id))

node_id = "MY_NODE_1"
prefix1 = "AAA"
prefix2 = "BBB"
my_node_1_instances_str = "{0}".format(prefix1)
ctx.logger.info('  yyy Checking node id {0}'.format(node_id))
for instance in client.node_instances.list(deployment_id=deployment_id, node_id=node_id):
    ctx.logger.info('   yyy Runtime attributes of instance id {0}'.format(instance.id))
    myStuffID = instance.runtime_properties['myStuffID']
    curr_str = "{0}{1}={2}{0}".format(prefix2, instance.id, myStuffID)
    ctx.logger.info('    yyy {0}'.format(curr_str))
    my_node_1_instances_str += "{0},".format(curr_str)

my_node_1_instances_str = my_node_1_instances_str[:-1]
my_node_1_instances_str += "{0}".format(prefix1)
ctx.logger.info("yyy my_node_1_instances_str is {0}".format(my_node_1_instances_str))
ctx.instance.runtime_properties["my_node_1_instances"] = my_node_1_instances_str
