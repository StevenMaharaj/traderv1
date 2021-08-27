from queue import Queue
from threading import Thread
from dataHandlers.deribit import DeribitTOB
import sys
from event import Event
from accountHandlers.deribit import DeribitOrder

event_queue = Queue()


deribit_tob = DeribitTOB(["ETH-PERPETUAL"],event_queue)
deribit_orders = DeribitOrder(["BTC-PERPETUAL"],event_queue)

# t1 = Thread(target=deribit_tob.start_stream,daemon=True)
# # t1.daemon = True
# t1.start()

t2 = Thread(target=deribit_orders.start_stream,daemon=True)
t2.daemon = True
t2.start()

while True:
    try:
        event = event_queue.get()
        print(event)
    except KeyboardInterrupt:
        sys.exit(1)
