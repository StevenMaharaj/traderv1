from dataclasses import dataclass
from accountHandlers.account import AccountHandler
import asyncio
from typing import List
import json
import websockets
import keys
from auth import DeribtAuth
from queue import Queue

@dataclass
class DeribitOrder(AccountHandler):
    symbols: List[str]
    event_queue: Queue
    
    async def connect(self, msg):
        deribit_auth = DeribtAuth(keys.DeribtTestSteve['api_key'],keys.DeribtTestSteve['secret_key'])
        async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
            await deribit_auth.auth(websocket)
            await websocket.send(msg)
            response = await websocket.recv()
            while websocket.open:
                response = await websocket.recv()
                # do something with the notifications...
                # self.event_queue.put_nowait(self.to_market_event(response))
                self.event_queue.put_nowait(response)


    def start_stream(self):
        print("here")
        
        msg = \
            {"jsonrpc": "2.0",
             "method": "public/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"user.changes.{symbol}.raw" for symbol in self.symbols]}
             }
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.connect(json.dumps(msg)))
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)