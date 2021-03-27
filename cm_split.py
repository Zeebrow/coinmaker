"""
NOTES

When limit sellling:
Amt is units of ETH

When market buying:
Amt is in USD
_total

"""

class Split:
    """
    A "split" is a pair of orders, one buying and one selling.
    Every split has a value, determined by the formula:
    ( price_selling - [price_selling*fee_rate]) = ( price_bought - [price_bought*fee_rate]) + value

    
    """

    def __init__(self, usd_invested: float, usd_return: float):
        self.usd_invested = usd_invested
        self.usd_return = usd_return
        self.fee_rate = 0.005
        self.tx_buy_ = None
        self.tx_sell = None
        self.buy_at = None
        self.sell_at = None
        self.bought = None
        self.sold = None
        self.buy_order = None

    def execute(self):
        """
        Place both the calculated buy and limit sell orders.
        
        """
        pass

    def magic_function(self):
        """
        Determine Split value by computing amount and price to sell.
        Ps(1-Fs) = Pb(1-Fb) - (USD_f - USD_i)
        Fs =   
        """
        pass

