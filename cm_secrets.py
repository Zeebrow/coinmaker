import configparser
import os.path
from cbpro import AuthenticatedClient
import CONSTANTS as C
########
# This file should be used by any other file that needs to import secret variables. 
# In otherwords, do not read secrets from any file but this one!
# I guess you can use the class vars to get secrets... maybe there's a way around this.
########

def get_coinbase_credentials(profile='coinbase_sandbox'):
    d = {}
    secrets= configparser.ConfigParser()
    secrets.read(C.DEFAULT_SECRETS_FILEPATH)
    d['key']        = secrets[profile]['api_key']
    d['b64secret']  = secrets[profile]['api_secret']
    d['passphrase'] = secrets[profile]['api_password']
    d['api_url']    = secrets[profile]['api_url']
    return d

def get_influxdb_credentials():
    creds = {}
    secrets= configparser.ConfigParser()
    secrets.read(C.DEFAULT_SECRETS_FILEPATH)
    creds['host']       = secrets['influxdb']['host']
    creds['port']       = secrets['influxdb']['port']
    creds['username']   = secrets['influxdb']['username']
    creds['password']   = secrets['influxdb']['password']
    # creds['database']         = secrets['influxdb']['database']
    return creds