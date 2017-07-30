from cloudify import ctx

from cloudify.state import ctx_parameters as inputs


# Add the following check :
#if use_external_resource don't add nor charge or only add ,but don't charge ...


#params_list = ctx.source.node.properties['params_list']
params_list = ctx.source.node.properties
ctx.logger.info("Show params_list params: {}".format(params_list))

target_properties = ctx.target.node.properties
for curr_prop in target_properties:
    ctx.logger.info("target prop {0}:{1}".format(curr_prop, target_properties[curr_prop]))


ctx.logger.info("source node id is {0}".format(ctx.source.node.id))
curr_instance_id = ctx.source.instance.id
ctx.logger.info("source node instance id is {0}".format(curr_instance_id))


request_id_str = "requestid"
if request_id_str in ctx.source.instance.runtime_properties:
    curr_value = ctx.source.instance.runtime_properties[request_id_str]
    ctx.logger.info("{0}: {1}={2}".format(curr_instance_id, request_id_str, curr_value))

use_external_resource_str = "use_external_resource"
if use_external_resource_str in ctx.source.node.properties:
    curr_use_external_resource = ctx.source.node.properties[use_external_resource_str]
else:
    curr_use_external_resource = True

ctx.logger.info("{0}: {1}={2}".format(curr_instance_id, use_external_resource_str, curr_use_external_resource))


ctx.logger.info("End of add_resource_to_rms.py")


