import collections
import json

# Order is a fundamental component of coinmaker.
# Orders should be able to be seamlessly passed around different parts of the program. 
# Using collections.namedtuple for immutablity
NT_Order = collections.namedtuple('Order', [
'id',
'product_id',
'profile_id',
'side',
'funds',
'specified_funds',
'type',
'post_only',
'created_at',
'done_at',
'done_reason',
'fill_fees',
'filled_size',
'executed_value',
'status',
'settled'
])

class Order:
    """
    Defining an Order object as it appears in the CB Pro console.

    Order objects can be created as typical objects are, or can be
    fetched from a database/cache.

    """
    def __init__(self):  
        self._id = None
        self.product_id = None
        self.profile_id = None
        self.side = None
        self.funds = None
        self.specified_funds = None
        self._type = None
        self.post_only = None
        self.created_at = None
        self.done_at = None
        self.done_reason = None
        self.fill_fees = None
        self.filled_size = None
        self.executed_value = None
        self.status = None
        self.settled = None
        self._set_order()

    def _set_order(self):
        self.order = NT_Order(
        self._id,
        self.product_id,
        self.profile_id,
        self.side,
        self.funds,
        self.specified_funds,
        self._type,
        self.post_only,
        self.created_at,
        self.done_at,
        self.done_reason,
        self.fill_fees,
        self.filled_size,
        self.executed_value,
        self.status,
        self.settled
        )
        return self.order

    def __repr__(self):
        return self.order

    def show(self, indent=2):
        print(json.dumps(self.order, indent=indent))

    def persist(self, database_connection):
        """
        Save order to SQLite3 database.
        But what if Oracle DB? Postgres? Hmmm... Drivers...
        """
        pass


class MarketBuy(Order):
    def __init__(self):
        pass

    def market_buy(self, amount, limit_price):
        """
        The value of a 100% filled limit sell order is predictable.

        For use in a Split, we nee the net value of a filled limit sell order.

        The actual order that hits the books is the value of the sell in USD, minus the fee.
        For example, you limit sell 0.01 ETH with a limit price of 1696 USD (16.96 USD value).
        Note the quoted fee (F_ls) of 0.06 USD = Amount (ETH) * limit_price (USD) * Fee rate (dimensionless)
        Once the limit order is filled, the quoted fee amount is subtracted from the final total. 
        """
        pass

class LimitSell(Order):
    def __init__(self):
        pass

    def limit_sell(self, amount, limit_price):
        """
        The value of a 100% filled limit sell order is predictable.

        For use in a Split, we nee the net value of a filled limit sell order.

        The actual order that hits the books is the value of the sell in USD, minus the fee.
        For example, you limit sell 0.01 ETH with a limit price of 1696 USD (16.96 USD value).
        Note the quoted fee (F_ls) of 0.06 USD = Amount (ETH) * limit_price (USD) * Fee rate (dimensionless)
        Once the limit order is filled, the quoted fee amount is subtracted from the final total. 
        """
        pass
    
def db_info():
    print("""
    sqlite3 db location:
    Tables: orders,
    orders:
        text id, text product_id, text side, text stp, specified_funds, type,  

    """)
    pass


def fetch_order(self, order_id):
    """
    Retrieve an order details from database to initialize values.
    Not sure why we need this yet, but having it definitely opens a Pandora's Box of sorts.
    Should DB connection be opened here?
    Args:
        order_id (str): Get the order_id from cbpro.AuthenticatedClient() after placing an order (the id field)

    Returns:
        order (Order): An order object fresh from the DB.
    """
    pass

def batch_fetch(self, order_ids: list):
    """
    Retrieve shittons of orders (potentially)

    Args:
        order_ids (list): See fetch_order

    Returns:
        orders (list): List of Order objects.
    """
    pass