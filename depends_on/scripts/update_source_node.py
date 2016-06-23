from cloudify import ctx


targetInstanceID1 = ctx.target.instance.id
targetInstanceID2 = ctx.target.instance.runtime_properties['myStuffID']

ctx.logger.info("target myStuffID: {0}".format(targetInstanceID1))
ctx.logger.info("The runtime attribute of {0}, are :".format(targetInstanceID2))
for key in ctx.target.instance.runtime_properties:
    ctx.logger.info("{0}: {1}".format(key, ctx.target.instance.runtime_properties[key]))
