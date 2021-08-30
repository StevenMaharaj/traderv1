from dataclasses import dataclass
import websockets
import asyncio
import json
from queue import Queue
import requests
from event import TobMarketEvent
from dataHandlers.data import DataHandler
from typing import List


@dataclass
class DeribitTOB(DataHandler):
    symbols: List[str]
    event_queue: Queue
    is_live: bool
    exchange: str = 'deribit',

    async def connect(self, msg):
        if self.is_live:
            url = 'wss://www.deribit.com/ws/api/v2'
        else:
            url = 'wss://test.deribit.com/ws/api/v2'
            
        async with websockets.connect(url) as websocket:
            await websocket.send(msg)
            response = await websocket.recv()
            while websocket.open:
                response = await websocket.recv()
                # do something with the notifications...
                self.event_queue.put_nowait(self.to_market_event(response))
                

    def start_stream(self):
        msg = \
            {"jsonrpc": "2.0",
             "method": "public/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"quote.{symbol}"for symbol in self.symbols]}
             }
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.connect(json.dumps(msg)))
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)

    def to_market_event(self, response: str) -> TobMarketEvent:
        temp = json.loads(response)
        return TobMarketEvent(event_type='MARKET',
                              market_event_type='TOB',
                              exchange='deribit',
                              product_type='future',
                              symbol=temp['params']['data']['instrument_name'],
                              ts=temp['params']['data']['timestamp'],
                              AskP=temp['params']['data']["best_ask_price"],
                              AskQ=temp['params']['data']["best_ask_amount"],
                              BidP=temp['params']['data']["best_bid_price"],
                              BidQ=temp['params']['data']["best_bid_amount"],)
