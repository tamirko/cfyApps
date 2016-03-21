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
def create_file(file_name,input_str,input_type,**kwargs):
    ctx.logger.info("In create_file {}".format(file_name))
    ctx.logger.info("input_str {}".format(input_str))
    ctx.logger.info("input_type {}".format(input_type))
    if input_type == 'name':
        node = ctx.get_node(input_str)
        ctx.logger.info( "*** create_file is about to be performed on node.id {}".format(node.id))
        for instance in node.instances:
            instance.execute_operation("file.interfaces.action.createNewFile",kwargs={'process': {'args': [file_name]}})
    else:
        for node in ctx.nodes:
            if input_str == node.type:
                ctx.logger.info( "*** create_file is about to be performed on node.id {}".format(node.id))
                for instance in node.instances:
                    instance.execute_operation("file.interfaces.action.createNewFile",kwargs={'process': {'args': [file_name]}})


    ctx.logger.info("End of create_file")
