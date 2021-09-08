from queue import Queue
import unittest
from event import *   
from portfolio import Portfolio

from Strategies import scalper_deribit

class TestScalper(unittest.TestCase):
    def test_makeSignalEvent(self):
        portfolio = Portfolio({}, {})
        event_queue = Queue()
        signal_event_queue = Queue()
        is_live = False
        deribit_scalper = scalper_deribit.Scalper(event_queue, signal_event_queue,
                  working_orders=1, portfolio=portfolio,
                  exchange='deribit',symbols=["BTC-PERPETUAL"], is_live=is_live,order_dist=3)
        fill_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630972136653, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001871362539064693, price=53437.0, isBuy=True, isLimit=True, time_in_force='good_til_cancelled', id='6507759441')

        res = deribit_scalper.makeSignalEvent(fill_event)
        print(res)

        self.assertEqual(res.price,fill_event.price + 3*0.5 )