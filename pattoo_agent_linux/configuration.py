#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config
from pattoo_shared import files
from pattoo_agent_linux import (
    PATTOO_AGENT_LINUX_SPOKED, PATTOO_AGENT_LINUX_HUBD, PATTOO_AGENT_LINUX_AUTONOMOUSD)


class ConfigSpoked(Config):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_LINUX_SPOKED constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate inheritance
        Config.__init__(self)

        # Get the configuration
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_LINUX_SPOKED)
        self._agent_config = files.read_yaml_file(config_file)

    def ip_listen_address(self):
        """Get ip_listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_LINUX_SPOKED
        sub_key = 'ip_listen_address'
        result = configuration.search(
            key, sub_key, self._agent_config, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def ip_bind_port(self):
        """Get ip_bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_LINUX_SPOKED
        sub_key = 'ip_bind_port'
        intermediate = configuration.search(
            key, sub_key, self._agent_config, die=False)

        # Default to 6000
        if intermediate is None:
            result = 5000
        else:
            result = int(intermediate)
        return result


class ConfigHubd(Config):
    """Class for PATTOO_AGENT_LINUX_HUBD configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_LINUX_HUBD constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate inheritance
        Config.__init__(self)

        # Get the configuration
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_LINUX_HUBD)
        self._agent_config = files.read_yaml_file(config_file)

    def ip_targets(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_LINUX_HUBD
        sub_key = 'ip_targets'
        result = configuration.search(
            key, sub_key, self._agent_config, die=True)
        return result

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_LINUX_HUBD
        sub_key = 'polling_interval'
        intermediate = configuration.search(
            key, sub_key, self._agent_config, die=False)

        # Default to 300
        if bool(intermediate) is False:
            result = 300
        else:
            result = abs(int(intermediate))
        return result


class ConfigAutonomousd(Config):
    """Class for PATTOO_AGENT_LINUX_AUTONOMOUSD configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_LINUX_AUTONOMOUSD constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate inheritance
        Config.__init__(self)

        # Get the configuration
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_LINUX_AUTONOMOUSD)
        self._agent_config = files.read_yaml_file(config_file)

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_LINUX_AUTONOMOUSD
        sub_key = 'polling_interval'
        intermediate = configuration.search(
            key, sub_key, self._agent_config, die=False)

        # Default to 300
        if bool(intermediate) is False:
            result = 300
        else:
            result = abs(int(intermediate))
        return result
