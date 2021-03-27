import sys

"""
These classes are an experiment with inheritance and Abstract Base Classes.
Their functional purpose is purely cosmetic for now. 
"""
class Coin(object):
    """
    Coin
    Using this to learn about class inheritance.
    Extend this for each Currency you want to use, overriding(?) methods and stuff.
    """
    def __inti__(self,name, symbol):
        self.name = name
        self.symbol = symbol
        
    def convert(self, currency="USD"):
        pass
        
class ETH(Coin):
    def __init__(self):
        pass
    def convert(self):
        pass 


