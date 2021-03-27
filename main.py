import sys
import cbpro

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




print("Coin Maker")