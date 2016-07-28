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
'''Cloudify Fortinet plugin package config'''

from os import environ, path
import logging
from subprocess import Popen, PIPE
from setuptools import setup
from setuptools.command.install import install

logging.basicConfig(level=logging.DEBUG)


def install_package(pip_path, pkg):
    '''Install a required package'''
    proc = Popen([pip_path, 'install', pkg], stderr=PIPE)
    err = proc.communicate()
    if proc.returncode:
        raise Exception('Installing Python package "{0}" failed: {1}'
                        .format(pkg, err))


def uninstall_package(pip_path, pkg):
    '''Uninstall a required package'''
    proc = Popen([pip_path, 'uninstall', pkg, '-y'], stderr=PIPE)
    err = proc.communicate()
    if proc.returncode:
        raise Exception('Uninstalling Python package "{0}" failed: {1}'
                        .format(pkg, err))


def install_requirements():
    '''Install required Python packages'''
    logger = logging.getLogger('setup.py')

    ureqs = ['paramiko']
    # This is needed due to an SSH bug in FortiGate and latest Paramiko (Fabric)
    reqs = ['https://github.com/01000101/paramiko/archive/v1.17-fortigate.zip']

    pip_win_path = path.join(environ.get('VIRTUAL_ENV'), 'Scripts/pip.exe')
    pip_nix_path = path.join(environ.get('VIRTUAL_ENV'), 'bin/pip')
    pip_path = pip_nix_path if path.exists(pip_nix_path) else pip_win_path

    logger.info('Using PIP: %s', pip_path)
    for ureq in ureqs:
        logger.info('Uninstalling Python package "%s"', ureq)
        uninstall_package(pip_path, ureq)
    for req in reqs:
        logger.info('Installing Python package "%s"', req)
        install_package(pip_path, req)


class CustomInstall(install):
    '''Custom install'''
    def run(self):
        install_requirements()
        install.run(self)


setup(
    name='cloudify-fortinet-plugin',
    version='1.1',
    license='LICENSE',
    packages=[
        'fortigate',
        'fortigate.firewall'
    ],
    cmdclass={'install': CustomInstall},
    description='A Cloudify plugin for Fortinet NFV orchestration',
    install_requires=[
        'cloudify-plugins-common>=3.4'
    ]
)
