"""The checks necessary for a seamless installation."""
import os
import getpass
from _pattoo_agent_linux import shared


def venv_check():
    """Check if "virtualenv" is installed.

    If virtualenv is not installed it gets automatically installed to the
    user's default python path

    Args:
        None

    Returns:
        None

    """
    # Check if virtualenv is installed
    try:
        import virtualenv
    except ModuleNotFoundError:
        print('virtualenv is not installed, installing virtualenv')
        shared.run_script('pip3 install virtualenv==20.0.30')


def pattoo_shared_check():
    """Check if pattoo shared is installed.

    If pattoo shared is not installed, it gets installed to the user's
    default python path

    Args:
        None

    Returns:
        None

    """
    # Try except to install pattoo shared
    try:
        import pattoo_shared
    except ModuleNotFoundError:
        print('PattooShared is missing, installing the latest version')
        shared.run_script('pip3 install PattooShared')


def installation_checks():
    """Validate conditions needed to start installation.

    Prevents installation if the script is not run as root and prevents
    installation if script is run in a home related directory

    Args:
        None

    Returns:
        True: If conditions for installation are satisfied

    """
    # Check user
    if getpass.getuser() != 'travis':
        if shared.root_check() is False:
            shared.log('Please run the script with sudo to continue.')
        # Check installation directory
        if os.getcwd().startswith('/home'):
            shared.log('''\
You cloned the repository in a home related directory, please clone in a\
 non-home directory to continue''')
