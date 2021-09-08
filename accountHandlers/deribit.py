from dataclasses import dataclass
from accountHandlers.account import AccountHandler
import asyncio
from typing import List, Mapping
import json
import websockets
import keys
from auth import DeribtAuth
from queue import Queue
from event import OrderEvent


# deribit_order_state_map: Mapping[str,str] = {}

# Order state: "open", "filled", "rejected", "cancelled", "untriggered"
@dataclass
class DeribitOrder(AccountHandler):
    symbols: List[str]
    event_queue: Queue
    is_live: bool
    

    async def connect(self, msg):

        deribit_auth = DeribtAuth(
            keys.DeribtTestSteve['api_key'], keys.DeribtTestSteve['secret_key'])
        if self.is_live:
            url = 'wss://www.deribit.com/ws/api/v2'
        else:
            url = 'wss://test.deribit.com/ws/api/v2'

        async with websockets.connect(url) as websocket:
            await deribit_auth.auth(websocket)
            await websocket.send(msg)
            response = await websocket.recv()
            while websocket.open:
                response = await websocket.recv()
                # do something with the notifications...
                # self.event_queue.put_nowait(self.to_market_event(response))
                self.event_queue.put_nowait(self.to_order_event(response))

    def start_stream(self):

        msg = \
            {"jsonrpc": "2.0",
             "method": "public/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"user.orders.{symbol}.raw" for symbol in self.symbols]}
             }
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.connect(json.dumps(msg)))
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)

    def to_order_event(self, response: str) -> OrderEvent:
        temp = json.loads(response)
        # print(temp['params']['data'])

        return OrderEvent(event_type='ORDER',
                              exchange='deribit',
                              product_type='future',
                              symbol=temp['params']['data']['instrument_name'],
                              ts=temp['params']['data']['last_update_timestamp'],
                              state=temp['params']['data']['order_state'],
                              volume=temp['params']['data']["amount"]/temp['params']['data']["price"],
                              qty=temp['params']['data']["amount"],
                              price=temp['params']['data']["price"],
                              isBuy=True if temp['params']['data']["direction"]=='buy' else False,
                              isLimit=True if temp['params']['data']["order_type"]=='limit' else False,
                              time_in_force=temp['params']['data']["time_in_force"],
                              id=temp['params']['data']['order_id'])
