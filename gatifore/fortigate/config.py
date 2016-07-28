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
    Fortinet.FortiGate.Config
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Low-level configuration subsystem interface
'''

from cloudify import ctx
from cloudify.exceptions import NonRecoverableError
from cloudify.decorators import operation
from fortigate.generic import Generic
from fortigate.utils import dict_update

# pylint: disable=R0201


class Config(Generic):
    '''
        FortiGate interface for performing CRUD operations on
        the configuration subsystem

    :param dict ssh_config:
        Key-value pair that get sent to `fabric.api.settings`
    '''
    def __init__(self, ssh_config, name=None, cid=None, _ctx=ctx):
        # Init the inherited class
        Generic.__init__(self, ssh_config, _ctx=_ctx)
        self.ctx = _ctx
        self.name = name
        self.cid = cid

    def create(self, params, name=None, cid=None, with_quotes=False):
        '''
            Creates a FortiGate config entry

        :param dict params:
            Key-value pairs of configuration parameters to set
        :param string name:
            Name of the configuration element (eg. "firewall policy")
        :param string cid:
            Name of the specific configuration ID to edit
        '''
        name = name or self.name
        cid = cid or self.cid
        self.ctx.logger.info('Running config updates on "%s (%s)"', name, cid)
        # Sanity checks
        if not name:
            raise NonRecoverableError('Missing config name parameter')
        if not params:
            self.ctx.logger.warn(
                'No key-value pairs provided for config. Skipping...')
            return
        commands = []
        # Start in "config" mode
        commands.append('config {0}'.format(name))
        # Switch to "edit" mode (if needed)
        if cid:
            commands.append('edit {0}'.format(cid))
        # Run SET commands
        for param in params:
            for key, val in param.iteritems():
                if val is None or val == "":
                    commands.append('{0}').format(key)
                else:
                    if with_quotes:
                        commands.append('set {0} "{1}"'.format(key, val))
                    else:
                        commands.append('set {0} {1}'.format(key, val))
        # End "config" mode
        commands.append('end')
        # Run the command
        output = self.execute('\n'.join(commands))
        self.ctx.logger.info('[REMOTE] {0}'.format(output))

    def read(self, name=None, cid=None):
        '''
            Reads in a FortiGate config entry

        :param string name:
            Name of the configuration element (eg. "firewall policy")
        :param string cid:
            Name of the specific configuration ID to delete
        '''
        name = name or self.name
        cid = cid or self.cid
        self.ctx.logger.info('Running show config on "%s (%s)"', name, cid)
        # Sanity checks
        if not name:
            raise NonRecoverableError('Missing config name parameter')
        # Run the command
        command = 'show {0}'.format(name)
        if cid:
            command = '{0} {1}'.format(command, cid)
        return self.parse_output(
            self.execute('show {0} {1}'.format(name, cid)))

    def update(self, params, name=None, cid=None):
        '''
            Updates a FortiGate config entry

        :param string name:
            Name of the configuration element (eg. "firewall policy")
        :param string cid:
            Name of the specific configuration ID to edit
        :param dict params:
            Key-value pair of configuration parameters to set
        '''
        name = name or self.name
        cid = cid or self.cid
        # Sanity checks
        if not name:
            raise NonRecoverableError('Missing config name parameter')
        self.create(params, name=name, cid=cid)

    def delete(self, name=None, cid=None):
        '''
            Deletes a FortiGate config entry

        :param string name:
            Name of the configuration element (eg. "firewall policy")
        :param string cid:
            Name of the specific configuration ID to delete
        '''
        name = name or self.name
        cid = cid or self.cid
        self.ctx.logger.info('Running config delete on "%s (%s)"', name, cid)
        # Sanity checks
        if not name:
            raise NonRecoverableError('Missing config name parameter')
        if not cid:
            raise NonRecoverableError('Missing config id parameter')
        output = self.execute('\n'.join([
            # Start in "config" mode
            'config {0}'.format(name),
            # Delete the entry
            'delete {0}'.format(cid),
            # End "config" mode
            'end']))
        self.ctx.logger.info('[REMOTE] {0}'.format(output))

    def parse_output(self, raw_output):
        '''Converts raw output to a dict of config data'''
        props = dict()
        if not isinstance(raw_output, basestring):
            return None
        # Split by newline and strip whitespace
        output = [x.strip() for x in raw_output.rsplit('\n')]
        # Locate "set" lines, split by whitespace twice max, grab the
        # last two strings (key and val, excluding the word "set")
        opts = [x.rsplit(' ', 2)[1:] for x in output if x.startswith('set ')]
        # Strip out the quotation marks (which are seemingly arbitrarily placed)
        for opt in opts:
            props[opt[0]] = opt[1].strip('"')
        return props


@operation
def create(config_name, config_id, config, ssh_config, **_):
    '''Generic config create operation'''
    # Merge properties and lifecycle inputs
    config_name = config_name or ctx.node.properties.get('config_name')
    config_id = config_id or ctx.node.properties.get('config_id')
    ssh_config = dict_update(
        ssh_config, ctx.node.properties.get('ssh_config'))
    config = dict_update(
        config, ctx.node.properties.get('config'))
    # Get a config interface
    iface = Config(
        name=config_name,
        cid=config_id,
        ssh_config=ssh_config)
    # Create the config
    iface.create(config)
    # Set runtime properties
    ctx.instance.runtime_properties['ssh_config'] = ssh_config
    ctx.instance.runtime_properties['config_name'] = config_name
    ctx.instance.runtime_properties['config_id'] = config_id
    ctx.instance.runtime_properties['config'] = iface.read()
    # Dump the runtime properties
    ctx.logger.info('Runtime properties: {0}'.format(
        ctx.instance.runtime_properties))


@operation
def delete(**_):
    '''Generic config delete operation'''
    # Delete the config item
    Config(
        name=ctx.instance.runtime_properties.get('config_name'),
        cid=ctx.instance.runtime_properties.get('config_id'),
        ssh_config=ctx.instance.runtime_properties.get('ssh_config')
    ).delete()
    # Delete runtime properties
    ctx.instance.runtime_properties = dict()
