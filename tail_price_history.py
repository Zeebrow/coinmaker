import cm_secrets
import cbpro
from influxdb import InfluxDBClient
from datetime import datetime
from time import time
import logging
logger = logging.getLogger(__name__)
auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials('coinbase_secrets'))


idb_order_skel = {
    "measurement": "btc_price",
    "tags": {
        "id": "",
        "product_id": "",
        "profile_id": "",
        "side": "",
        "funds": 0.0,
        "specified_funds": 0.0,
        "type": "",
        "post_only": None,
        "created_at": "1990-03-11T08:26:02.122069Z",
        "done_at": "1990-03-11T08:26:02.132Z",
        "done_reason": "",
        "fill_fees": 0.0,
        "filled_size": 0.0,
        "executed_value": 0.0,
        "status": "",
        "settled": None
    },
    "time": "1990-03-11T08:26:02Z",
    "fields": {
        "one": 1
    }
}

cb_order_skel = {
    "id": "", "product_id": "", "profile_id": "", "side": "",
    "funds": 0.0, "specified_funds": 0.0, "type": "", "post_only": None, 
    "created_at": "", "done_at": "", "done_reason": "", "fill_fees": 0.0,
    "filled_size": 0.0, "executed_value": 0.0, "status": "", "settled": None
}

class IDB_Order():
    order_skel = {
        "id": "", "product_id": "", "profile_id": "", "side": "",
        "funds": 0.0, "specified_funds": 0.0, "type": "", "post_only": None, 
        "created_at": "", "done_at": "", "done_reason": "", "fill_fees": 0.0,
        "filled_size": 0.0, "executed_value": 0.0, "status": "", "settled": None
    }
    def __init__(self):
        # self._id = ""
        # self.product_id = ""
        # self.profile_id = ""
        # self.side = ""
        # self.funds = 0.0
        # self.specified_funds = 0.0
        # self._type = ""
        # self.post_only = None
        # self.created_at = ""
        # self.done_at = ""
        # self.done_reason = ""
        # self.fill_fees = 0.0
        # self.filled_size = 0.0
        # self.executed_value = 0.0
        # self.status = ""
        # self.settled = None
        self.order = self.order_skel

    def get_id(self):
        return self.order['id']

    def set_id(self, _id):
        self.order['id'] = _id
        return self.order['id']

    def show(self):
        return self.order



creds = cm_secrets.get_influxdb_credentials()
client = InfluxDBClient(**creds)
influxdb_user = creds['username']
influxdb_user_pw = creds['password']
default_db_list = ['cb_tx_history']
def init_influxdb(db_create_list: list, clean=False):
    pass
    # for db in db_create_list:
    #     default_db_list.append(db)
    # if clean:
    #     clean_db()
    # # create user if not exists
    # client.create_user(influxdb_user)
    # client.set_user_password(influxdb_user_pw)
    # # create db if not exists
    # client.create_database(db)
    # # grant privileges on db to user
    # client.grant_privilege('all', db, influxdb_user)

def clean_db(db):
    pass
    # # drop db
    # client.drop_database(db)
    # # remove user
    # clent.drop_user(influxdb_user)

def idb_commit_cb_order(order: dict, database='test_order_history'):
    """Commit a single order to InfluxDB"""

    if set(cb_order_skel.keys()) != set(order.keys()):
        print("Malformed order!")
        return False
    _commit = idb_order_skel
    _commit['measurement']      = order['product_id'].lower().replace("-","_") + "_price"
    _commit['tags']             = order
    _commit['time']             = order['done_at']
    _commit['fields']['one']    = 1
    _cl = []
    _cl.append(_commit)
    # print("DEBUG: committing order to influxdb...")
    # print(f"DEBUG: {_cl}")
    dbc = InfluxDBClient(**creds) 
    dbc.switch_database(database)
    dbc.write_points(_cl)
    logger.debug(f"Committed order {order['id']}.")
    dbc.close()

def idb_commitbulk_cb_order(orders: list, database='test_order_history'):
    for d in orders:
        if set(cb_order_skel.keys()) != set(d.keys()):
            print("Malformed order!")
            return False
    print(f"DEBUG: committing {len(orders)} orders...")
    _cl = []
    for d in orders:
        _commit = idb_order_skel
        _commit['measurement']      = d['product_id'].lower().replace("-","_") + "_price"
        _commit['tags']             = d
        _commit['time']             = d['done_at']
        _commit['fields']['one']    = 1
        _cl.append(_commit)
        # print("DEBUG: committing order to influxdb...")
        # print(f"DEBUG: {_cl}")
    dbc = InfluxDBClient(**creds) 
    dbc.switch_database(database)
    dbc.write_points(_cl)
    dbc.close()

def save_datapoint():
    pass