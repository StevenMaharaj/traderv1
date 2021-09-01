from websockets.protocol import State
from event import OrderEvent
import unittest
import json
from accountHandlers.deribit import DeribitOrder
from queue import Queue


class TestDeribitTob(unittest.TestCase):
    def setUp(self):
        event_queue = Queue()
        self.deribit_order = DeribitOrder(
            symbols=["BTC-PERPETUAL"], event_queue=event_queue, is_live=False)
        self.response = json.dumps({"jsonrpc": "2.0", "method": "subscription", "params": {"channel": "user.orders.BTC-PERPETUAL.raw", "data": {"web": True, "time_in_force": "immediate_or_cancel", "replaced": False, "reduce_only": False, "profit_loss": 0.0, "price": 48434.5, "post_only": False, "order_type": "limit", "order_state": "cancelled",
                                                                                                                                                "order_id": "6461552120", "max_show": 10.0, "last_update_timestamp": 1630288390359, "label": "", "is_liquidation": False, "instrument_name": "BTC-PERPETUAL", "filled_amount": 0.0, "direction": "buy", "creation_timestamp": 1630288390359, "commission": 0.0, "average_price": 0.0, "api": False, "amount": 10.0}}})
        self.res = OrderEvent(event_type='ORDER',
                                exchange='deribit',
                                product_type='future',
                                symbol='BTC-PERPETUAL',
                                ts=1630288390359,
                                state='cancelled',
                                qty=10.0,
                                price=48434.5,
                                volume = 10.0/48434.5,
                                isBuy=True,
                                isLimit=True,
                                time_in_force='immediate_or_cancel',
                                id="6461552120")

    def test_to_market_event(self):
        self.assertEqual(self.deribit_order.to_order_event(
            self.response), self.res)


if __name__ == '__main__':
    unittest.main()
