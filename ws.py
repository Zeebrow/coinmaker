import cm_secrets
import cbpro
import json
import time
import sys
import secrets
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase





cb_secs = secrets.cb_credentials
# cb_credentials = {'key': '9e0799466ea77e92d3f8649005daaa77', 'b64secret': 'huOhWkArWQX0iCWuUAuBOY99MnTvwyQym69US+sqRXE1qNB6Lt016cJMJRE/Zq/87MsNjLGEC+Fcgnb7vTngDQ==', 'passphrase': '6s5hewt7e5g', 'api_url': 'https://api-public.sandbox.pro.coinbase.com'}

class MyWebsocketClient(cbpro.WebsocketClient):
    def __init__(
            self,
            channels=['ticker']
            ):
        super().__init__(
            api_key=cb_secs['key'],
            api_secret=cb_secs['b64secret'],
            api_passphrase=cb_secs['passphrase'],
            # Make channels a required keyword-only argument; see pep3102
            #*,
            # Channel options: ['ticker', 'user', 'matches', 'level2', 'full']
            channels=['user'])
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ['ETH-USD']
        self.message_count = 0
        print("Lets count messages?")

    def on_message(self, msg):
        print(json.dumps(msg, indent=4, sort_keys=True))
        self.message_count += 1

    def on_close(self):
        print("GBye")

wsclient = MyWebsocketClient(channels='ticker')
wsclient.start()
print(wsclient.url, wsclient.products)

try:
    while True:
        print(f"Message count: {wsclient.message_count}")
        time.sleep(1)
except KeyboardInterrupt:
    wsclient.close()

if wsclient.error:
    sys.exit(1)
else:
    sys.exit(0)


