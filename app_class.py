import logging
from time import sleep
import cm_secrets
from cbpro import AuthenticatedClient

tracked_currencies = ["BTC", "ETH", "BCH", "USD"]
log = logging.getLogger(__name__)

class App(AuthenticatedClient):
    def __init__(self, p):
        self.accbtc = None
        self.secrets = cm_secrets.get_coinbase_credentials(p)
        super().__init__(**self.secrets)
        self.p = p 
        self.profile = self.init_profile()
        del self.secrets
    
    def init_profile(self):
        return App.Profile(self, self.p)

    class Profile(object):
        def __init__(self, app, name):
            log.debug("Creating Profile object")
            self.name = name
            self.assets = []
            self.holds = None
            self.available_balance = None

        def set_assets(self):
            pass
            # for asset in app.get_assets(name):
            #     self.assets.append()

        class Asset(object):
            def __init__(self, name):
                log.info("Creating Asset object")
                self.name = name
                self.id = None
                self.currency = None
                self.bal = None
                self.hold = None
                self.available = None
                self._profile = None

            @property
            def id(self):
                return self.id

            @property
            def bal(self):
                pass

        def set_accounts(self, accts_lofd: list):
            pass


    def get_assets(self, profile):
        log.debug(f"Getting assets for profile: {profile}...")
        active_assets = []
        ct = 0
        for asset in super().get_accounts():
            d = {}
            ct += 1
            log.debug(f"Got asset: {asset}")
            if asset['currency'] in tracked_currencies:
                d[asset['currency']] = asset['id'] 
                active_assets.append(d)
        log.info(f"Got {len(active_assets)} assets out of {ct} total asssets.")
        return active_assets

    def set_accts(self, acct: dict):
        self.btcid = acct['BTC']
        self.ethid = acct['ETH']
        self.accbch = acct['BCH']
        self.accusd = acct['USD']

    def get_order_history(self, acct_id, acct_canonical_name=None, rate_limit_seconds=0.3):
        """
        Used solely to get each order's id field for use in get_order_details (should return list of id's instead, w/e)
        Return:
            list (of order_ids)
        """
        # _test_account_id = '3fa53d16-7da5-4272-bfbf-bc9cc8ac698e'
        order_ids = []
        txfers = []
        # auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(profile=profile))
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
        # print(f"\rGot {len(order_ids)} ids for {acct_id} account." + " "*20)
        # if len(txfers) > 0:
        #     print(f"There were {len(txfers)} transfer-type orders. These are not returned in resulting order_ids list!")
        # # log.info(f"Got {len(order_ids)} order ids.")
        # return order_ids
    
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter( '--TEST--%(asctime)s - %(name)s - %(levelname)s - %(message)s' ))
    logger.addHandler(sh)
    logger.info("BEGIN MYSTICAL JOURNEY")
    profile = 'coinbase_secrets'
    app = App(profile)
    print(app.profile.name)
    # accts = app.get_assets(profile)
    
    # print(app.get_accts())
    # print(app.get_products())