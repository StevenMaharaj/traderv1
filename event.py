from dataclasses import dataclass, field


@dataclass
class Event:
    event_type: str
    symbol: str
    ts: int
    exchange: str
    product_type: str


@dataclass
class MarketEvent(Event):
    market_event_type: str


@dataclass
class TobMarketEvent(MarketEvent):
    AskP: float
    AskQ: float
    BidP: float
    BidQ: float


@dataclass
class TradeMarketEvent(MarketEvent):
    LastQ: float
    LastP: float


@dataclass
class CandleMarketEvent(MarketEvent):
    O: float
    H: float
    L: float
    C: float
    V: float


@dataclass
class OrderEvent(Event):
    state: str
    qty: float
    entry: float
    isBuy: bool
    isLimit: bool
    time_in_force: str

@dataclass
class SignalEvent(Event):
    qty: float
    price: float
    isBuy: bool
    isLimit: bool
    time_in_force: str



