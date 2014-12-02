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
from cloudify import ctx

# put the workflow decorator on any function that is a task
from cloudify.decorators import workflow
import os


@workflow
def drush_download_module(ctx,module_name, **kwargs):    
	ctx.logger.info("xxx In drush_download_module")
	ctx.logger.info("xxx drush_download_module: deployment_id is {}".format(ctx.deployment_id))

	# I can use this instead ,but for the execise I used something else 
	# node = ctx.get_node('drupal_app')
	
	
    for node in ctx.nodes:
        ctx.logger.info("xxx drush_download_module node.type_hierarchy is {}".format(node.type_hierarchy))
        ctx.logger.info("xxx drush_download_module node.id is {}".format(node.id))
        if node.id == 'drupal_app':
            ctx.logger.info("xxx about to exec node.id {}".format(node.id))
			# See docs http://getcloudify.org/guide/3.1/plugin-script.html
            for instance in node.instances:		
                instance.execute_operation('drupal.interfaces.action.download_module', 
					kwargs={'process': {'args': [module_name]}})		
        else:
           ctx.logger.info("xxx In drush_download_module")			        
			
	ctx.logger.info("xxx End of drush_download_module")
	
@workflow
def drush_enable_module(ctx,module_name, **kwargs):    
	ctx.logger.info("xxx In drush_enable_module")
	ctx.logger.info("xxx drush_enable_module: deployment_id is {}".format(ctx.deployment_id))

    for node in ctx.nodes:
        ctx.logger.info("xxx drush_enable_module node.type_hierarchy is {}".format(node.type_hierarchy))
        ctx.logger.info("xxx drush_enable_module node.id is {}".format(node.id))
        if node.id == 'drupal_app':
            ctx.logger.info("xxx about to exec node.id {}".format(node.id))
            for instance in node.instances:		
                instance.execute_operation('drupal.interfaces.enable_module',module_name=module_name)
        else:
           ctx.logger.info("xxx In drush_enable_module")			        
			
	ctx.logger.info("xxx End of drush_enable_module")	