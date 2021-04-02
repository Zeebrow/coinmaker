import cbpro
import logging
import cm_secrets
import cm_sqlite3_backend as db
from CONSTANTS import *
import json
logger = logging.getLogger(__name__)
import time


"""
Perform operations against Coinbase Bro api.
"""
cb_profile_name='coinbase_secrets'
auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))

def get_account_info(cb_profile_name='coinbase_sandbox'):
    """
    Returns:
        list of accounts with balance > 0
    """
    accts = auth_client.get_accounts() # list of accounts
    active_accts = []
    for acct in accts:
        if float(acct['balance']) > 0:
            active_accts.append(acct)
    return active_accts

def get_order_history(acct_id, cb_profile_name='coinbase_sandbox', rate_limit=0):
    """
    Used solely to get each order's id field for use in get_order_details (should return list of id's instead, w/e)
    Return:
        list (of order_ids)
    """
    # _test_account_id = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'
    order_ids = []
    auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))
    i = 1
    for order in auth_client.get_account_history(acct_id):
        logger.debug(f"Getting order {i}...")
        print(order)
        if 'details' not in order:
            if 'message' in order:
                if 'rate limit exceeded' in order['message'].lower():
                    logger.warning("Rate limit exceeded, sleeping for 5 seconds.")
                    time.sleep(5)
                else:
                    logger.error(f"Could not get order {order}. {order['message']}")
                    break
        if 'order_id' not in order['details'].keys():
            logger.error(f"Unhandled transaction type, I think. Order: {order}")
            break

        _test_order = 'f1419466-0ebe-464b-a549-7dbdb9847f39'
        if len(order['details']['order_id']) != len(_test_order):
            logger.error("Invalid order id detected! {order_id}")
            break

        order_ids.append(order['details']['order_id'])
        time.sleep(rate_limit)
        i+=1
    return order_ids
    

def get_order_details(order_id, cb_profile_name='coinbase_sandbox'):
    """
    Get details of an order, to match cm_order
    Returns:
        dict
    """
    # For the one wierd case where order_id was '3c958bf7-fcc3-4881-8180-b2f44823e2d2-c7b7-48eb-bfba-4ada110178cd'


    order = auth_client.get_order(order_id)
    
    if 'message' in order.keys():
        logger.error(f"Could not get order {order}.")
        print(f"ERROR: {order['message']} for order_id {order_id}")
        time.sleep(5)
        return {'retry_order_id': order_id}
    else:
        logger.debug(f"get_order_details order: {order}")
        return order

def sanitize_order(order):
    record = (
        order['id'], order['product_id'], order['profile_id'], order['side'], 
        order['funds'], order['specified_funds'], order['type'], str(order['post_only']), 
        order['created_at'], order['done_at'], order['done_reason'], order['fill_fees'], 
        order['filled_size'], order['executed_value'], order['status'], str(order['settled'])
    )
    return record


