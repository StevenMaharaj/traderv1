from dataclasses import dataclass
from datetime import datetime
from typing import Mapping
from event import *



@dataclass
class Position:
    symbol: str
    exchange: str
    price: float
    time: datetime
    current_price: float
    qty: float
    volume: float
    isBuy: bool
    unrealized_profits: float
    id: str
    

@dataclass
class OpenOrder:
    symbol: str
    exchange: str
    time: datetime
    price: float
    qty: float
    volume: float
    isBuy: bool
    id: str

@dataclass
class Portfolio:
    positions: Mapping[str,Position]
    open_orders: Mapping[str,OpenOrder]

    def update(self,event: Event):
        if isinstance(event,MarketEvent):
            if isinstance(event,TobMarketEvent):
                pass
        elif isinstance(event,OrderEvent):
            self.handle_OrderEvent(event)
    
    def handle_OrderEvent(self,event: OrderEvent):
        if event.state == "open":
            self.open_orders[event.id] = OpenOrder(
                symbol=event.symbol,
                exchange=event.exchange,
                time=datetime.fromtimestamp(event.ts/1000),
                qty=event.qty,
                volume=event.volume, 
                isBuy=event.isBuy,
                id=event.id,
                price=event.price
            )
        elif event.state == "filled":
            self.open_orders.pop(event.id, None)
            self.positions[event.id] = Position(
                symbol=event.symbol,
                exchange=event.exchange,
                time=datetime.fromtimestamp(event.ts/1000),
                qty=event.qty,
                volume=event.volume, 
                isBuy=event.isBuy,
                price=event.price,
                unrealized_profits = 0.0,
                current_price=event.price,
                id=event.id,
            )
        
        elif event.state == "cancelled":
            self.open_orders.pop(event.id)


