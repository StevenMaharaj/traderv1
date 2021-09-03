from dataclasses import dataclass
import logging
from queue import Queue
from portfolio import Portfolio
from strategy import Strategy
from typing import List, Mapping
from threading import Thread

from dataHandlers.deribit import DeribitTOB
import sys
from event import Event, SignalEvent
from accountHandlers.deribit import DeribitOrder
from executionHandlers.deribit import DeribitExecutionHandler
from datetime import datetime


@dataclass
class Scalper(Strategy):
    event_queue: Queue
    signal_event_queue: Queue
    working_orders: int
    portfolio: Portfolio
    exchange: str
    symbols: List[str]
    is_live: bool


    def connect_streams(self):
        if self.exchange == 'deribit':
            self.handle_deribit_connection()


    def run(self):
        self.connect_streams()
        while True:
            try:
                pass
                # inp = input("(isBuy,price)\n")
                # signal_event_queue.put_nowait(make_signal(*eval(inp)))
                event: Event = self.event_queue.get()
                self.portfolio.update(event)
                print(self.portfolio)
                logging.info(event)
            except NameError:
                logging.exception("exception")
            
            except KeyboardInterrupt:
                logging.exception("exception")
                sys.exit(1)


    def handle_deribit_connection(self):
        deribit_tob = DeribitTOB(self.symbols, self.event_queue, self.is_live)

        deribit_orders = DeribitOrder(self.symbols, self.event_queue, self.is_live)


        # deribit_execution_handler = DeribitExecutionHandler(
        #     is_live=is_live,signal_event_queue=signal_event_queue)

        t1 = Thread(target=deribit_tob.start_stream,daemon=True)
        t2 = Thread(target=deribit_orders.start_stream, daemon=True)
        
        t1.start()
        t2.start()

