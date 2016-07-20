# #######
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
'''
    Fortinet.FortiGate.Firewall.Policy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Handles config subsystem firewall/policy*
'''

import logging
from cloudify import ctx
from cloudify.decorators import operation
from fortigate.config import Config
from fortigate.utils import dict_update


class Policy(Config):
    '''
        FortiGate Firewall/Policy interface

    :param int policy_id:
        Policy ID to update
    :param dict ssh_config:
        Key-value pair that get sent to `fabric.api.settings`
    '''
    def __init__(self, policy_id, ssh_config):
        Config.__init__(self, ssh_config,
                        name='firewall policy',
                        cid=policy_id)


@operation
def create(config_id, config, ssh_config, **_):
    '''config/firewall/policy'''
    # Enable Paramiko debug logging to CTX logger
    # enable_paramiko_debug_logging()
    ctx.logger.info('config: {0}'.format(config))
    # Merge properties and lifecycle inputs
    config_id = config_id or ctx.node.properties.get('config_id')
    ssh_config = dict_update(
        ssh_config, ctx.node.properties.get('ssh_config'))
    config = dict_update(
        config, ctx.node.properties.get('config'))
    # Create the configuration
    iface = Policy(config_id, ssh_config)
    iface.create(config)
    # Set runtime properties
    ctx.instance.runtime_properties['ssh_config'] = ssh_config
    ctx.instance.runtime_properties['config_id'] = config_id
    ctx.instance.runtime_properties['config'] = iface.read()
    # Dump the runtime properties
    ctx.logger.debug('Runtime properties: {0}'.format(
        ctx.instance.runtime_properties))


@operation
def delete(**_):
    '''config/firewall/policy'''
    # Delete the config item
    Policy(
        ctx.instance.runtime_properties.get('config_id'),
        ssh_config=ctx.instance.runtime_properties.get('ssh_config')
    ).delete()


def enable_paramiko_debug_logging():
    '''Enables Paramiko debug logging to ctx.logger'''
    for handler in ctx.logger.handlers:
        logging.getLogger("paramiko").addHandler(handler)
    logging.getLogger("paramiko").setLevel(logging.DEBUG)
    logging.getLogger("paramiko.transport").setLevel(logging.DEBUG)
