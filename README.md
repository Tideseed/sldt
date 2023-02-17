# About sldt package

Python test SDK package for SLDT (Single Lot Demo Trading)

## Installation

Min Python requirement is 3.10.

```bash
pip install git+https://github.com/Tideseed/sldt.git
```

## Usage

You will need an api key and server url from your administrator.

(ps. You can directly visit the Gist [here](https://gist.github.com/berkorbay/258ccc2907fccb7cd48fcfb93001d9a1))

Minimal working example python script:

```python
from sldt.client import sldtClient
import random

## Environment variables
API_KEY = "YOUR_API_KEY"
SERVER_URL = "THE_SERVER_URL"

def random_trade(d):

    if d.get("event", "noevent") == "hourly_contracts":
        if random.uniform(0, 1) > 0.1:
            trade_d = {"contract": d["c"], "position": random.choice(["short", "long"])}
            return trade_d
    else:
        return None


class Trader(sldtClient):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key, **kwargs)

    def traderstream(self, **kwargs):
        tradeeventlist = []
        for event in self.streamer.events():
            d = self.event_handler(event)
            trade_d = random_trade(d)
            if trade_d is not None:
                res = self.trade(trade_d)
                if not isinstance(res, dict):
                    print("====TRADE ORDER====")
                    print(trade_d)
                    print("====TRADE ORDER====")
                    tradeeventlist.append(res.json())
                    print("====TRADE RESULT====")
                    print(tradeeventlist[-1])
                    print("====TRADE RESULT====")


trader = Trader(api_key=API_KEY, url=SERVER_URL)

trader.traderstream()

```