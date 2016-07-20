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


@workflow
def updatenow(ssh_config, **_):
    '''Run update-now'''
    ctx.logger.info('Executing "updatenow" workflow')
    Generic(ssh_config, _ctx=ctx).execute('exec update-now')
