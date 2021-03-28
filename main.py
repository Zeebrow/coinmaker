import sys, json, collections
import cbpro
import cm_order, cm_secrets
import sqlite3
from CONSTANTS import *
"""
Coin Maker
Input how much $USD you want to make, and how much you are willing to invest.
Coin Maker will return a pair of limit orders: One to buy at the current market rate, and
one to limit sell so that you hit your desired make target.

Each night that DCAbot is run, Coin Maker will query for filled orders (unless cbpro calls back 
when an order is filled - maybe an email hook?). If an order made by Coin Maker will send you a
notification of how much you made!

There is an opportunity to gain market insight based on how long it takes a split to be filled,
as well as how large the split return is. 

TODO: learn about stop orders
"""
Test_Order = {
  "id": "74130f08-baac-4430-b1ec-5aee0df98379",
  "product_id": "ETH-USD",
  "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93", 
  "side": "buy",
  "funds": "9.9502487500000000",
  "specified_funds": "10.0000000000000000",
  "type": "market",
  "post_only": "false",
  "created_at": "2021-03-17T07:34:01.972518Z",
  "done_at": "2021-03-17T07:34:01.982Z", 
  "done_reason": "filled", 
  "fill_fees": "0.0497512000275000", 
  "filled_size": "0.00558165",  
  "executed_value": "9.9502400055000000", 
  "status": "done", 
  "settled": "true"
}

print("Coin Maker")
print("------------------------------------")
# for k in tt._fields:
#     print(k, '->', getattr(tt, k))
a = cm_order.Order(**Test_Order)

# a.show()
def get_account_info(cb_profile_name='coinbase_sandbox'):
    auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))
    accts = auth_client.get_accounts()
    active_accts = []
    for acct in accts:
        if float(acct['balance']) > 0:
            active_accts.append(acct)
    return active_accts

accts = get_account_info()
# print(accts)
id_btc = 'd75cd20a-dbe1-4942-b473-209ee48cffa5'
id_eth = '920c879b-c310-44b4-b61d-91e7ca18bcf3'
id_usd = 'fdaa3d1b-47c9-4fe9-b117-b250e02132e3'

accts_live = get_account_info('coinbase_secrets')
# print(accts_live)
live_id_btc = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'
live_id_eth = 'aafb8af7-a54f-496a-af0f-aa660e864104'
live_id_usd = '984037ca-36e9-4b7f-a2ee-33ee8d2fdab2'

def get_order_hist(acct_id, cb_profile_name='coinbase_sandbox'):
    """
    Used solely to get each order's id field for use in get_order_details (should return list of id's instead, w/e)
    """
    orders = []
    auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))
    h = auth_client.get_account_history(acct_id)
    for order in h:
        orders.append(order)
        with open('var\\incoming_orders.txt', 'w') as o:
            o.write(json.dumps(order, indent=4))
    return orders

orders = get_order_hist(live_id_eth, cb_profile_name='coinbase_secrets')
# for order in orders:
#     o = {
#         'id': order['details']['order_id'],
#         'product_id': order['details']['product_id'],

#     }
#     print(order)

guinea_pig_order_id = 'ce0bfa07-50a2-4a33-a639-b30afbce0983'

def get_order_details(order_id, cb_profile_name='coinbase_sandbox'):
    """
    Get details of an order, to match cm_order
    """
    auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))
    return auth_client.get_order(order_id)

o1 = get_order_details(guinea_pig_order_id, cb_profile_name='coinbase_secrets')
print(o1)

record_list = []
order_list_dict = []
for order in get_order_hist(live_id_btc, cb_profile_name='coinbase_secrets'):
    print('Getting order {}...'.format( order['details']['order_id'] ))
    h = get_order_details(order['details']['order_id'],cb_profile_name='coinbase_secrets')
    print('\t\t{}'.format(h))
    order_list_dict.append(h)
    record = (
        h['id'], h['product_id'], h['profile_id'], h['side'], 
        h['funds'], h['specified_funds'], h['type'], str(h['post_only']), 
        h['created_at'], h['done_at'], h['done_reason'], h['fill_fees'], 
        h['filled_size'], h['executed_value'], h['status'], str(h['settled'])
    )
    # _tuple_list = []
    # for kv_tuple in h.items():
    #     _tuple_list.append(kv_tuple)
    record_list.append(record)
    # print(f'\t\t{record_list[i]}')
    #print(record)
index = []
for record in record_list:
    print('Got:')
    print(record)
    index.append(record[0])
    # with open('var\\index.txt') as i, open('var\\temp-data.txt') as f:
    #     for line in i:
    #         if record['id'] in line:
    #             print(f"{record['id']} already exists.")
    #             break
    #         else:
    #             print(f"Saving {record['id']} locally (var/index.txt)")
    #             i.write()
    #             f.write(record)

def init_db(db_filepath):
    db_conn = sqlite3.connect(db_filepath)
    cur = db_conn.cursor()
    cur.execute("""
CREATE TABLE btc_filled_orders
(id text, product_id text, profile_id text, side text, funds text, specified_funds text, type text, post_only text, 
created_at text, done_at text, done_reason text, fill_fees text, filled_size text, executed_value text, status text, settled text)
""")
    db_conn.close()

def save_order(records):
    # init_db(DEFAULT_DB_FILEPATH)
    db_conn = sqlite3.connect(DEFAULT_DB_FILEPATH)
    cur = db_conn.cursor()
    for rec in records:
        print( 'Saving {} to database...'.format(rec) )
        cur.execute('INSERT INTO btc_filled_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rec) 
    db_conn.close()
print('-------------------------------------------------------------------------------------')
print('Indexes (ids):')
print(index)
print('-------------------------------------------------------------------------------------')
print('All orders:')
for order in order_list_dict:
    print(order)
print('-------------------------------------------------------------------------------------')
print('Record list:')
for record in record_list:
    print(record)

save_order(record_list)