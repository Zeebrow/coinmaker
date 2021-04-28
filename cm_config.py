import configparser
import sys
import logging
import os
import CONSTANTS as C
import app_config

log = logging.getLogger(__name__)

class AppConfig(object):
    def __init__(self, config_file=C.DEFAULT_CONFIG_FILEPATH):
        self.config_file = config_file
        try:
            os.stat(config_file)
        except FileNotFoundError:
            log.critical(f"Could not find {config_file}! App exits.")
            raise
        config = configparser.ConfigParser()
        config.read(config_file)
        self._datbase = config['app']['influxdb_database_name']
        self._log_level = config['app']['log_level']
    
    @property
    def database(self):
        return self._datbase

    @property
    def log_level(self):
        _levels ={
            'CRITICAL': logging.CRITICAL,
            'FATAL': logging.FATAL,
            'ERROR': logging.ERROR,
            'WARN': logging.WARNING,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET,
        } 
        return _levels[self._log_level.upper()]



if __name__ == '__main__':
    conf = AppConfig()
    print(conf.database)
    print(conf.log_level)

