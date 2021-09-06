import unittest
from exchangeInfo import deribit
class TestDeribit(unittest.TestCase):

    def test_get_exchange_info(self):
        is_live = False
        res = deribit.get_exchange_info(is_live)
        for sym in ['ETH-PERPETUAL','BTC-PERPETUAL']:
            self.assertTrue(sym in res.keys())
