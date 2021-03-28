import sys, json, collections
import cbpro
import cm_order, cm_coin, cm_split

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
test_data = {
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
print(json.dumps(test_data,indent=2))
Test_Order = collections.namedtuple("Test_Order", [
    "id",
    "product_id",
    "profile_id", 
    "side",
    "funds",
    "specified_funds",
    "type",
    "post_only",
    "created_at",
    "done_at", 
    "done_reason", 
    "fill_fees", 
    "filled_size",  
    "executed_value", 
    "status", 
    "settled"
])
tt = Test_Order(**test_data)
a = cm_order.Order()

print("Coin Maker")
print("------------------------------------")
# for k in tt._fields:
#     print(k, '->', getattr(tt, k))


a.show()