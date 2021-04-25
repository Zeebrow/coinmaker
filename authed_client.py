import logging
import cm_secrets
from cbpro import AuthenticatedClient

log = logging.getLogger(__name__)


class AuthedClient(AuthenticatedClient):
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.secrets = cm_secrets.get_coinbase_credentials(profile_name)
        super().__init__(**self.secrets)
        del self.secrets
