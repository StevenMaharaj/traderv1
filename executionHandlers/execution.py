from abc import ABC, abstractmethod
from dataclasses import dataclass
from event import SignalEvent
from typing import List, Mapping
# from deribit import DerbitExecutionHandler

@dataclass
class ExecutionHandler(ABC):

    @abstractmethod
    def execute_order(self,signal: SignalEvent):
        raise NotImplementedError("should implement execute_order")

    @abstractmethod
    def start_stream(self):
        raise NotImplementedError("should implement start_stream")

# @dataclass
# class ExecutionManager:
#     exchanges: List[str]
#     is_live: bool
    
#     def __post_init__(self):
#         self.execution_handlers: Mapping[str,ExecutionHandler]

#     def start(self):

#         if 'deribit' in self.exchanges:
#             self.execution_handlers['deribit'] = DerbitExecutionHandler(is_live=self.is_live.signal_event_queue)
#             self.execution_handlers['deribit'].start_stream()

        
