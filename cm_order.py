import collections
import json
from cbpro import AuthenticatedClient
import cm_secrets
# Order is a fundamental component of coinmaker.
# Orders should be able to be seamlessly passed around different parts of the program. 
# Using collections.namedtuple for immutablity

class Order:
    """
    Defining an Order object as it appears in the CB Pro console.

    Order objects can be created as typical objects are, or can be
    fetched from a database/cache.

    """
    #_order_args_list = ['id', 'product_id', 'profile_id', 'side', 'funds', 'specified_funds', 'type', 'post_only', 'created_at', 'done_at', 'done_reason', 'fill_fees', 'filled_size', 'executed_value', 'status', 'settled']

    def __init__(self, *args, **kwargs):
        self._id = kwargs.get('id'),
        self.product_id = kwargs.get('product_id'),
        self.profile_id = kwargs.get('profile_id'),
        self.side = kwargs.get('side'),
        self.stp = kwargs.get('stp'),
        self.funds = kwargs.get('funds'),
        self.specified_funds = kwargs.get('specified_funds'),
        self._type = kwargs.get('type'),
        self.post_only = kwargs.get('post_only'),
        self.created_at = kwargs.get('created_at'),
        self.done_at = kwargs.get('done_at'),
        self.done_reason = kwargs.get('done_reason'),
        self.fill_fees = kwargs.get('fill_fees'),
        self.filled_size = kwargs.get('filled_size'),
        self.executed_value = kwargs.get('executed_value'),
        self.status = kwargs.get('status'),
        self.settled = kwargs.get('settled')
        self.order = dict(kwargs)

    def show(self, indent=2):
        print(json.dumps(self.order, indent=2))
        pass

    def persist(self, database_connection):
        """
        Save order to SQLite3 database.
        But what if Oracle DB? Postgres? Hmmm... Drivers...
        """
        pass

def fetch_all_orders():
    auth_client = AuthenticatedClient(**cm_secrets.get_coinbase_credentials())
    

# class MarketBuy(Order):
#     def __init__(self):
#         pass

#     def market_buy(self, amount, limit_price):
#         """
#         The value of a 100% filled limit sell order is predictable.

#         For use in a Split, we nee the net value of a filled limit sell order.

#         The actual order that hits the books is the value of the sell in USD, minus the fee.
#         For example, you limit sell 0.01 ETH with a limit price of 1696 USD (16.96 USD value).
#         Note the quoted fee (F_ls) of 0.06 USD = Amount (ETH) * limit_price (USD) * Fee rate (dimensionless)
#         Once the limit order is filled, the quoted fee amount is subtracted from the final total. 
#         """
#         pass

# class LimitSell(Order):
#     def __init__(self):
#         pass

#     def limit_sell(self, amount, limit_price):
#         """
#         The value of a 100% filled limit sell order is predictable.

#         For use in a Split, we nee the net value of a filled limit sell order.

#         The actual order that hits the books is the value of the sell in USD, minus the fee.
#         For example, you limit sell 0.01 ETH with a limit price of 1696 USD (16.96 USD value).
#         Note the quoted fee (F_ls) of 0.06 USD = Amount (ETH) * limit_price (USD) * Fee rate (dimensionless)
#         Once the limit order is filled, the quoted fee amount is subtracted from the final total. 
#         """
#         pass


# def fetch_order(self, order_id):
#     """
#     Retrieve an order details from database to initialize values.
#     Not sure why we need this yet, but having it definitely opens a Pandora's Box of sorts.
#     Should DB connection be opened here?
#     Args:
#         order_id (str): Get the order_id from cbpro.AuthenticatedClient() after placing an order (the id field)

#     Returns:
#         order (Order): An order object fresh from the DB.
#     """
#     pass

# def batch_fetch(self, order_ids: list):
#     """
#     Retrieve shittons of orders (potentially)

#     Args:
#         order_ids (list): See fetch_order

#     Returns:
#         orders (list): List of Order objects.
#     """
#     pass