import os

DEFAULT_SECRETS_FILEPATH = ''
DEFAULT_CONFIG_FILEPATH = ''
DEFAULT_DB_FILEPATH = ''
DEFAULT_LOGS_FILEPATH = ''

if os.name == 'nt':
    DEFAULT_SECRETS_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\secrets'
    DEFAULT_CONFIG_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\etc\\coinmaker.conf'
    DEFAULT_DB_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\var\\sqlite3db'
    DEFAULT_LOG_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\logs\\coinmaker.log'
elif os.name == 'posix':
    DEFAULT_SECRETS_FILEPATH = '/home/mike/.dcabot_secrets'
    DEFAULT_CONFIG_FILEPATH = '/home/mike/bin/coinmaker/coinmaker/etc/coinmaker.conf'
    DEFAULT_DB_FILEPATH = '/home/mike/bin/coinmaker/coinmaker/var/sqlitedb'
    DEFAULT_LOG_FILEPATH = '/home/mike/bin/coinmaker/coinmaker/logs/coinmaker.log'
    pass

else:
    print(f'OS "{os.name}" not supported!')
    exit(1)
