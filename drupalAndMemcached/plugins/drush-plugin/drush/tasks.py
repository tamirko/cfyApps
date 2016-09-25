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

import json
import time

import requests

# ctx is imported and used in operations
from cloudify.workflows import ctx

# put the workflow decorator on any function that is a task
from cloudify.decorators import workflow
import os

@workflow
def install_project(project_name, **kwargs):
    ctx.logger.info("install_project {}".format(project_name))

    # I can use this instead ,but for the exercise I used something else
    # node = ctx.get_node('drupal_app')

    for node in ctx.nodes:
        if node.id == 'drupal_app':
            ctx.logger.info("install_project is about to exec on node.id {}".format(node.id))
            # See docs http://getcloudify.org/guide/3.1/plugin-script.html
            for instance in node.instances:
                instance.execute_operation("drupal.interfaces.action.install_project",
                                           kwargs={'process': {'args': [project_name]}})

    ctx.logger.info("End of install_project")


def _send_slack_message(incoming_slack_webhook, channel, sender_name, msg, **kwargs):
    headers = {'Content-type': 'application/json', }
    payload = json.dumps({"channel": channel,"username": sender_name,"text": msg})
    requests.post(incoming_slack_webhook, headers=headers, data=payload, )


def _get_slack_message(variable_name, variable_value):
    if "theme_default" == variable_name:
        msg = "Site's theme has changed to :'{0}'".format(variable_value)
    elif variable_name == "maintenance_mode" :
        if variable_value == "1":
            msg = "Important: Site is now in maintenance mode"
        else:
            msg = "Important: Site is now active. It's no longer in maintenance mode"
    else:
        msg = "{0}'s value has been set to '{0}'".format(variable_name, variable_value)

    return msg


@workflow
def set_variable(variable_name, variable_value, **kwargs):
    variable_value = str(variable_value)
    ctx.logger.info("set_variable variable_name is  {}".format(variable_name))
    ctx.logger.info("set_variable variable_value is {}".format(variable_value))

    msg = _get_slack_message(variable_name, variable_value)

    for node in ctx.nodes:
        if node.id == 'drupal_app':
            ctx.logger.info("set_variable is about to exec on node.id {}".format(node.id))
            # See docs http://getcloudify.org/guide/3.1/plugin-script.html
            for instance in node.instances:
                instance.execute_operation("drupal.interfaces.action.set_variable",
                                           kwargs={'process': {'args': [variable_name, variable_value]}})
            incoming_slack_webhook = node.properties['incoming_slack_webhook']
            ctx.logger.info("incoming_slack_webhook url is {}".format(incoming_slack_webhook))
            _send_slack_message(incoming_slack_webhook, "#operations", ctx.deployment.id , msg)

    ctx.logger.info("End of set_variable")