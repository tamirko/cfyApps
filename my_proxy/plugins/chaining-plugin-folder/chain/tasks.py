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
from cloudify import ctx
from cloudify.decorators import operation


def _print_node_name(prefix_text, suffix_text, **kwargs):
    current_node_name = ctx.node.name
    ctx.logger.info("{0} {1} {2}".format(prefix_text, current_node_name, suffix_text))


@operation
def start_element(device_type, **kwargs):
    _print_node_name("Starting element ", "", **kwargs)

    ctx.logger.info("device_type {0}".format(device_type))
    rt = ctx.instance.runtime_properties
    rt["device_type"] = device_type

    element_type = ctx.node.properties.get('element_type')
    ctx.logger.info("element_type {0}".format(element_type))

@operation
def stop_element(**kwargs):
    _print_node_name("Stopping element ", "", **kwargs)


@operation
def start_network(network_type, bandwidth, **kwargs):
    _print_node_name("Starting network ", "", **kwargs)

    ctx.logger.info("network_type: {0}".format(network_type))
    rt = ctx.instance.runtime_properties
    rt["network_type"] = network_type

    ctx.logger.info("bandwidth:    {0}".format(bandwidth))


@operation
def stop_network(**kwargs):
    _print_node_name("Stopping network ", "", **kwargs)

    rt = ctx.instance.runtime_properties
    network_type = rt["network_type"]
    ctx.logger.info("network_type: {0}".format(network_type))




