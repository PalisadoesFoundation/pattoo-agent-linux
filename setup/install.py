#!/usr/bin/env python3
"""Script to install the pattoo linux agent."""
from inspect import ismethod
import textwrap
import argparse
import sys
import os
import pwd
import getpass
# Set up python path
EXEC_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
_EXPECTED = '{0}pattoo-agent-linux{0}setup'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.append(ROOT_DIR)
    # Set pattoo config dir if it had not been set already
    try:
        os.environ['PATTOO_CONFIGDIR']
    except KeyError:
        os.environ['PATTOO_CONFIGDIR'] = '/etc/pattoo'
else:
    print('''\
This script is not installed in the "{}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from _pattoo_agent_linux import shared, checks

# Attempt to import pattoo shared
DEFAULT_PATH = '''\
{}/.local/lib/pattoo/site-packages'''.format(os.path.expanduser('~'))


class _Parser(argparse.ArgumentParser):
    """Class gathers all CLI information."""

    def error(self, message):
        """Override the default behavior of the error method.

        Will print the help message whenever the error method is triggered.

        Args:
            None

        Returns:
            _args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        sys.stderr.write('\nERROR: {}\n\n'.format(message))
        self.print_help()
        sys.exit(2)


class Parser():
    """Class gathers all CLI information."""

    def __init__(self, additional_help=None):
        """Intialize the class."""
        # Create a number of here-doc entries
        if additional_help is not None:
            self._help = additional_help
        else:
            self._help = ''

    def args(self):
        """Return all the CLI options.

        Args:
            None

        Returns:
            _args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        # Initialize key variables
        width = 80

        # Header for the help menu of the application
        parser = _Parser(
            description=self._help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='action')

        # Parse "install", return object used for parser
        _Install(subparsers, width=width)

        # Install help if no arguments
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        # Return the CLI arguments
        _args = parser.parse_args()

        # Return our parsed CLI arguments
        return (_args, parser)


class _Install():
    """Class gathers all CLI 'install' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables for normal installation
        install_help = '''\
Install pattoo linux agent. Type install --help to see additional arguments'''
        install_parser = subparsers.add_parser(
            'install',
            help=textwrap.fill(install_help, width=width)
        )

        # Add subparser
        self.subparsers = install_parser.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        self._execute_methods(width=width)

    def all(self, width=80):
        """CLI command to install all pattoo components.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'all',
            help=textwrap.fill('Install all pattoo components', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')

    def pip(self, width=80):
        """CLI command to install the necessary pip3 packages.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'pip',
            help=textwrap.fill('Install pip packages', width=width)
        )

        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')

    def configuration(self, width=80):
        """CLI command to configure pattoo.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        _ = self.subparsers.add_parser(
            'configuration',
            help=textwrap.fill('Configure the pattoo linux agent', width=width)
        )

    def systemd(self, width=80):
        """CLI command to install and start the system daemons.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        _ = self.subparsers.add_parser(
            'systemd',
            help=textwrap.fill('Install and run system daemons', width=width)
        )

    def _execute_methods(self, width=80):
        """Execute class methods.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)


def get_pattoo_home():
    """Retrieve home directory for pattoo user.

    Args:
        None

    Returns:
        The home directory for the pattoo user

    """
    if shared.root_check() is True:
        try:
            # No exception will be thrown if the pattoo user exists
            pattoo_home = pwd.getpwnam('pattoo').pw_dir
        # Set defaults if pattoo user doesn't exist
        except KeyError:
            pattoo_home = '/home/pattoo'

        # Ensure that the pattoo home directory is not set to non-existent
        if pattoo_home == '/nonexistent':
            pattoo_home = '/home/pattoo'

    return pattoo_home


def main():
    """Pattoo CLI script.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    _help = 'This program is the CLI interface to configuring the linux agent'
    template_dir = os.path.join(ROOT_DIR, 'setup/systemd/system')
    daemon_list = [
                    'pattoo_agent_linux_autonomousd',
                    'pattoo_agent_linux_spoked',
                    'pattoo_agent_linux_hubd'
                ]

    # Perform checks
    checks.installation_checks()
    checks.pattoo_shared_check()
    checks.venv_check()
    # Process the CLI
    _parser = Parser(additional_help=_help)
    (args, parser) = _parser.args()

    # Import packages that depend on pattoo shared
    from _pattoo_agent_linux import configure
    from pattoo_shared.installation import packages, systemd, environment

    # Set up essentials for creating the virtualenv
    pattoo_home = get_pattoo_home()
    venv_dir = os.path.join(pattoo_home, 'pattoo-venv')
    if getpass.getuser() != 'travis':
        environment.environment_setup(venv_dir)
    venv_interpreter = os.path.join(venv_dir, 'bin/python3')
    installation_dir = '{} {}'.format(venv_interpreter, ROOT_DIR)
    # Installs all linux agent components
    if args.action == 'install':
        if args.qualifier == 'all':
            print('Installing everything')
            configure.install(daemon_list, pattoo_home)
            packages.install(ROOT_DIR, venv_dir, args.verbose)
            systemd.install(daemon_list=daemon_list,
                            template_dir=template_dir,
                            installation_dir=installation_dir)

        # Sets up configuration for linux agent
        elif args.qualifier == 'configuration':
            print('Installing configuration')
            configure.install(daemon_list, pattoo_home)

        # Installs necessary pip packages
        elif args.qualifier == 'pip':
            print('Installing pip packages')
            packages.install(ROOT_DIR, venv_dir, args.verbose)

        # Installs and runs system daemons
        elif args.qualifier == 'systemd':
            print('Installing and running system daemons')
            systemd.install(daemon_list=daemon_list,
                            template_dir=template_dir,
                            installation_dir=installation_dir)

        else:
            parser.print_help(sys.stderr)
            sys.exit(1)

        # Done
        print('Done')


if __name__ == '__main__':
    # Ensure appropriate conditions are set for the installation
    main()
