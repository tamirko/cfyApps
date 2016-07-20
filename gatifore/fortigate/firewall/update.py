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
    Fortinet.FortiGate.Firewall.Update
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Handles execute subsystem for update-*
'''

from cloudify import ctx
from cloudify.decorators import operation
from fortigate.generic import Generic
from fortigate.utils import dict_update

# pylint: disable=R0913


class Update(Generic):
    '''
        FortiGate interface for performing firewall updates

    :param dict ssh_config:
        Key-value pair that get sent to `fabric.api.settings`
    '''
    def __init__(self, ssh_config):
        # Init the inherited class
        Generic.__init__(self, ssh_config)

    def update_av(self):
        '''update-av'''
        self.execute('execute update-av')

    def update_geo_ip(self):
        '''update-geo-ip'''
        self.execute('execute update-geo-ip')

    def update_ips(self):
        '''update-ips'''
        self.execute('execute update-ips')

    def update_list(self):
        '''update-list'''
        self.execute('execute update-list')

    def update_src_vis(self):
        '''update-src-vis'''
        self.execute('execute update-src-vis')


@operation
def create(update_av,
           update_geo_ip,
           update_ips,
           update_list,
           update_src_vis,
           ssh_config, **_):
    '''Generic config create operation'''
    # Merge properties and lifecycle inputs
    update_av = update_av or ctx.node.properties.get('update_av')
    update_geo_ip = update_geo_ip or \
        ctx.node.properties.get('update_geo_ip')
    update_ips = update_ips or ctx.node.properties.get('update_ips')
    update_list = update_list or ctx.node.properties.get('update_list')
    update_src_vis = update_src_vis or \
        ctx.node.properties.get('update_src_vis')
    ssh_config = dict_update(
        ssh_config, ctx.node.properties.get('ssh_config'))
    # Execute the updates
    iface = Update(ssh_config)
    if update_av:
        iface.update_av()
    if update_geo_ip:
        iface.update_geo_ip()
    if update_ips:
        iface.update_ips()
    if update_list:
        iface.update_list()
    if update_src_vis:
        iface.update_src_vis()
