import unittest
from executionHandlers.deribit import *
from queue import Queue
from typing import Mapping


class TestDeribitEH(unittest.TestCase):
    def setUp(self):
        self.is_live = False
        signal_event_queue = Queue()
        self.deh = DeribitExecutionHandler(is_live=self.is_live,signal_event_queue=signal_event_queue)
        self.ei: Mapping[str,dict] = self.deh.get_exchange_info()
        self.symbol = 'BTC-PERPETUAL'

    def test_get_exchange_info(self):
        self.assertEqual(self.ei['ETH-PERPETUAL']['settlement_period'],'perpetual')

    def test_price_precision(self):
        min_trade_amount = self.ei[self.symbol]['min_trade_amount']
        self.assertEqual(min_trade_amount,10)
        



if __name__ == '__main__':
    unittest.main()
