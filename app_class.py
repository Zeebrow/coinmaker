import logging
import cm_secrets
from cbpro import AuthenticatedClient

log = logging.getLogger(__name__)

class app(AuthenticatedClient):
    def __init__(self, profile):
        self.profile = profile
        self.secrets = {}
        self.secrets['key'] = cm_secrets.get_coinbase_credentials(self.profile)['key']
        self.secrets['b64secret'] = cm_secrets.get_coinbase_credentials(self.profile)['b64secret']
        self.secrets['passphrase'] = cm_secrets.get_coinbase_credentials(self.profile)['passphrase']
        self.secrets['api_url'] = cm_secrets.get_coinbase_credentials(self.profile)['api_url']
        super().__init__(**self.secrets)
        del self.secrets

    def get_accts(self):
        log.debug(f"Getting active accounts for profile: {self.profile}...")
        active_accounts = []
        for acct in self.get_accounts():
            log.debug(f"Found account: {acct}")
            if acct['currency'] in ["BTC", "ETH", "BCH", "USD"]:
                active_accounts.append({
                    "currency": acct['currency'],
                    "id": acct['id']
                })
        return active_accounts

    def get_account_history(self, acct):
        pass

    def get_profile(self):
        return self.profile

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    app = app('coinbase_sandbox')
    print(app.get_profile())
    print(app.get_accts())