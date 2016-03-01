########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
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


# ctx is imported and used in operations
from cloudify.workflows import ctx

# put the workflow decorator on any function that is a task
from cloudify.decorators import workflow

@workflow
def jenkins_run_cmd(cmd_name,arg_value="",key1_name="",key1_value="",**kwargs):
    ctx.logger.info("In jenkins_run_cmd {}".format(cmd_name))
    node = ctx.get_node('jenkins_app')
    ctx.logger.info("jenkins_run_cmd is about to exec on node.id {}".format(node.id))
	
    for instance in node.instances:
        instance.execute_operation("jenkins.interfaces.action.jenkins_cmd",
                                   kwargs={'process': {'args': [cmd_name,arg_value,key1_name,key1_value]}})
    ctx.logger.info("End of jenkins_run_cmd")
