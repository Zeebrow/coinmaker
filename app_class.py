import logging
import json
from time import sleep

# from asset import Asset
from profile import Profile
from authed_client import AuthedClient
from order import Order

tracked_currencies = ["BTC", "ETH", "BCH", "USD"]
log = logging.getLogger(__name__)

class App(AuthedClient):
    def __init__(self, profile_name):
        super().__init__(profile_name=profile_name)
        self.profile_name = profile_name 
        self.profile = self.init_profile()
    
    def init_profile(self):
        return Profile(self.profile_name)

    def get_order_history(self, acct_id, acct_canonical_name=None, rate_limit_seconds=0.3):
        """
        Used solely to get each order's id field for use in get_order_details (should return list of id's instead, w/e)
        Return:
            list (of order_ids)
        """
        # _test_account_id = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'
        txfers = []
        i = 0
        for order in self.get_account_history(acct_id):
            log.debug(f"\rGetting order {i} in account {acct_canonical_name}...", end="")
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
    
if __name__ == '__main__':
    import order
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter( '--TEST--%(asctime)s - %(name)s - %(levelname)s - %(message)s' ))
    logger.addHandler(sh)
    logger.info("BEGIN MYSTICAL JOURNEY")
    profile = 'coinbase_secrets'
    app = App(profile)
    # print(App.Profile)
    print(app.profile.assets[0])
    order1 = app.profile.assets[0].get_order_details('f1419466-0ebe-464b-a549-7dbdb9847f39')
    print(order1)
    print(type(order1))
    # for order in app.profile.assets[0].get_order_history():
    #     print(order)
    #     o = app.profile.assets[0].get_order_details(order)
    #     o.save('myflie.txt')
    o = order.Order.ex_order
    o['id_'] = o['id'] + 'asdf'
    o['type_'] = o['type'] + 'asdf'
    print(Order(**o))