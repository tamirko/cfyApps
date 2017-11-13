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

USE_EXTERNAL_RESOURCE = 'use_external_resource'
system_prefix = "{0} ".format("-"*4)


def _print_node_name(prefix_text, suffix_text, **kwargs):
    current_node_name = ctx.node.name
    ctx.logger.info("{0}{1}{2}{3}".format(system_prefix, prefix_text, current_node_name, suffix_text))
    return current_node_name


def _random_alphanumeric(output_length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(output_length))


def _use_external_resource(**kwargs):
    if USE_EXTERNAL_RESOURCE in ctx.node.properties:
        curr_use_external_resource = ctx.node.properties[USE_EXTERNAL_RESOURCE]
        return curr_use_external_resource
    return False


@operation
def start_component(device_type, **kwargs):
    component_name = _print_node_name("Starting component: ", "", **kwargs)

    rt = ctx.instance.runtime_properties
    rt["device_type"] = device_type
    ctx.logger.info("{0}{1} device_type: {2}".format(system_prefix, component_name, device_type))

    component_type = ctx.node.properties.get('component_type')
    ctx.logger.info("{0}{1} component_type: {2}".format(system_prefix, component_name, component_type))

    time.sleep(1)
    ctx.logger.info("{0}{1} Generating a component ID...".format(system_prefix, component_name))
    component_id = "COMPONENT_{0}".format(_random_alphanumeric(16))
    rt["component_id"] = component_id
    time.sleep(1)
    ctx.logger.info("{0}{1} component ID: {2}".format(system_prefix, component_name, component_id))


@operation
def stop_component(**kwargs):
    _print_node_name("Stopping component: ", "", **kwargs)


@operation
def create_device(**kwargs):
    if _use_external_resource(**kwargs):
        device_name = ctx.node.name
        device_id = ctx.node.id
        ctx.logger.info("{0} {1} {2} already exists. Skipping creation".
                        format(system_prefix, "Device", device_name, device_id))
        return

    _print_node_name("Creating device: ", "...", **kwargs)


@operation
def start_device(device_type, bandwidth, global_device_id=None, **kwargs):
    if _use_external_resource(**kwargs):
        return

    device_name = _print_node_name("Starting device: ", "", **kwargs)

    rt = ctx.instance.runtime_properties
    rt["device_type"] = device_type

    ctx.logger.info("{0}{1} device_type: {2}".format(system_prefix, device_name, device_type))
    ctx.logger.info("{0}{1} bandwidth: {2}".format(system_prefix, device_name, bandwidth))

    global_device_type = ctx.node.properties.get('global_device_type')
    ctx.logger.info("{0}{1} global_device_type: {2}".format(system_prefix, device_name, global_device_type))

    if global_device_id is not None:
        ctx.logger.info("{0}{1} global_device_id: {2}".format(system_prefix, device_name, global_device_id))
        rt["global_device_id"] = global_device_id
    else:
        ctx.logger.info("{0}{1} global_device_id is None".format(system_prefix, device_name))

    time.sleep(1)
    ctx.logger.info("{0}{1} Generating a device ID...".format(system_prefix, device_name))
    device_id = "DEVICE_{0}".format(_random_alphanumeric(16))
    rt["device_id"] = device_id
    time.sleep(1)
    ctx.logger.info("{0}{1} device ID: {2}".format(system_prefix, device_name, device_id))


@operation
def stop_device(**kwargs):
    _print_node_name("Stopping device: ", "", **kwargs)






