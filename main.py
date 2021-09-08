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
from Strategies.ScalperDeribit import scalper_deribit 
from portfolio import Portfolio


log_folder = 'logs'
now: datetime = datetime.now()
now_string = datetime.strftime(now, '%y%m%d%H-%M-%S')

logging.basicConfig(filename=os.path.join(log_folder, f'{now_string}.log'),
                    level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


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

portfolio = Portfolio({}, {})

deribit_scalper = scalper_deribit.Scalper(event_queue, signal_event_queue,
                  working_orders=5, portfolio=portfolio,
                  exchange='deribit',symbols=["BTC-PERPETUAL"], is_live=is_live,order_dist=20)

deribit_scalper.run()
