import logging
from influxdb import InfluxDBClient
from cm_secrets import get_influxdb_credentials

log = logging.getLogger(__name__)

class DBClient(InfluxDBClient):
    def __init__(self):
        super().__init__(**get_influxdb_credentials())
        log.debug("Created DBClient.")