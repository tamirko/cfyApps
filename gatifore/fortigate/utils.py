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
    Fortinet.FortiGate.Utils
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Helper utilities
'''

from collections import Mapping


def dict_update(orig, updates):
    '''Recursively merges two objects'''
    orig = orig or dict()
    updates = updates or dict()
    for key, val in updates.iteritems():
        if isinstance(val, Mapping):
            orig[key] = dict_update(orig.get(key, {}), val)
        else:
            orig[key] = updates[key]
    return orig
