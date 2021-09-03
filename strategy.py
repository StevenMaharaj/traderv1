from dataclasses import dataclass

from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError("should implement run")

    def connect_streams(self):
        raise NotImplementedError("should implement connect_streams")


