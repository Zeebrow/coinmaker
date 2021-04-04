import configparser
import os.path
from cbpro import AuthenticatedClient
from CONSTANTS import *
########
# This file should be used by any other file that needs to import secret variables. 
# In otherwords, do not read secrets from any file but this one!
# I guess you can use the class vars to get secrets... maybe there's a way around this.
########

def get_coinbase_credentials(cb_profile_name='coinbase_sandbox'):
    d = {}
    config = configparser.ConfigParser()
    config.read(DEFAULT_SECRETS_FILEPATH)
    d['key']        = config[cb_profile_name]['api_key']
    d['b64secret']  = config[cb_profile_name]['api_secret']
    d['passphrase'] = config[cb_profile_name]['api_password']
    d['api_url']    = config[cb_profile_name]['api_url']
    return d

def get_influxdb_credentials():
    creds = {}
    config = configparser.ConfigParser()
    config.read(DEFAULT_SECRETS_FILEPATH)
    creds['host']       = config['influxdb']['host']
    creds['port']       = config['influxdb']['port']
    creds['username']   = config['influxdb']['username']
    creds['password']   = config['influxdb']['password']
    # creds['database']         = config['influxdb']['database']
    return creds