def init_app(clean=False):
    logger.info("Starting fresh app.")
    logger.info("Getting account information...")
    active_accounts = get_account_info('coinbase_secrets')
    logger.debug(f"Got active accounts: {active_accounts}.")
    tables = []
    # Get a list of account ids with funds in them
    for acct in active_accounts:
        id = acct['id']
        curr = acct['currency'].lower()
        logger.info("")
        table = curr + "_filled_orders"
        tables.append(table)
        # Delete tables that exist, conditionally
        db.nuke(table, DEFAULT_DB_FILEPATH, are_you_sure=clean)
        logger.info(f"Creating table {table}...")
        # Create tables to hold order history, for active accounts
        db.init_db_table(DEFAULT_DB_FILEPATH, table)

        # Populate table with order history
        logger.info("Getting orders... oh shit...")
        order_list = get_order_history(acct['id'], 'coinbase_secrets')
        record_list = []
        logger.debug(f"order_list (type type(order_list): {order_list}")
        logger.debug(f"init_app order_list length : {len(order_list)}")
        # for order in get_order_history(acct, 'coinbase_secrets'):
        retry_order_id_list = []
        for o in order_list:
            # We shouldn't need to check for bad orders here.
            print(f"Order (type {type(o)}): {o}")
            h = get_order_details(o,cb_profile_name='coinbase_secrets')

            if 'retry_order_id' in h.keys():
                retry_order_id_list.append(h['retry_order_id'])
                logger.warning("Rate limit exceeded, sleeping 5...")
                time.sleep(5)
                h = get_order_details(o,cb_profile_name='coinbase_secrets')
            record = (
                h['id'], h['product_id'], h['profile_id'], h['side'], 
                h['funds'], h['specified_funds'], h['type'], str(h['post_only']), 
                h['created_at'], h['done_at'], h['done_reason'], h['fill_fees'], 
                h['filled_size'], h['executed_value'], h['status'], str(h['settled'])
            )
            record_list.append(record)
        logger.warning(f"These orders were not committed to database! {retry_order_id_list}")
        db.commit_bulk(orders=record_list, table=table, db_filepath=DEFAULT_DB_FILEPATH)
        
    

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    fh = logging.FileHandler(DEFAULT_LOG_FILEPATH)
    sh.setFormatter(logging.Formatter( '--TEST--%(asctime)s - %(name)s - %(levelname)s - %(message)s' ))
    logger.addHandler(sh)
    init_app()
    # a = get_order_history('3fa53d16-7da5-4272-bfbf-bc9cc8ac698e', 'coinbase_secrets')
    # print(a)
    orders_list = [{'id': '5531038486', 'amount': '0.0001692700000000', 'balance': '0.0063764200000000', 'created_at': '2021-04-01T07:41:01.92803Z', 'type': 'match', 'details': {'order_id': 'e021e693-afbb-4d1a-992d-bf426169cc72', 'product_id': 'BTC-USD', 'trade_id': '151619003'}}, {'id': '5508389895', 'amount': '0.0001677800000000', 'balance': '0.0062071500000000', 'created_at': '2021-03-31T07:45:02.311724Z', 'type': 'match', 'details': {'order_id': '13770664-3b41-4435-a557-f214511deee6', 'product_id': 'BTC-USD', 'trade_id': '151259852'}}, {'id': '5490030649', 'amount': '0.0001714300000000', 'balance': '0.0060393700000000', 'created_at': '2021-03-30T07:40:01.786134Z', 'type': 'match', 'details': {'order_id': '53e036c9-0c37-4788-9c04-d1a9043fca12', 'product_id': 'BTC-USD', 'trade_id': '150953098'}}, {'id': '5467765614', 'amount': '0.0001790500000000', 'balance': '0.0058679400000000', 'created_at': '2021-03-29T07:11:02.215736Z', 'type': 'match', 'details': {'order_id': '23dc9a88-5132-44fd-9059-45b9c4c54ad0', 'product_id': 'BTC-USD', 'trade_id': '150573779'}}, {'id': '5449811906', 'amount': '0.0001773000000000', 'balance': '0.0056888900000000', 'created_at': '2021-03-28T07:51:01.667974Z', 'type': 'match', 'details': {'order_id': 'bb88b867-fc81-4323-990c-dbaaf10adc96', 'product_id': 'BTC-USD', 'trade_id': '150340231'}}, {'id': '5428790231', 'amount': '0.0001817600000000', 'balance': '0.0055115900000000', 'created_at': '2021-03-27T07:46:01.950719Z', 'type': 'match', 'details': {'order_id': 'bf7113fb-c9fc-4317-ab88-9452e7b99bc3', 'product_id': 'BTC-USD', 'trade_id': '150072611'}}, {'id': '5387235281', 'amount': '0.0001879700000000', 'balance': '0.0053298300000000', 'created_at': '2021-03-25T07:18:01.63206Z', 'type': 'match', 'details': {'order_id': '407b18ac-f7f3-4cf4-9c45-e38627224796', 'product_id': 'BTC-USD', 'trade_id': '149215901'}}, {'id': '5366566243', 'amount': '0.0001795200000000', 'balance': '0.0051418600000000', 'created_at': '2021-03-24T07:07:02.063791Z', 'type': 'match', 'details': {'order_id': '568e43d4-15d0-48fa-95df-2713645cc6da', 'product_id': 'BTC-USD', 'trade_id': '148723044'}}, {'id': '5351057485', 'amount': '0.0001850800000000', 'balance': '0.0049623400000000', 'created_at': '2021-03-23T07:33:01.517209Z', 'type': 'match', 'details': {'order_id': '27e20766-09cf-44b2-8d42-db84e51da8d5', 'product_id': 'BTC-USD', 'trade_id': 
'148374014'}}, {'id': '5330934399', 'amount': '0.0001725800000000', 'balance': '0.0047772600000000', 'created_at': '2021-03-22T07:38:01.820613Z', 'type': 'match', 'details': {'order_id': '1769de74-2d0d-4cb6-af06-ca53ff481010', 'product_id': 'BTC-USD', 'trade_id': '147911865'}}, {'id': '5317719362', 'amount': '0.0001742000000000', 'balance': '0.0046046800000000', 'created_at': '2021-03-21T07:37:02.315374Z', 'type': 'match', 'details': {'order_id': '6a2c580f-5198-411e-b883-748d827996c3', 'product_id': 'BTC-USD', 'trade_id': '147634667'}}, {'id': '5315431924', 'amount': '0.0001726800000000', 'balance': '0.0044304800000000', 'created_at': '2021-03-21T03:19:38.210612Z', 'type': 'match', 'details': {'order_id': 'b06c9cf2-73a9-4448-84bd-2584fecdd781', 'product_id': 'BTC-USD', 'trade_id': '147582076'}}, {'id': '5315386122', 'amount': '0.0001724800000000', 'balance': '0.0042578000000000', 'created_at': '2021-03-21T03:14:26.38851Z', 'type': 'match', 'details': {'order_id': 'eec336a8-db96-40c1-8d0f-a2a538a0164d', 'product_id': 'BTC-USD', 'trade_id': '147581069'}}, {'id': '5315290583', 'amount': '0.0001723400000000', 'balance': '0.0040853200000000', 'created_at': '2021-03-21T03:04:02.255326Z', 'type': 'match', 'details': {'order_id': '4fbd7271-6a78-43be-90cd-c04609d75ed6', 'product_id': 'BTC-USD', 'trade_id': '147578815'}}, {'id': '5300582586', 'amount': '0.0001707100000000', 'balance': '0.0039129800000000', 'created_at': '2021-03-20T07:10:01.542193Z', 'type': 'match', 'details': {'order_id': 'a10f5586-7c6c-47a3-9570-cd7677ed2d7d', 'product_id': 'BTC-USD', 'trade_id': '147344110'}}, {'id': '5281890672', 'amount': '0.0001709600000000', 'balance': '0.0037422700000000', 'created_at': '2021-03-19T07:23:01.937172Z', 'type': 'match', 'details': {'order_id': '810577f6-e0bb-4512-867b-dba7844580d8', 'product_id': 'BTC-USD', 'trade_id': '146992802'}}, {'id': '5261041043', 'amount': '0.0001707800000000', 'balance': '0.0035713100000000', 'created_at': '2021-03-18T07:50:02.448474Z', 'type': 'match', 'details': {'order_id': '272c1a41-9245-47f3-a251-ff49024513b2', 'product_id': 'BTC-USD', 'trade_id': '146569450'}}, {'id': '5258281937', 'amount': '0.0001694800000000', 'balance': '0.0034005300000000', 'created_at': '2021-03-18T03:41:06.895247Z', 'type': 'match', 'details': {'order_id': '4f630603-2aa1-43c0-b0e5-479626cf3bfc', 'product_id': 'BTC-USD', 'trade_id': '146517220'}}, {'id': '5257409167', 'amount': '0.0001684600000000', 'balance': '0.0032310500000000', 'created_at': '2021-03-18T02:43:04.425304Z', 'type': 'match', 'details': {'order_id': '73d9e453-b01e-4f5c-ba81-bfc1f605926f', 'product_id': 'BTC-USD', 'trade_id': '146501286'}}, {'id': '5257288176', 'amount': '0.0001680900000000', 'balance': '0.0030625900000000', 'created_at': '2021-03-18T02:36:34.764309Z', 'type': 'match', 'details': {'order_id': '54f2aa44-af22-4fb8-8d1e-d59895ee5942', 'product_id': 'BTC-USD', 'trade_id': '146499329'}}, {'id': '5255567173', 'amount': '0.0001686600000000', 'balance': '0.0028945000000000', 'created_at': '2021-03-18T00:59:20.461874Z', 'type': 'match', 'details': {'order_id': 'c8db6064-3999-4f38-9b84-31d1062e4989', 'product_id': 'BTC-USD', 'trade_id': '146469673'}}, {'id': '5255438969', 'amount': '0.0001682700000000', 'balance': '0.0027258400000000', 'created_at': '2021-03-18T00:53:12.317943Z', 'type': 'match', 'details': {'order_id': '4061c105-f121-4b0f-ae32-7b0b489fd275', 'product_id': 'BTC-USD', 'trade_id': '146467801'}}, {'id': '5238750981', 'amount': '0.0001775600000000', 'balance': '0.0025575700000000', 'created_at': '2021-03-17T07:34:01.715546Z', 'type': 'match', 'details': {'order_id': '00ef478a-67c3-493f-a88e-4d1df129ed75', 'product_id': 'BTC-USD', 'trade_id': '146089047'}}, {'id': '5222524337', 'amount': '0.0001807200000000', 'balance': '0.0023800100000000', 'created_at': '2021-03-16T07:44:02.220019Z', 'type': 'match', 'details': {'order_id': 'c990cbc1-69d6-4f54-8b61-1573d965e0fa', 'product_id': 'BTC-USD', 'trade_id': '145719343'}}, {'id': '5218750741', 'amount': '0.0001828000000000', 'balance': '0.0021992900000000', 'created_at': '2021-03-16T02:06:09.841434Z', 'type': 'match', 'details': {'order_id': 'fd9e70d7-5e80-4977-9f50-bf6c4624615a', 'product_id': 'BTC-USD', 'trade_id': '145612781'}}, {'id': '5200753994', 'amount': '0.0001714200000000', 'balance': '0.0020164900000000', 'created_at': '2021-03-15T07:39:01.535362Z', 'type': 'match', 'details': {'order_id': 'b5239b68-ab26-445c-841c-072ee7421661', 'product_id': 'BTC-USD', 'trade_id': '145087983'}}, {'id': '5182607036', 'amount': '0.0001636900000000', 'balance': '0.0018450700000000', 'created_at': '2021-03-14T07:14:01.896664Z', 'type': 'match', 'details': {'order_id': 'd2a2842c-72af-4c33-8448-bc73cc8d405e', 'product_id': 'BTC-USD', 'trade_id': '144730342'}}, {'id': '5159876768', 'amount': '0.0000866900000000', 'balance': '0.0016813800000000', 'created_at': '2021-03-13T08:25:02.289901Z', 'type': 'match', 'details': {'order_id': 'aa890615-1e2d-49ea-8431-6952078da99d', 'product_id': 'BTC-USD', 'trade_id': '144286519'}}, {'id': '5140812606', 'amount': '0.0000879100000000', 'balance': '0.0015946900000000', 'created_at': '2021-03-12T08:15:01.691537Z', 'type': 'match', 'details': {'order_id': 'f5a3a9c5-e405-4922-92f0-49f1462f8b75', 'product_id': 'BTC-USD', 'trade_id': '143922970'}}, {'id': '5120699273', 'amount': '0.0000909800000000', 'balance': '0.0015067800000000', 'created_at': '2021-03-11T08:26:02.13741Z', 'type': 'match', 'details': {'order_id': 'f1419466-0ebe-464b-a549-7dbdb9847f39', 'product_id': 'BTC-USD', 'trade_id': '143502723'}}, {'id': '5104119966', 'amount': '0.0000913100000000', 'balance': '0.0014158000000000', 'created_at': '2021-03-10T08:30:01.454369Z', 'type': 'match', 'details': {'order_id': 'c10ca88a-5e55-47b7-a0b9-20addced70d4', 'product_id': 'BTC-USD', 'trade_id': '143099413'}}, {'id': '5086200828', 'amount': '0.0000926600000000', 'balance': '0.0013244900000000', 'created_at': '2021-03-09T08:08:01.872858Z', 'type': 'match', 'details': {'order_id': '7b1c6f6f-9063-49c1-8a0e-d6e9c2f70099', 'product_id': 'BTC-USD', 'trade_id': '142727836'}}, {'id': '5080858347', 'amount': '0.0000936300000000', 'balance': '0.0012318300000000', 'created_at': '2021-03-09T01:31:33.482379Z', 'type': 'match', 'details': {'order_id': '97de91e8-97c7-486e-ae1f-0328bc3441c3', 'product_id': 'BTC-USD', 'trade_id': '142595098'}}, {'id': '5080854177', 'amount': '0.0000937200000000', 'balance': '0.0011382000000000', 'created_at': '2021-03-09T01:31:24.215976Z', 'type': 'match', 'details': {'order_id': '1f76e86e-4c75-41f8-900f-01457d392fdd', 'product_id': 'BTC-USD', 'trade_id': '142594903'}}, {'id': '5080839925', 'amount': '0.0000937600000000', 'balance': '0.0010444800000000', 'created_at': '2021-03-09T01:30:25.795094Z', 'type': 'match', 'details': {'order_id': 'f7ea3329-5908-4455-9e8a-fb9e9adf4c59', 'product_id': 'BTC-USD', 'trade_id': '142594425'}}, {'id': '5080795880', 'amount': '0.0000941400000000', 'balance': '0.0009507200000000', 'created_at': '2021-03-09T01:27:41.32615Z', 'type': 'match', 'details': {'order_id': '3c958bf7-fcc3-4881-8180-b2f44823e2d2-c7b7-48eb-bfba-4ada110178cd', 'product_id': 'BTC-USD', 'trade_id': '142592231'}}, {'id': '5080776178', 'amount': '0.0000940400000000', 'balance': '0.0007624900000000', 'created_at': '2021-03-09T01:26:10.10047Z', 'type': 'match', 'details': {'order_id': 'eae26952-6b1e-4d0c-90a6-fe10b6adb845', 'product_id': 'BTC-USD', 'trade_id': '142592012'}}, {'id': '5080763148', 'amount': '0.0000941300000000', 'balance': '0.0006684500000000', 'created_at': '2021-03-09T01:25:37.616486Z', 'type': 'match', 'details': {'order_id': '6a8d93e2-7db7-4acd-a9a9-b98a54177ef7', 'product_id': 'BTC-USD', 'trade_id': '142591560'}}, {'id': '5080757386', 'amount': '0.0000942200000000', 'balance': '0.0005743200000000', 'created_at': '2021-03-09T01:25:20.100533Z', 'type': 'match', 'details': {'order_id': '4ca60cb7-5ae3-4be8-a11a-5c136c0fd700', 'product_id': 'BTC-USD', 'trade_id': '142591341'}}, {'id': '5080740930', 'amount': '0.0000943700000000', 'balance': '0.0004801000000000', 'created_at': '2021-03-09T01:24:15.476108Z', 'type': 'match', 'details': {'order_id': 'e5e871c9-78d6-4702-aa4f-a99ce6d78050', 'product_id': 'BTC-USD', 'trade_id': '142590869'}}, {'id': '5080733398', 'amount': '0.0000944300000000', 'balance': '0.0003857300000000', 'created_at': '2021-03-09T01:23:48.00275Z', 'type': 'match', 'details': {'order_id': '4b48e916-6a98-47f7-beaa-0a8fc5f7fb9f', 'product_id': 'BTC-USD', 'trade_id': '142590702'}}, {'id': '5080657717', 'amount': '0.0000947800000000', 'balance': '0.0002913000000000', 'created_at': '2021-03-09T01:19:40.450721Z', 'type': 'match', 'details': {'order_id': '67f4a4c6-f008-4e1d-81c1-4bd6a13021d4', 'product_id': 'BTC-USD', 'trade_id': '142588337'}}, {'id': '5068603345', 'amount': '0.0000999700000000', 'balance': '0.0001965200000000', 'created_at': '2021-03-08T08:07:02.23509Z', 'type': 'match', 'details': {'order_id': '957fbd54-6ea4-4be2-bcbf-acea0a9a1098', 'product_id': 'BTC-USD', 'trade_id': '142342168'}}, {'id': '5065309763', 'amount': '0.0000965500000000', 'balance': '0.0000965500000000', 'created_at': '2021-03-08T02:02:02.321976Z', 'type': 'match', 'details': {'order_id': '444237fa-a8d4-4978-965d-f9162651dc19', 'product_id': 'BTC-USD', 'trade_id': '142266831'}}]

    acct_id = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'
    # auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))
    # h = auth_client.get_account_history(acct_id)
    # h = get_order_history(acct_id, 'coinbase_secrets')
    # print(type(h))
    # print(h[0])
