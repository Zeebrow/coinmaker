import os

DEFAULT_SECRETS_FILEPATH = ''
DEFAULT_CONFIG_FILEPATH = ''

if os.name == 'nt':
    DEFAULT_SECRETS_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\secrets'
    DEFAULT_CONFIG_FILEPATH = 'C:\\Users\\MikeAdmin\\Documents\\Python\\Projects\\coinmaker\\etc\\coinmaker.conf'

elif os.name == 'posix':
    pass

else:
    print(f'OS "{os.name}" not supported!')
    exit(1)
