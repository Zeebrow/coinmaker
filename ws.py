import cm_secrets
import cbpro
import json
import time
import sys
import secrets

cb_secs = secrets.cb_credentials
# cb_credentials = {'key': '9e0799466ea77e92d3f8649005daaa77', 'b64secret': 'huOhWkArWQX0iCWuUAuBOY99MnTvwyQym69US+sqRXE1qNB6Lt016cJMJRE/Zq/87MsNjLGEC+Fcgnb7vTngDQ==', 'passphrase': '6s5hewt7e5g', 'api_url': 'https://api-public.sandbox.pro.coinbase.com'}

class MyWebsocketClient(cbpro.WebsocketClient):
    def __init__(
            self,
            #url="wss://ws-feed.pro.coinbase.com",
            #products=None,
            #message_type="subscribe",
            #mongo_collection=None,
            #should_print=True,
            #auth=False,
            #api_key=cb_secs['key'],
            #    api_secret=cb_secs['b64secret'],
            #    api_passphrase=cb_secs['passphrase'],
            # Make channels a required keyword-only argument; see pep3102
            #*,
            # Channel options: ['ticker', 'user', 'matches', 'level2', 'full']
            channels=['ticker']
            ):
        super().__init__(
            #url="wss://ws-feed.pro.coinbase.com",
            #products=None,
            #message_type="subscribe",
            #mongo_collection=None,
            #should_print=True,
            #auth=False,
            api_key=cb_secs['key'],
            api_secret=cb_secs['b64secret'],
            api_passphrase=cb_secs['passphrase'],
            # Make channels a required keyword-only argument; see pep3102
            #*,
            # Channel options: ['ticker', 'user', 'matches', 'level2', 'full']
            channels=['ticker'])
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


