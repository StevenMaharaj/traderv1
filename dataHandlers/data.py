import websockets
import asyncio
import json
from queue import Queue
import requests
from event import TobMarketEvent

from abc import ABC, abstractmethod


class DataHandler(ABC):

    @abstractmethod
    def start_stream(self):
        raise NotImplementedError("should implement start_stream")

    def connect(self):
        raise NotImplementedError("should implement connect")

    @abstractmethod
    def to_market_event():
        raise NotImplementedError("should implement to_market_event")




        
