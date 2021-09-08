from dataclasses import dataclass
import logging
from queue import Queue
from portfolio import Portfolio
from strategy import Strategy
from typing import List, Mapping
from threading import Thread

from dataHandlers.deribit import DeribitTOB
import sys
from event import Event, SignalEvent, OrderEvent,CancelSignalEvent, TobMarketEvent
from accountHandlers.deribit import DeribitOrder
from executionHandlers.deribit import DeribitExecutionHandler
from datetime import datetime
from exchangeInfo.deribit import get_exchange_info




@dataclass
class Scalper(Strategy):
    event_queue: Queue
    signal_event_queue: Queue
    working_orders: int
    portfolio: Portfolio
    exchange: str
    symbols: List[str]
    is_live: bool
    order_dist: int #(tick)

    def __post_init__(self):
        self.EI = get_exchange_info(self.is_live)
        self.n_tob_events = 0

    def connect_streams(self):
        if self.exchange == 'deribit':
            self.handle_deribit_connection()

    def run(self):
        self.connect_streams()
        while True:
            try:
                # inp = input("(isBuy,price)\n")
                # signal_event_queue.put_nowait(make_signal(*eval(inp)))
                event: Event = self.event_queue.get()
                self.portfolio.update(event)
                # print(self.portfolio.positions)
                self.strategy_logic(event)
                

                # print(len(self.portfolio.open_orders))
                # print(type(event))
            except NameError:
                logging.exception("exception")

            except KeyboardInterrupt:
                logging.exception("exception")
                sys.exit(1)

    def strategy_logic(self, event: Event):
        
        if isinstance(event, OrderEvent):
                # self.n_tob_events = 0
                if event.state == "filled":
                    self.signal_event_queue.put_nowait(self.makeSignalEvent(event))
                    # logging.info(event)
                    
        elif isinstance(event,TobMarketEvent):
            self.n_tob_events += 1 
            mid_price = (event.AskP + event.BidP)*0.5
            tick_size = self.EI[event.symbol]['tick_size']
            (n_bids, n_asks) = self.portfolio.get_n_bid_ask()
            # print(n_bids, n_asks)

            if self.n_tob_events % (20) == 0:
                self.n_tob_events = 0
                if n_bids < self.working_orders:
                    for i in range(n_bids+1,self.working_orders+1):
                        # print('her')
                        self.signal_event_queue.put_nowait(self.makeSignalEvent_stackorders(event,
                        price=mid_price - tick_size*self.order_dist*i,
                        isBuy=True))

                if n_asks < self.working_orders:
                    for i in range(n_asks+1,self.working_orders+1):
                        self.signal_event_queue.put_nowait(self.makeSignalEvent_stackorders(event,
                        price=mid_price + tick_size*self.order_dist*i,
                        isBuy=False))
            if self.n_tob_events % (10) == 0:
                if  n_bids > self.working_orders or n_asks > self.working_orders:
                    for id,oo in self.portfolio.open_orders.items():
                        # print(abs(oo.price - mid_price))
                        # print(abs(self.working_orders*self.order_dist*tick_size - mid_price))
                        if abs(oo.price - mid_price) > self.working_orders*self.order_dist*tick_size:
                            self.signal_event_queue.put_nowait(self.makeSignalEventCancel(id))
                            # logging.info(event)







    def get_order_qty(self):
        return 10

    def makeSignalEvent(self, event: OrderEvent):
        delta_od:float = self.order_dist*self.EI[event.symbol]['tick_size']
        return SignalEvent(event_type="SIGNAL", 
        symbol=event.symbol, 
        ts=event.ts, 
        exchange=event.exchange, 
        product_type='future', 
        qty=self.get_order_qty(), 
        price=event.price + delta_od if event.isBuy else event.price - delta_od, 
        isBuy=not event.isBuy, 
        isLimit=True, 
        time_in_force="GTC")

    def makeSignalEventCancel(self, id):
        
        return CancelSignalEvent(event_type="SIGNAL", 
        symbol="", 
        ts=0, 
        exchange='deribit', 
        product_type='future', 
        qty=0.0, 
        price=0.0, 
        isBuy=False, 
        isLimit=False, 
        time_in_force="GTC",
        id=id)


    def makeSignalEvent_stackorders(self,event:TobMarketEvent, price:float,isBuy:bool):
        return SignalEvent(event_type="SIGNAL", 
        symbol=event.symbol, 
        ts=event.ts, 
        exchange=event.exchange, 
        product_type='future', 
        qty=self.get_order_qty(), 
        price=price, 
        isBuy=isBuy, 
        isLimit=True, 
        time_in_force="GTC")


    def handle_deribit_connection(self):
        deribit_tob = DeribitTOB(self.symbols, self.event_queue, self.is_live)

        deribit_orders = DeribitOrder(
            self.symbols, self.event_queue, self.is_live)

        deribit_execution_handler = DeribitExecutionHandler(
            is_live=self.is_live,signal_event_queue=self.signal_event_queue)

        t1 = Thread(target=deribit_tob.start_stream, daemon=True)
        t2 = Thread(target=deribit_orders.start_stream, daemon=True)
        t3 = Thread(target=deribit_execution_handler.start_stream, daemon=True)



        t1.start()
        t2.start()
        t3.start()
