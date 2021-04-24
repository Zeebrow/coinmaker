import cm_secrets
import cbpro
import cm_cbpro_connector

profile = ''
pro = input("Enter cb_default (default profile) or coinbase_sandbox (dcabot profile)")
if pro == '1':
    profile = 'cb_default'
if pro == '2':
    profile = 'coinbase_sandbox'

secs = cm_secrets.get_coinbase_credentials(profile)
auth_client = cbpro.AuthenticatedClient(**secs)

all_accts = cm_cbpro_connector.get_account_info(cb_profile_name=profile)
print(all_accts)
accts = set_accts(all_accts)

def log():
    entry = input("> ")
    entry = entry + '\n'
    with open("diary.txt", 'a') as d:
        d.writelines(entry)

def set_accts(acct_list):
    global accbtc
    global acceth
    global accbth
    global accusd
    for acct in acct_list:
        if acct['currency'].lower() == 'btc':
            print("DEBUG foind btc?")
            print(acct['currency'])
            accbtc = acct['id']
        elif acct['currency'].lower() == 'eth':
            acceth = acct['id']
        elif acct['currency'].lower() == 'bch':
            accbch = acct['id']
        elif acct['currency'].lower() == 'usd':
            accusd = acct['id']
        else:
            print("What currency is {acct['currency']}?")
    return {'accbtc': accbtc, 
            'acceth': acceth,
            'accbch': accbch,
            'accusd': accusd}


def get_bal(a):
    return auth_client.get_account(a)
