import os
from pattoo_shared.installation import configure, shared
from pattoo_shared import files


def install():
    """Start configuration process.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    if os.environ.get('PATTOO_CONFIGDIR') is None:
        os.environ['PATTOO_CONFIGDIR'] = '{0}etc{0}pattoo'.format(os.sep)
    config_directory = os.environ.get('PATTOO_CONFIGDIR')

    config_dict = {
        'pattoo_agent_linux_spoked': {
            'polling_interval': 300,
            'ip_listen_address': '127.0.0.1',
            'ip_bind_port': 5000
        }
    }

    # Attempt to create configuration directory
    files.mkdir(config_directory)

    # Create the pattoo user and group
    configure.create_user('pattoo', '/nonexistent', ' /bin/false', True)

    # Attempt to change the ownership of the configuration directory
    shared.chown(config_directory)

    config_file = configure.pattoo_config(
                                        'pattoo_agent_linux_spoked',
                                        config_directory,
                                        config_dict)

    configure.check_config(config_file, config_dict)
