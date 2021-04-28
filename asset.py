import logging
import json
from time import sleep
from order import Order
from authed_client import AuthedClient


log = logging.getLogger(__name__)

class Asset(AuthedClient):
    ex_asset = {
        'id': '984037ca-36e9-4b7f-a2ee-33ee8d2fdab2', 
        'currency': 'USD', 
        'balance': '210.0217553782342500', 
        'hold': '0.0000000000000000', 
        'available': '210.02175537823425', 
        'profile_id': 'bce73511-6c46-48fd-83c1-31002ed36d93', 
        'trading_enabled': True
    }

    def __init__(self, profile_name, currency, balance, hold, available, profile_id, trading_enabled, id=None, id_=None ):
        super().__init__(profile_name=profile_name)
        if id:
            self.id_ = id
            del id
        else:
            self.id_ = id_
        self.profile_name = profile_name
        self.currency = currency
        self.balance = balance
        self.hold = hold
        self.available = available
        self.profile_id = profile_id
        self.trading_enabled = trading_enabled

    # def __repr__(self):
    #     return str(self.id_)

    @property
    def order_history(self):
        return self.get_order_history()

    def get_detailed_order_history(self, commit=False, rate_limit_seconds=0.3):
        for _id in self.get_order_history():
            _order = Order(**self.get_order(_id))
            sleep(rate_limit_seconds)
            if commit:
                yield _order.commitable()
            else:
                yield _order

    def get_order_history(self, rate_limit_seconds=0.3):
            """
            Used solely to get each order's id field for use in get_order_details (should return list of id's instead, w/e)
            Return:
                list (of order_ids)
            """
            # _test_account_id = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'
            txfers = []
            # auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(profile=profile))
            i = 0

            for order in self.get_account_history(self.id_):
                log.debug(f"\rGetting order {i} in account {self.id_}...")
                # # Error handling
                # if 'details' not in order:
                #     if 'message' in order:
                #         if 'rate limit exceeded' in order['message'].lower():
                #             log.warning("Rate limit exceeded, sleeping for 5 seconds.")
                #             sleep(rate_limit_seconds)
                #         else:
                #             log.error(f"Could not get order {order}. {order['message']}")
                #             continue
                if 'order_id' not in order['details'].keys():
                    if order['type'].lower() == 'transfer':
                        txfers.append(order)
                        continue
                    else:
                        log.error(f"Unhandled transaction type, I think. Order: {order}")
                        continue

                _test_order = 'f1419466-0ebe-464b-a549-7dbdb9847f39'
                if len(order['details']['order_id']) != len(_test_order):
                    log.error("Invalid order id detected! {order_id}")
                    continue

                sleep(rate_limit_seconds)
                i+=1
                yield order['details']['order_id']
                
    def get_order_details(self, order_id, _cache={}):
        if order_id in _cache:
            return _cache[order_id]
        h = self.get_order(order_id)
        print(h)
        # Do checking here
        if 'id' not in h:
            log.error(f"Bad order params detected before creating order! {h}")
            return None

        return Order(**h)

    def get_all_order_details(self, rate_limit_seconds=0.3, _cache={}):
        for order in self.get_order_history():
                # For the one wierd case where order_id was '3c958bf7-fcc3-4881-8180-b2f44823e2d2-c7b7-48eb-bfba-4ada110178cd'
            if order['id'] in _cache:
                return _cache[order]

            if 'message' in order.keys():
                log.error(f"Could not get order {order}.")
                print(f"ERROR: {order['message']} for order_id {order}")
                sleep(5)
                return {'retry_order_id': order}
            else:
                _cache[order['id']] = order
                log.debug(f"get_order_details order: {order}")
                return order


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ))
    logger.addHandler(sh)
    logger.info("asset.py")
