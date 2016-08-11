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
    Fortinet.FortiGate.Workflows
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Common workflows
'''

from cloudify.decorators import workflow
from cloudify.workflows import ctx

from fortigate.generic import Generic
from fortigate.config import Config


@workflow
def updatenow(ssh_config, **_):
    '''Run update-now'''
    ctx.logger.info('Executing "updatenow" workflow')
    Generic(ssh_config, _ctx=ctx).execute('exec update-now')


@workflow
def update_xyz(ssh_config, config_name, cid, property_name, property_value, **_):

    if cid == "":
        cid = None
        ctx.logger.info("update_xyz: config {0}-> set {2} {3}".format(config_name, property_name, property_value))
    else:
        ctx.logger.info("update_xyz: config {0}-> edit {1}-> set {2} {3}".format(config_name, cid, property_name,
                                                                                 property_value))

    params = []
    param = {}
    param[property_name] = property_value
    params.append(param)

    Config(ssh_config=ssh_config, name=config_name, cid=cid, _ctx=ctx).create(params=params)

    ctx.logger.info("End of update_xyz")