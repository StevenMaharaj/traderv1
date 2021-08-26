from event import TobMarketEvent
import unittest
import json
from dataHandlers.deribit import DeribitTOB
from queue import Queue


class TestDeribitTob(unittest.TestCase):
    def setUp(self):
        event_queue = Queue()
        self.deribit_tob = DeribitTOB(["ETH-PERPETUAL"], event_queue)
        self.response = json.dumps({"jsonrpc": "2.0", "method": "subscription", "params": {"channel": "quote.ETH-PERPETUAL", "data": {"timestamp": 1629968039462,
                                                                                                                                      "instrument_name": "ETH-PERPETUAL", "best_bid_price": 3107.2, "best_bid_amount": 34944.0, "best_ask_price": 3107.25, "best_ask_amount": 240.0}}})
        self.res = TobMarketEvent(exchange='deribit',
                                  product_type='future',
                                  event_type='MARKET',
                                  market_event_type='TOB',
                                  symbol='ETH-PERPETUAL',
                                  ts=1629968039462, AskP=3107.25, AskQ=240.0, BidP=3107.2, BidQ=34944.0)

    def test_to_market_event(self):
        self.assertEqual(self.deribit_tob.to_market_event(
            self.response), self.res)


if __name__ == '__main__':
    unittest.main()
