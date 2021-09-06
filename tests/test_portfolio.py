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



    def test_handle_OrderEvent_cancelled(self):
        self.p.update(self.open_order)
        self.p.update(self.cancelled_order)
        self.assertEqual(self.p, Portfolio({}, {}))


class TestPortfolioOrderEventFills(unittest.TestCase):
    def setUp(self):
        self.p = Portfolio({}, {})
        self.p_empty = Portfolio({}, {})


    def test_buy_sell(self):
        buy_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897431900, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001903565377952906, price=52533.0, isBuy=True, isLimit=False, time_in_force='good_til_cancelled', id='6503574855')
        sell_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897433646, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001961534312138955, price=50980.5, isBuy=False, isLimit=False, time_in_force='good_til_cancelled', id='6503574903')
        self.p.update(buy_event)
        self.p.update(sell_event)
        self.assertEqual(self.p, Portfolio({}, {}))

    def test_sell_buy(self):
        buy_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897431900, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001903565377952906, price=52533.0, isBuy=True, isLimit=False, time_in_force='good_til_cancelled', id='6503574855')
        sell_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897433646, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001961534312138955, price=50980.5, isBuy=False, isLimit=False, time_in_force='good_til_cancelled', id='6503574903')
        self.p.update(sell_event)
        self.p.update(buy_event)
        self.assertEqual(self.p, Portfolio({}, {}))

    def test_buy_buy(self):
        buy_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897431900, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001903565377952906, price=52533.0, isBuy=True, isLimit=False, time_in_force='good_til_cancelled', id='6503574855')
        sell_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897433646, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001961534312138955, price=50980.5, isBuy=False, isLimit=False, time_in_force='good_til_cancelled', id='6503574903')
        self.p.update(buy_event)
        self.p.update(buy_event)
        self.assertEqual(self.p.positions['BTC-PERPETUAL-deribit'].qty, 20.0)

    def test_sell_sell(self):
        buy_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897431900, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001903565377952906, price=52533.0, isBuy=True, isLimit=False, time_in_force='good_til_cancelled', id='6503574855')
        sell_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897433646, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001961534312138955, price=50980.5, isBuy=False, isLimit=False, time_in_force='good_til_cancelled', id='6503574903')
        self.p.update(sell_event)
        self.p.update(sell_event)
        self.assertEqual(self.p.positions['BTC-PERPETUAL-deribit'].qty, -20.0)


    def test_buy_buy_sell(self):
        buy_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897431900, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001903565377952906, price=52533.0, isBuy=True, isLimit=False, time_in_force='good_til_cancelled', id='6503574855')
        sell_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897433646, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001961534312138955, price=50980.5, isBuy=False, isLimit=False, time_in_force='good_til_cancelled', id='6503574903')
        self.p.update(buy_event)
        self.p.update(buy_event)
        self.p.update(sell_event)
        self.assertEqual(self.p.positions['BTC-PERPETUAL-deribit'].qty, 10.0)

    def test_sell_buy_sell(self):
        buy_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897431900, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001903565377952906, price=52533.0, isBuy=True, isLimit=False, time_in_force='good_til_cancelled', id='6503574855')
        sell_event = OrderEvent(event_type='ORDER', symbol='BTC-PERPETUAL', ts=1630897433646, exchange='deribit', product_type='future', state='filled', qty=10.0, volume=0.0001961534312138955, price=50980.5, isBuy=False, isLimit=False, time_in_force='good_til_cancelled', id='6503574903')
        self.p.update(sell_event)
        self.p.update(buy_event)
        self.assertEqual(self.p,self.p_empty)
        self.p.update(sell_event)
        self.assertEqual(self.p.positions['BTC-PERPETUAL-deribit'].qty, -10.0)



        

if __name__ == '__main__':
    unittest.main()
