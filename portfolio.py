from dataclasses import dataclass
from datetime import datetime

@dataclass
class Position:
    symbol: str
    exchange: str
    entry: float
    entry_time: datetime
    price: float
    qty: float
    isBuy: bool
    state: str