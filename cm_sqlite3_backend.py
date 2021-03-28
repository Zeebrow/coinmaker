import os
import sqlite3
from CONSTANTS import *
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
logger.addHandler(sh)

"""
Each order must be a tuple with 16 elements
"""

def init_db(db_filepath, table):
    try:
        db_conn = sqlite3.connect(db_filepath)
        logger.debug(f"Connected to db {db_filepath}")
    except sqlite3.OperationalError:
        logger.error(f"Could not connect to db as {db_filepath}. Does it exist?")
    cur = db_conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} 
        (id text, 
        product_id text, 
        profile_id text, 
        side text, 
        funds text, 
        specified_funds text, 
        type text, 
        post_only text, 
        created_at text, 
        done_at text, 
        done_reason text, 
        fill_fees text, 
        filled_size text, 
        executed_value text, 
        status text, 
        settled text)
        """)
    logger.info(f"Created table {table}.")

    db_conn.close()

def commit_order(order, table, db_filepath):
    db_conn = sqlite3.connect(db_filepath)
    cur = db_conn.cursor()
    logger.debug(f"Commiting order id {order[0]}...")
    cur.execute("INSERT INTO btc_filled_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", order)
    db_conn.commit()
    db_conn.close()

def commit_bulk(orders, table, db_filepath):
    logger.debug(f"Commiting {len(orders)} orders...")
    db_conn = sqlite3.connect(db_filepath)
    cur = db_conn.cursor()
    cur.executemany("INSERT INTO btc_filled_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", orders)
    db_conn.commit()
    db_conn.close()

def sc_commit_order(table, db_filepath):
    db_conn = sqlite3.connect(db_filepath)
    cur = db_conn.cursor()
    logger.debug("Commit order...")
    cur.execute("INSERT INTO btc_filled_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ('4061c105-f121-4b0f-ae32-7b0b489fd275', 'BTC-USD', 'bce73511-6c46-48fd-83c1-31002ed36d93', 'buy', '9.9502487500000000', 
    '10.0000000000000000', 'market', 'False', '2021-03-18T00:53:12.306503Z', '2021-03-18T00:53:12.315Z', 'filled', '0.0497486048250000', '0.00016827', '9.9497209650000000', 'done', 'True'))
    db_conn.commit()
    db_conn.close()

def nuke(table, db_filepath, are_you_sure=False):
    if are_you_sure:
        logger.warning(f"Dropping table {table}...")
        db_conn = sqlite3.connect(db_filepath)
        cur = db_conn.cursor()
        cur.execute(f"""
        DROP TABLE IF EXISTS {table}
        """)
        db_conn.close()
    else:
        logger.info("You aren't sure you want to destroy db. Ain't gonna do it!")


if __name__ == '__main__':
    print("--------------------------------------------------------------------")
    test_recs = [
        ('4061c105-f121-4b0f-ae32-7b0b489fd275', 'BTC-USD', 'bce73511-6c46-48fd-83c1-31002ed36d93', 'buy', '9.9502487500000000', '10.0000000000000000', 
        'market', 'False', '2021-03-18T00:53:12.306503Z', '2021-03-18T00:53:12.315Z', 'filled', '0.0497486048250000', '0.00016827', '9.9497209650000000', 'done', 'True'),
        ('4061c105-f121-4b0f-ae32-7b0b489fd276', 'BTC-USD', 'bce73511-6c46-48fd-83c1-31002ed36d93', 'buy', '9.9502487500000000', '10.0000000000000000', 
        'market', 'False', '2021-03-18T00:53:12.306503Z', '2021-03-18T00:53:12.315Z', 'filled', '0.0497486048250000', '0.00016827', '9.9497209650000000', 'done', 'True'),
        ('4061c105-f121-4b0f-ae32-7b0b489fd277', 'BTC-USD', 'bce73511-6c46-48fd-83c1-31002ed36d93', 'buy', '9.9502487500000000', '10.0000000000000000', 
        'market', 'False', '2021-03-18T00:53:12.306503Z', '2021-03-18T00:53:12.315Z', 'filled', '0.0497486048250000', '0.00016827', '9.9497209650000000', 'done', 'True')
    ]
    table = 'btc_filled_orders'
    nuke(table, DEFAULT_DB_FILEPATH, are_you_sure=True)
    init_db(table=table, db_filepath=DEFAULT_DB_FILEPATH)
    #sc_commit_order(table=table, db_filepath=DEFAULT_DB_FILEPATH)
    for rec in test_recs:
        _o = rec
        commit_order(_o,table,DEFAULT_DB_FILEPATH)
    nuke(table, DEFAULT_DB_FILEPATH, are_you_sure=True)
    init_db(table=table, db_filepath=DEFAULT_DB_FILEPATH)
    commit_bulk(orders=test_recs,table=table,db_filepath=DEFAULT_DB_FILEPATH)
    # for rec in test_recs:
    #     print(f"{rec}")
    #     commit_order(rec, table, DEFAULT_DB_FILEPATH)
    #nuke('btc_filled_orders', DEFAULT_DB_FILEPATH)