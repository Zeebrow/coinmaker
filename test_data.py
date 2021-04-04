# Fields are not indexed in influx, but tags are.
# Queries against indexes things are faster.
idb_json_to_load = [
    {
        "measurement": "btc_price",
        "tags": {
            "coin": "btc",
        },
        "time": "2009-11-10T23:00:10Z",
        "fields": {
            "currency": "btcusd",
            "Float_value": 60000.75
        }
    }
]

# For btc_filled_orders table
# sqlite3_record_to_load = (
#     order['id'], order['product_id'], order['profile_id'], order['side'], 
#     order['funds'], order['specified_funds'], order['type'], str(order['post_only']), 
#     order['created_at'], order['done_at'], order['done_reason'], order['fill_fees'], 
#     order['filled_size'], order['executed_value'], order['status'], str(order['settled'])
# )


cb_test_account_id = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'

# actually a generator, but this is an item in it.
cb_get_order_histpry_response = [{
    "id": "5258281937",
    "amount": "0.0001694800000000",
    "balance": "0.0034005300000000",
    "created_at": "2021-03-18T03:41:06.895247Z",
    "type": "match",
    "details": {
        "order_id": "4f630603-2aa1-43c0-b0e5-479626cf3bfc",
        "product_id": "BTC-USD",
        "trade_id": "146517220"
    }
}]

cb_test_order_id = 'f1419466-0ebe-464b-a549-7dbdb9847f39'
cb_get_order_response = {
    "id": "f1419466-0ebe-464b-a549-7dbdb9847f39",
    "product_id": "BTC-USD",
    "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93",
    "side": "buy",
    "funds": "4.9751243700000000",
    "specified_funds": "5.0000000000000000",
    "type": "market",
    "post_only": "false",
    "created_at": "2021-03-11T08:26:02.122069Z",
    "done_at": "2021-03-11T08:26:02.132Z",
    "done_reason": "filled",
    "fill_fees": "0.0248731905130000",
    "filled_size": "0.00009098",
    "executed_value": "4.9746381026000000",
    "status": "done",
    "settled": "true"
}
idb_stored_order1 = [
    {
        "measurement": "btc_price",
        "tags": {
            "id": "f1419466-0ebe-464b-a549-7dbdb9847f39",
            "product_id": "BTC-USD",
            "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93",
            "side": "buy",
            "funds": 4.9751243700000000,
            "specified_funds": 5.0000000000000000,
            "type": "market",
            "post_only": False,
            "created_at": "2021-03-11T08:26:02.122069Z",
            "done_at": "2021-03-11T08:26:02.132Z",
            "done_reason": "filled",
            "fill_fees": 0.0248731905130000,
            "filled_size": 0.00009098,
            "executed_value": 4.9746381026000000,
            "status": "done",
            "settled": True
        },
        "time": "2021-03-11T08:26:02Z", # cb_get_order_response['done_at']
        "fields": {
            "one": 1
        }
    }
]