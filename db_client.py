import logging
from influxdb import InfluxDBClient
from cm_secrets import get_influxdb_credentials

log = logging.getLogger(__name__)

class DBClient(InfluxDBClient):
    ex_cb_order = [
        {
            "measurement": "eth-orders",
            "tags": {
                "can_filter_based_on": "True?",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": 0.64
            }
        }
    ]
    """
    Base class for authenticating an InfluxDB connection.
    Lots of random crap in here to help me learn and remember what
    influxdb commands do what.


    InfluxDB will create it's own timestamp if none provided
    """

    def __init__(self, database):
        super().__init__(**get_influxdb_credentials())
        log.debug("Created DBClient.")
        self.database = database
        
    def get_databases(self):
        return self.query('SHOW DATABASES')

    def use_database(self, db):
        #this will not work.
        self.switch_database(db)
    
    def use_user(self, user, pw):
        #this will not work
        self.switch_user(username=user, password=pw)

    def commit_cb_order(self, order: dict):
        pass

    def get_measurements(self):
        """
        Measurements = tables
        Measurements exist in a database

        In the Python client, measurements are defined from 
        within the data passed to write_points() 
        """
        pass

    def q(self, q) -> dict:
        """lol im lazy"""
        return self.query(q).raw


    def init_db_table(self, db_filepath, table):
        pass


    def nuke(self, table, db_filepath, are_you_sure=False):
        if are_you_sure:
            log.warning(f"Dropping table {table}...")

        else:
            log.info("You aren't sure you want to destroy db. Ain't gonna do it!")

if __name__ == '__main__':
    import app_class
    import json
    from order import Order
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter( '--TEST--%(asctime)s - %(name)s - %(levelname)s - %(message)s' ))
    logger.addHandler(sh)
    logger.info("BEGIN MYSTICAL JOURNEY")
    profile = 'coinbase_secrets'
    app = app_class.App('coinbase_secrets')

    o = Order.ex_order
    client = DBClient(database='premade')
    order = Order(**o)
    # for _o in order.commit():
    #     print(json.dumps(_o, indent=4))
    print(order.commitable())
    
    client.write_points( order.commitable(), database='premade')

