from queue import Queue
from threading import Thread
from dataHandlers.deribit import DeribitTOB
import sys
from event import Event

event_queue = Queue()


deribit_tob = DeribitTOB(["ETH-PERPETUAL"],event_queue)


t1 = Thread(target=deribit_tob.start_stream,daemon=True)
# t1.daemon = True
t1.start()

while True:
    try:
        event: Event = event_queue.get()
        print(event)
    except KeyboardInterrupt:
        sys.exit(0)
