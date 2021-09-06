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
                self.handle_TobMarketEvent(event)
        elif isinstance(event,OrderEvent):
            self.handle_OrderEvent(event)
    

    def handle_TobMarketEvent(self,event: TobMarketEvent):
        if len(self.positions) > 0:
            mid_price = (event.AskP + event.BidP)*0.5

            for id, position in self.positions.items():
                if (position.symbol == event.symbol) and (position.exchange == event.exchange):
                    self.positions[id].price = mid_price
                    if self.positions[id].isBuy:
                        self.positions[id].unrealized_profits = (mid_price - self.positions[id].price) * self.positions[id].volume
                    else:
                        self.positions[id].unrealized_profits = -1.0*(mid_price - self.positions[id].price) * self.positions[id].volume
                     

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
            position_key: str = f"{event.symbol}-{event.exchange}"
            is_first_filled_order = False if position_key in self.positions.keys() else True
            if is_first_filled_order:
                self.open_orders.pop(event.id, None)
                self.positions[f"{event.symbol}-{event.exchange}"] = Position(
                    symbol=event.symbol,
                    exchange=event.exchange,
                    time=datetime.fromtimestamp(event.ts/1000),
                    qty=event.qty*(event.isBuy*2.0-1.0),
                    volume=event.volume, 
                    isBuy=event.isBuy,
                    price=event.price,
                    unrealized_profits = 0.0,
                    current_price=event.price,
                    id=event.id,
                )
            else:
                update_qty: float = event.qty*(event.isBuy*2.0-1.0)
                volume_qty: float = (event.qty/event.price)*(event.isBuy*2.0-1.0)
                
                if self.positions[position_key] != event.isBuy:
                    if abs(self.positions[position_key].qty + update_qty) < 0.00000001: # reduce to zero
                        self.positions.pop(position_key, None)
                    else:
                        self.positions[position_key].qty += update_qty
                        self.positions[position_key].volume += volume_qty


                elif (event.isBuy == self.positions[position_key].isBuy): # add to position
                    self.positions[position_key].qty += update_qty
                    self.positions[position_key].volume += volume_qty


        elif event.state == "cancelled":
            self.open_orders.pop(event.id)


