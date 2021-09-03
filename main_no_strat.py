from executionHandlers.execution import ExecutionHandler
from queue import Queue
from threading import Thread
from dataHandlers.deribit import DeribitTOB
import sys
from event import Event, SignalEvent
from accountHandlers.deribit import DeribitOrder
from executionHandlers.deribit import DeribitExecutionHandler
from datetime import datetime
from time import sleep
import argparse
import logging
import os



log_folder='logs'
now: datetime = datetime.now()
now_string=datetime.strftime(now,'%y%m%d%H-%M-%S')

logging.basicConfig(filename= os.path.join(log_folder,f'{now_string}.log'),
    level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--isLive", help="Live trading or test")
args = parser.parse_args()


is_live: bool = eval(args.isLive)

if is_live:
    print("This seesion will run live")
else:
    print("This session is a test")


event_queue = Queue()
signal_event_queue = Queue()


deribit_tob = DeribitTOB(["BTC-PERPETUAL"],event_queue,is_live)
deribit_orders = DeribitOrder(["BTC-PERPETUAL"], event_queue, is_live)


deribit_execution_handler = DeribitExecutionHandler(
    is_live=is_live,signal_event_queue=signal_event_queue)

t1 = Thread(target=deribit_tob.start_stream,daemon=True)
# t1.daemon = True
t1.start()

t2 = Thread(target=deribit_orders.start_stream, daemon=True)
t2.daemon = True
t2.start()

# t3 = Thread(target=deribit_execution_handler.start_stream, daemon=True)
# t3.daemon = True
# t3.start()

def make_signal(isBuy: bool,price:float) -> SignalEvent:
    return SignalEvent(event_type="SIGNAL",
                        symbol="BTC-PERPETUAL",
                        ts=int(datetime.timestamp(
                            datetime.now())*1000),
                        exchange='deribit',
                        product_type='future',
                        qty=10,
                        price=price,
                        isBuy=isBuy,
                        isLimit=True,
                        time_in_force="GTC"
                        )

sleep(2)
while True:
    try:
        pass
        # inp = input("(isBuy,price)\n")
        # signal_event_queue.put_nowait(make_signal(*eval(inp)))
        event = event_queue.get()
        print(event)
        logging.info(event)
    except NameError:
        logging.exception("exception")
    
    except KeyboardInterrupt:
        logging.exception("exception")
        sys.exit(1)
