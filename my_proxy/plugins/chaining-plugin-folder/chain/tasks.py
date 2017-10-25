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

import time
import json
import random
import string

from cloudify import ctx
from cloudify.decorators import operation

system_prefix = "{0} ".format("-"*4)


def _print_node_name(prefix_text, suffix_text, **kwargs):
    current_node_name = ctx.node.name
    ctx.logger.info("{0}{1}{2}{3}".format(system_prefix, prefix_text, current_node_name, suffix_text))
    return current_node_name


def _random_alphanumeric(output_length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(output_length))


@operation
def start_element(device_type, **kwargs):
    element_name = _print_node_name("Starting element: ", "", **kwargs)

    rt = ctx.instance.runtime_properties
    rt["device_type"] = device_type
    ctx.logger.info("{0}{1} device_type: {2}".format(system_prefix, element_name, device_type))

    element_type = ctx.node.properties.get('element_type')
    ctx.logger.info("{0}{1} element_type: {2}".format(system_prefix, element_name, element_type))

    time.sleep(1)
    ctx.logger.info("{0}{1} Generating an element ID...".format(system_prefix, element_name))
    element_id = "ELE_{0}".format(_random_alphanumeric(16))
    rt["element_id"] = element_id
    time.sleep(1)
    ctx.logger.info("{0}{1} element ID: {2}".format(system_prefix, element_name, element_id))


@operation
def stop_element(**kwargs):
    _print_node_name("Stopping element: ", "", **kwargs)


@operation
def start_network(network_type, bandwidth, **kwargs):
    network_name = _print_node_name("Starting network: ", "", **kwargs)

    rt = ctx.instance.runtime_properties
    rt["network_type"] = network_type

    ctx.logger.info("{0}{1} network_type: {2}".format(system_prefix, network_name, network_type))
    ctx.logger.info("{0}{1} bandwidth: {2}".format(system_prefix, network_name, bandwidth))

    time.sleep(1)
    ctx.logger.info("{0}{1} Generating a network ID...".format(system_prefix, network_name))
    network_id = "NET_{0}".format(_random_alphanumeric(16))
    rt["network_id"] = network_id
    time.sleep(1)
    ctx.logger.info("{0}{1} network ID: {2}".format(system_prefix, network_name, network_id))


@operation
def stop_network(**kwargs):
    _print_node_name("Stopping network: ", "", **kwargs)






