import unittest
from event import SignalEvent
from datetime import datetime


class TestSignalEvent(unittest.TestCase):
    def test_signalEvent(self):
        buy_signal = SignalEvent(event_type="SIGNAL",
                                 symbol="BTC-PERPETUAL",
                                 ts=int(datetime.timestamp(
                                     datetime.now())*1000),
                                 exchange='deribit',
                                 product_type='future',
                                 qty=10,
                                 price=0,
                                 isBuy=True,
                                 isLimit=False,
                                 time_in_force="GTC"
                                 )
        # print(buy_signal)
        self.assertEqual(buy_signal.event_type, 'SIGNAL')
if __name__ == '__main__':
    unittest.main()