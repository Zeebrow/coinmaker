import os, sys
from pathlib import Path
import json
import logging

log = logging.getLogger(__name__)


user = os.getlogin()
log.debug(f"Running {json.dumps({'program': sys.argv[0], 'as_user': user})}")
log.debug(f"OS type {os.name}")

homedir = ['/home/'+os.getlogin()+'/' if os.name == 'posix' else '/Users/'+os.getlogin()+'/']

DEFAULT_SECRETS_FILEPATH = ''
DEFAULT_CONFIG_FILEPATH = ''
DEFAULT_DB_FILEPATH = ''
DEFAULT_LOGS_FILEPATH = ''

if os.name == 'nt':
    #_default_secrets_filepath = homedir + str(Path('Documents/Python/Projects/coinmaker/secrets') )
    #DEFAULT_SECRETS_FILEPATH = homedir + Path('Documents/Python/Projects/coinmaker/secrets')
    DEFAULT_SECRETS_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\secrets'
    DEFAULT_CONFIG_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\etc\\coinmaker.conf'
    DEFAULT_DB_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\var\\sqlite3db'
    DEFAULT_LOG_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\logs\\coinmaker.log'
elif os.name == 'posix':
    install_dir = '/opt/coinmaker/'
    config_dir = '/etc/opt/coinmaker/'
    secrets_dir = homedir + '.dcabot_secrets'
    DEFAULT_SECRETS_FILEPATH = homedir + '.dcabot_secrets'
    DEFAULT_CONFIG_FILEPATH = '/etc/opt/coinmaker/'
    #DEFAULT_CONFIG_FILEPATH = '/home/mike/bin/coinmaker/coinmaker/etc/coinmaker.conf'
    DEFAULT_DB_FILEPATH = '/home/mike/bin/coinmaker/coinmaker/var/sqlitedb'
    DEFAULT_LOG_FILEPATH = '/home/mike/bin/coinmaker/coinmaker/logs/coinmaker.log'
    pass

else:
    log.critical(f"OS '{os.name}' not supported! (Supported versions are 'nt' or 'posix')")
    exit(1)

def check_config():
    pass

if __name__ == '__main__':
    logging.info(f"{__name__}")
    check_config()