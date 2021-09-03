import unittest
from portfolio import *
from datetime import datetime


class TestPortfolioOrderEvent(unittest.TestCase):
    def setUp(self):
        self.p = Portfolio({}, {})
        self.open_order = OrderEvent(event_type='ORDER',
                                     exchange='deribit',
                                     product_type='future',
                                     symbol='BTC-PERPETUAL',
                                     ts=1630288390359,
                                     state='open',
                                     qty=10.0,
                                     price=48434.5,
                                     volume=10.0/48434.5,
                                     isBuy=True,
                                     isLimit=True,
                                     time_in_force='GTC',
                                     id="6461552120")
        self.filled_order = OrderEvent(event_type='ORDER',
                                       exchange='deribit',
                                       product_type='future',
                                       symbol='BTC-PERPETUAL',
                                       ts=1630288390359,
                                       state='filled',
                                       qty=10.0,
                                       price=48434.5,
                                       volume=10.0/48434.5,
                                       isBuy=True,
                                       isLimit=True,
                                       time_in_force='GTC',
                                       id="6461552120")
        self.cancelled_order = OrderEvent(event_type='ORDER',
                                          exchange='deribit',
                                          product_type='future',
                                          symbol='BTC-PERPETUAL',
                                          ts=1630288390359,
                                          state='cancelled',
                                          qty=10.0,
                                          price=48434.5,
                                          volume=10.0/48434.5,
                                          isBuy=True,
                                          isLimit=True,
                                          time_in_force='GTC',
                                          id="6461552120")
        self.resopen = Portfolio(positions={}, open_orders={'6461552120': OpenOrder(symbol='BTC-PERPETUAL', exchange='deribit', time=datetime(
            2021, 8, 30, 11, 53, 10, 359000), price=48434.5, qty=10.0, volume=0.0002064644003757652, isBuy=True, id='6461552120')})
        self.resfilled = Portfolio(positions={'6461552120': Position(symbol='BTC-PERPETUAL', exchange='deribit', price=48434.5, time=datetime(
            2021, 8, 30, 11, 53, 10, 359000), current_price=48434.5, qty=10.0, volume=0.0002064644003757652, isBuy=True, unrealized_profits=0.0, id='6461552120')}, open_orders={})

    def test_handle_OrderEvent_open(self):
        self.p.update(self.open_order)
        self.assertEqual(self.resopen, self.p)

    def test_handle_OrderEvent_filled(self):
        self.p.update(self.open_order)
        self.assertEqual(self.resopen, self.p)

        self.p.update(self.filled_order)

        self.assertEqual(self.resfilled, self.p)

    def test_handle_OrderEvent_cancelled(self):
        self.p.update(self.open_order)
        self.p.update(self.cancelled_order)
        self.assertEqual(self.p, Portfolio({}, {}))


class TestPortfolioTobMarketEvent(unittest.TestCase):

    def setUp(self):
        self.p = Portfolio({}, {})
        self.tob1 = TobMarketEvent(event_type='MARKET', symbol='BTC-PERPETUAL', ts=1630394748649, exchange='deribit',
                       product_type='future', market_event_type='TOB', AskP=47325.0, AskQ=191180.0, BidP=47323.0, BidQ=2000.0)

        self.tob2 = TobMarketEvent(event_type='MARKET', symbol='BTC-PERPETUAL', ts=1630394748655, exchange='deribit',
                       product_type='future', market_event_type='TOB', AskP=47325.5, AskQ=5800.0, BidP=47323.0, BidQ=2000.0)
        self.filled_order = OrderEvent(event_type='ORDER',
                                exchange='deribit',
                                product_type='future',
                                symbol='BTC-PERPETUAL',
                                ts=1630288390359,
                                state='filled',
                                qty=10.0,
                                price=48434.5,
                                volume=10.0/48434.5,
                                isBuy=True,
                                isLimit=True,
                                time_in_force='GTC',
                                id="6461552120")
        # self.res1 = 
    def test_no_position(self):
        self.p.update(self.tob1)
        
        self.assertEqual(self.p,Portfolio({}, {}))
        print()
    
    def test_1_position(self):
        self.p.update(self.filled_order)
        self.p.update(self.tob1)
        mid_price = (self.tob1.BidP +  self.tob1.AskP)*0.5
        self.assertEqual(self.p.positions[self.filled_order.id].price,mid_price)
        

if __name__ == '__main__':
    unittest.main()
