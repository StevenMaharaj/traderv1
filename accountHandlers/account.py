from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AccountHandler(ABC):
    apiKey: str
    secret: str

    @abstractmethod
    def start_stream(self):
        raise NotImplementedError("should implement start_stream")

    def connect(self):
        raise NotImplementedError("should implement connect")

    @abstractmethod
    def to_order_event():
        raise NotImplementedError("should implement to_market_event")
