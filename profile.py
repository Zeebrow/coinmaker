import logging
from asset import Asset
from authed_client import AuthedClient

log = logging.getLogger(__name__)
tracked_currencies = ["BTC", "ETH", "BCH", "USD"]

class Profile(AuthedClient):
    def __init__(self, profile_name):
        super().__init__(profile_name=profile_name)
        log.debug("Creating Profile object")
        self.profile = profile_name
        self._assets = []
        for asset in self.set_assets(self.profile):
            self._assets.append(asset)
        self.holds = None
        self.available_balance = None

    def __str__(self):
        return self.profile

    @property
    def assets(self):
        return self._assets

    def get_assets(self, profile):
        log.debug(f"Getting assets for profile: {profile}...")
        active_assets = []
        ct = 0
        for asset in super().get_accounts():
            ct += 1
            log.debug(f"Got asset: {asset}")
            if asset['currency'] in tracked_currencies:
                active_assets.append(asset)
        log.info(f"Got {len(active_assets)} assets out of {ct} total asssets.")
        return active_assets

    def add_asset(self, assetprops: dict):
        return Asset(profile_name=self.profile, **assetprops)

    def set_assets(self, p):
        log.debug(f"setting assets")
        a = []
        for asset in self.get_assets(p):
            log.debug(f"ass {asset}")
            a.append(self.add_asset(asset))
        return a