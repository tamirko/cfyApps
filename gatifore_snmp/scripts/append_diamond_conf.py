from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

APPEND_DIAMOND_STR = "append_diamond_conf"
ctx.logger.info("Starting {0} ... ".format(APPEND_DIAMOND_STR))
target_instance = ctx.target.instance
ctx.logger.info("{0} target_instance {1} ... ".format(APPEND_DIAMOND_STR, target_instance))
target_node = ctx.target.node
ctx.logger.info("{0} target_node {1} ... ".format(APPEND_DIAMOND_STR, target_node))
src_instance = ctx.source.instance
ctx.logger.info("{0} src_instance {1} ... ".format(APPEND_DIAMOND_STR, src_instance))

ctx.logger.info("{0} ctx.target.node.name {1} ... ".format(APPEND_DIAMOND_STR, ctx.target.node.name))
config = src_instance.runtime_properties.get('snmp_collector_config', {})

for key, val in config.items():
    if isinstance(val, dict):
        ctx.logger.info("  {0} config.{1} b4 -> ... ".format(APPEND_DIAMOND_STR, key))
        for k, v in val.items():
            ctx.logger.info("  {0} config.{1} b4 -> {2}:{3} ... ".format(APPEND_DIAMOND_STR, key, k, v))
    else:
        ctx.logger.info("{0} config b4 -> {1}:{2} ... ".format(APPEND_DIAMOND_STR, key, str(val)))

devices_conf = config.get('devices', {})
devices_conf[ctx.target.node.name] = device_config = {}
device_config['node_instance_id'] = target_instance.id
device_config['node_id'] = target_node.id
if 'host' in inputs:
    device_config['host'] = inputs.host
else:
    device_config['host'] = target_instance.host_ip
ctx.logger.info("xxx {0} host is {1} ... yyy".format(APPEND_DIAMOND_STR, device_config['host']))

device_config['port'] = inputs.port
device_config['community'] = inputs.community
device_config['oids'] = inputs.oids

config['devices'] = devices_conf

for key, val in config.items():
    if isinstance(val, dict):
        ctx.logger.info("  {0} config.{1} after -> ... ".format(APPEND_DIAMOND_STR, key))
        for k, v in val.items():
            ctx.logger.info("  {0} config.{1} after -> {2}:{3} ... ".format(APPEND_DIAMOND_STR, key, k, v))
    else:
        ctx.logger.info("{0} config after -> {1}:{2} ... ".format(APPEND_DIAMOND_STR, key, str(val)))

src_instance.runtime_properties['snmp_collector_config'] = config
