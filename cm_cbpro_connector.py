import cbpro
import logging
import cm_secrets

logger = logging.getLogger(__name__)

"""
Perform operations against Coinbase Bro api.
"""
cb_profile_name='coinbase_secrets'
auth_client = cbpro.AuthenticatedClient(**cm_secrets.get_coinbase_credentials(cb_profile_name=cb_profile_name))

def get_account_info(cb_profile_name='coinbase_sandbox'):

    accts = auth_client.get_accounts()
    active_accts = []
    for acct in accts:
        if float(acct['balance']) > 0:
            active_accts.append(acct)
    return active_accts


if __name__ == '__main__':
    cb_profile_name='coinbase_secrets'
    DEFAULT_CONSOLE_DELIMITER = ""
    for i in range(80):
        DEFAULT_CONSOLE_DELIMITER = DEFAULT_CONSOLE_DELIMITER + "-"
    print(DEFAULT_CONSOLE_DELIMITER)
    print("cm_cbpro_connector")
    