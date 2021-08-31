from dataclasses import dataclass, field
from executionHandlers.execution import ExecutionHandler
import asyncio
from typing import Mapping, Dict
import json
import websockets
from websockets import WebSocketClientProtocol
import keys
from auth import DeribtAuth
from queue import Queue
from event import SignalEvent
import requests
from threading import Thread
import logging

@dataclass
class DeribitExecutionHandler(ExecutionHandler):
    is_live: bool
    signal_event_queue: Queue

    def __post_init__(self):
        self.exchange_info: Mapping[str, dict] = self.get_exchange_info()

    async def execute_order(self, signal: SignalEvent, websocket: WebSocketClientProtocol):
        params = {"instrument_name": signal.symbol,
                  "amount": signal.qty,
                  "type": 'limit' if signal.isLimit else 'market',
                  "label": "traderv1"}
        if not signal.isLimit:
            msg = \
                {"jsonrpc": "2.0",
                 "method": f"private/{'buy' if signal.isBuy else 'sell'}",
                 "id": 5275,
                 "params": params}
        elif signal.isLimit:
            params["price"] = self.price_precision(signal.price, signal.symbol)
            tif_map: Dict[str, str] = {
                'GTC': 'good_til_cancelled', 'FOK': 'fill_or_kill', "IOC": 'immediate_or_cancel'}
            params['time_in_force'] = tif_map[signal.time_in_force]
            msg = \
                {"jsonrpc": "2.0",
                 "method": f"private/{'buy' if signal.isBuy else 'sell'}",
                 "id": 5275,
                 "params": params}
        await websocket.send(json.dumps(msg))
        _ = await websocket.recv()

    async def connect(self):

        deribit_auth = DeribtAuth(
            keys.DeribtTestSteve['api_key'], keys.DeribtTestSteve['secret_key'])
        if self.is_live:
            url = 'wss://www.deribit.com/ws/api/v2'
        else:
            url = 'wss://test.deribit.com/ws/api/v2'

        async with websockets.connect(url) as websocket:
            await deribit_auth.auth(websocket)
            # await websocket.send(msg)
            # response = await websocket.recv()

            while websocket.open:
                signal: SignalEvent = self.signal_event_queue.get()
                await self.execute_order(signal, websocket)

    def start_stream(self):
        while True:
            try:
                loop = asyncio.new_event_loop()
                task = loop.create_task(self.connect())
                # loop.call_later(60, task.cancel)
                loop.run_until_complete(task)
            except websockets.exceptions.ConnectionClosedError:
                logging.exception("exception")

                print("WebSocket Closed reconnecting")

    


    def get_exchange_info(self) -> Mapping[str, dict]:
        if self.is_live:
            base = 'https://www.deribit.com/api/v2/'
        else:
            base = "https://test.deribit.com/api/v2/"

        response_btc = requests.get(
            f'{base}public/get_instruments?currency=BTC&kind=future')
        response_eth = requests.get(
            f'{base}public/get_instruments?currency=ETH&kind=future')

        exchange_info: Mapping[str, dict] = {}
        for response in [response_btc, response_eth]:
            response_dict = response.json()
            for el in response_dict['result']:
                exchange_info[el['instrument_name']] = el

        # self.exchange_info = exchange_info
        return exchange_info

    def price_precision(self, raw_price: float, symbol: str) -> float:

        min_trade_amount = self.exchange_info[symbol]['min_trade_amount']
        if min_trade_amount < 1:
            raise NotImplementedError("should implement <1 case")
        else:
            return int(raw_price)

async def manage_heartbeat(websocket: WebSocketClientProtocol):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 9098,
                "method": "public/set_heartbeat",
                "params": {
                    "interval": 10
                }
            }
            
        msg_continuing = \
        {
            "jsonrpc": "2.0",
            "id": 9098,
            "method": "public/test",
            "params": {
                "interval": 10
            }
        }
        await websocket.send(json.dumps(msg))
        _ = await websocket.recv()

        while True:
            res = await websocket.recv()
            res_dict = json.loads(res)
            try:
                if res_dict["params"]['type'] == "test_request":
                    print(res_dict)
                    websocket.send(json.dumps(msg_continuing))
            except KeyError:
                continue