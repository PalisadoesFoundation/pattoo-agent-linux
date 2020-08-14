#!/usr/bin/env python3
"""Class used to create the configuration file used for unittesting.

NOTE!! This script CANNOT import any pattoo-agent-linux libraries. Doing so risks
libraries trying to access a configuration or configuration directory that
doesn't yet exist. This is especially important when running cloud based
automated tests such as 'Travis CI'.

"""

# Standard imports
from __future__ import print_function
import tempfile
import os
import yaml

# Pattoo imports
from pattoo_shared import log
from pattoo_shared.configuration import BaseConfig, _config_reader, search
from pattoo_shared.constants import PATTOO_API_WEB_PREFIX
from pattoo_shared import url


class WebConfig(BaseConfig):
    """Class gathers all configuration information relating to pattoo web.
    The configuration values for this class will be written to pattoo_webd.yaml
    """

    def __init__(self):
        """Initialize the class.
        Args:
            None
        Returns:
            None
        """
        # Get the configuration
        BaseConfig.__init__(self)
        self._base_yaml_configuration = _config_reader('pattoo.yaml')

    def web_api_ip_address(self):
        """Get web_api_ip_address.
        Args:
            None
        Returns:
            result: result
        """
        # Initialize key variables
        key = 'pattoo_web_api'
        sub_key = 'ip_address'

        # Get result
        result = search(
            key, sub_key, self._base_yaml_configuration, die=True)
        return result

    def web_api_ip_bind_port(self):
        """Get web_api_ip_bind_port.
        Args:
            None
        Returns:
            result: result
        """
        # Initialize key variables
        key = 'pattoo_web_api'
        sub_key = 'ip_bind_port'

        # Get result
        intermediate = search(
            key, sub_key, self._base_yaml_configuration, die=False)
        if intermediate is None:
            result = 20202
        else:
            result = int(intermediate)
        return result

    def web_api_server_url(self, graphql=True):
        """Get pattoo server's remote URL.
        Args:
            agent_id: Agent ID
        Returns:
            result: URL.
        """
        # Create the suffix
        if bool(graphql) is True:
            suffix = '/graphql'
        else:
            suffix = '/rest/data'

        # Return
        _ip = url.url_ip_address(self.web_api_ip_address())
        result = (
            'http://{}:{}{}{}'.format(
                _ip,
                self.web_api_ip_bind_port(),
                PATTOO_API_WEB_PREFIX, suffix))
        return result


class UnittestConfig():
    """Creates configuration for testing."""

    def __init__(self):
        """Initialize the class."""
        # Initialize GLOBAL variables
        config_suffix = '.pattoo-agent-linux-unittests{}config'.format(os.sep)
        self._config_directory = (
            '{}{}{}'.format(os.environ['HOME'], os.sep, config_suffix))

        # Make sure the environmental variables are OK
        _environment(self._config_directory)

        # Set global variables
        self._log_directory = tempfile.mkdtemp()
        self._cache_directory = tempfile.mkdtemp()
        self._daemon_directory = tempfile.mkdtemp()

        # Make sure the configuration directory is OK
        if os.path.isdir(self._config_directory) is False:
            os.makedirs(self._config_directory, mode=0o750, exist_ok=True)

        self._config = {
            'pattoo': {
                'pattoo': {
                    'log_directory': self._log_directory,
                    'log_level': 'debug',
                    'language': 'abc',
                    'cache_directory': self._cache_directory,
                    'daemon_directory': self._daemon_directory,
                },
                'pattoo_agent_api': {
                    'ip_address': '127.0.0.11',
                    'ip_bind_port': 50001,
                },
                'pattoo_web_api': {
                    'ip_address': '127.0.0.12',
                    'ip_bind_port': 50002,
                }
            },
            'pattoo_agent_linux_autonomousd': {
                'polling_interval': 80
                },
            'pattoo_agent_linux_spoked': {
                'ip_listen_address': '127.0.0.1',
                'ip_bind_port': 5000
                },
            'pattoo_agent_linux_hubd': {
                'polling_interval': 98,
                'ip_targets': [
                    {'ip_address': '127.0.0.1',
                     'ip_bind_port': 5000}]
                },
        }

        self._agent_config = {
            'pattoo_agent_api': {
                'ip_address': '127.0.0.11',
                'ip_bind_port': 50001,
            },

            'encryption': {
                'agent_email': 'test_agent@example.org'
            }
        }

    def create(self):
        """Create a good config and set the PATTOO_CONFIGDIR variable.

        Args:
            None

        Returns:
            self.config_directory: Directory where the config is placed

        """
        # Initialize key variables
        agent_config = '{}{}pattoo_agent.yaml'.format(
                                            self._config_directory, os.sep)
        # Write good_config to file
        for key, config_ in sorted(self._config.items()):
            config_file = (
                '{}{}{}.yaml'.format(self._config_directory, os.sep, key))
            with open(config_file, 'w') as f_handle:
                yaml.dump(config_, f_handle, default_flow_style=False)

        # Write to pattoo_agent.yaml
        try:
            f_handle = open(agent_config, 'w')
        except PermissionError:
            log.log2die(50500, '''\
Insufficient permissions for creating the file:{}'''.format(f_handle))
        else:
            with f_handle:
                yaml.dump(self._agent_config, f_handle, default_flow_style=False)
        # Return
        return self._config_directory

    def cleanup(self):
        """Remove all residual directories.

        Args:
            None

        Returns:
            None

        """
        # Delete directories
        directories = [
            self._log_directory,
            self._cache_directory,
            self._daemon_directory,
            self._config_directory]
        for directory in directories:
            _delete_files(directory)


def _delete_files(directory):
    """Delete all files in directory."""
    # Cleanup files in temp directories
    filenames = [filename for filename in os.listdir(
        directory) if os.path.isfile(
            os.path.join(directory, filename))]

    # Get the full filepath for the cache file and remove filepath
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        os.remove(filepath)

    # Remove directory after files are deleted.
    os.rmdir(directory)


def _environment(config_directory):
    """Make sure environmental variables are OK.

    Args:
        config_directory: Directory with the configuration

    Returns:
        None

    """
    # Create a message for the screen
    screen_message = ('''
The PATTOO_CONFIGDIR is set to the wrong directory. Run this command to do \
so:

$ export PATTOO_CONFIGDIR={}

Then run this command again.
'''.format(config_directory))

    # Make sure the PATTOO_CONFIGDIR environment variable is set
    if 'PATTOO_CONFIGDIR' not in os.environ:
        log.log2die_safe(51023, screen_message)

    # Make sure the PATTOO_CONFIGDIR environment variable is set correctly
    if os.environ['PATTOO_CONFIGDIR'] != config_directory:
        log.log2die_safe(51024, screen_message)

    # Update message
    screen_message = ('''{}

PATTOO_CONFIGDIR is incorrectly set to {}

'''.format(screen_message, os.environ['PATTOO_CONFIGDIR']))

    # Make sure the PATTOO_CONFIGDIR environment variable is set to unittest
    if 'unittest' not in os.environ['PATTOO_CONFIGDIR']:
        log_message = (
            'The PATTOO_CONFIGDIR is not set to a unittest directory')
        log.log2die_safe(51025, log_message)
