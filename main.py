from queue import Queue
from threading import Thread
from dataHandlers.deribit import DeribitTOB
import sys
from event import Event
from accountHandlers.deribit import DeribitOrder
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--isLive", help="Live trading or test")
args = parser.parse_args()


is_live: bool = eval(args.isLive)

if is_live:
    print("This seesion will run live")
else:
    print("This session is a test")


event_queue = Queue()


# deribit_tob = DeribitTOB(["ETH-PERPETUAL"],event_queue,is_live)
deribit_orders = DeribitOrder(["BTC-PERPETUAL"],event_queue,is_live)

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
