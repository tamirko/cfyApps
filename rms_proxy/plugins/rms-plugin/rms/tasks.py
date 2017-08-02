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
import random

@workflow
def update_resource_in_rms(resource_type, quota, cost_per_unit, **kwargs):

    quota_and_price_str = "Quota: {0:,}, Unit price: ${1:,}".format(int(quota), int(cost_per_unit))
    message_to_rms = "Requesting RMS to add *{0}*. {1} ...".format(resource_type, quota_and_price_str)
    ctx.logger.info(message_to_rms)


    slack_node = ctx.get_node('slack_node')
    incoming_slack_webhook = slack_node.properties['incoming_slack_webhook']
    slack_channel_to_rms = slack_node.properties['slack_channel_to_rms']
    slack_channel_from_rms = slack_node.properties['slack_channel_from_rms']
    slack_failure_channel = slack_node.properties['slack_failure_channel']

    _send_slack_message(incoming_slack_webhook, slack_channel_to_rms, ctx.deployment.id, message_to_rms)

    OK_RESPONSE = "*OK*"
    FAILURE_RESPONSE = "{0}Failure{0}".format("`")
    #Dummy check against the RMS
    rnd_value = random.randint(1, 100)

    rms_response = OK_RESPONSE if rnd_value > 30 else FAILURE_RESPONSE
    message_from_rms = "The response from RMS for adding *{0}* is: {1}".format(resource_type, rms_response)
    _send_slack_message(incoming_slack_webhook, slack_channel_from_rms, ctx.deployment.id, message_from_rms)

    if rms_response == OK_RESPONSE:
        operations_msg = "Added *{0}* to the RMS. {1} ...".format(resource_type, quota_and_price_str)
        _send_slack_message(incoming_slack_webhook, "#operations", ctx.deployment.id, operations_msg)
    else:
        slack_failure_message = "`Failed` to add *{0}* to the RMS. {1} ...".format(resource_type, quota_and_price_str)
        _send_slack_message(incoming_slack_webhook, slack_failure_channel, ctx.deployment.id, slack_failure_message)

    ctx.logger.info("End of adding resource {0} to the RMS.".format(resource_type))


def _send_slack_message(incoming_slack_webhook, channel, sender_name, msg, **kwargs):
    headers = {'Content-type': 'application/json', }
    payload = json.dumps(
            {"channel": channel,
             "username": sender_name,
             "text": msg}
            )
    requests.post(incoming_slack_webhook, headers=headers, data=payload, )
