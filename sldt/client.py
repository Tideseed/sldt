from pydantic import BaseModel
import os
import requests
import sseclient  # pip install sseclient-py
import copy
import json


class singleLotTradeObject(BaseModel):
    contract: str
    position: str


def printout(d, **kwargs):
    print(d)


class sldtClient:
    def __init__(self, api_key, **kwargs):
        if kwargs.get("localtest", False):
            self.url = "http://localhost:3003"
        else:
            self.url = kwargs.get("url", None)
        self.streamer = None
        self.ms = {}
        self.authenticate(api_key)
        self.get_stream()

    def trade(self, trade_object: singleLotTradeObject):
        trade_body = copy.deepcopy(trade_object)
        if trade_body["position"] not in ["short", "long"]:
            return {"error": "Position parameter value should either be short or long."}

        ms_d = self.ms.get(trade_body["contract"], None)
        if ms_d is None:
            return {"error": "Currently there is no market data about this contract."}

        price = ms_d["info"][
            "bid_bp" if trade_body["position"] == "short" else "ask_bp"
        ]

        if price is None:
            return {
                "error": "Currently there is no "
                + ("bid" if trade_body["position"] == "short" else "ask")
                + " quote on the market info."
            }

        trade_body["price"] = price
        res = requests.post(
            os.path.join(self.url, "tradeorder"),
            json=trade_body,
            headers={"api_key": self.api_key},
        )
        return res

    def authenticate(self, api_key: str):
        self.api_key = api_key
        self.user = None
        self.get_stream()

    def get_stream(self, **kwargs):

        response = requests.get(
            os.path.join(self.url, "stream"),
            stream=True,
            headers={"api_key": self.api_key},
        )

        if response.status_code != 200:
            print("API KEY error in getting stream.")
            return response.json()

        self.streamer = sseclient.SSEClient(response)

    def show_stream(self, func=printout, **kwargs):
        if self.streamer is None:
            self.get_stream()
        else:
            for event in self.streamer.events():
                d = self.event_handler(event)
                func(d, **kwargs)

    def event_handler(self, event, **kwargs):
        d = event.__dict__
        if d["event"] == "ping":
            d2 = {"event": "ping", "id": d["data"], "data": {}, "retry": None}
        else:
            d2 = json.loads(d["data"])

        if d["event"] == "snapshot":
            self.ms = copy.deepcopy(d2)
        return d2
