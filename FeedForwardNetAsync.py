
from enum import Enum, auto
from queue import Queue
import threading
from threading import Thread

from FeedForwardNet import FeedForwardNet

class FFNetFunctions(Enum):
    predict_on_batch = auto()
    train_on_batch = auto()

class Message(object):
    def __init__(self, header, data):
        self.header = header
        self.data = data

def net_async(pipe, args, kwargs):
    mydata = threading.local()
    mydata.net = FeedForwardNet(*args, **kwargs)
    while True:
        mydata.message = pipe[0].get()
        data = mydata.message.data
        if mydata.message.header == FFNetFunctions.predict_on_batch:
            pipe[1].put(mydata.net.predict_on_batch(data))
        elif mydata.message.header == FFNetFunctions.train_on_batch:
            loss = mydata.net.train_on_batch(data[0], data[1])
            #pipe[1].put(loss)
    
class FeedForwardNetAsync(object):
    '''An interface that abstracts the talking with an asynchronous Agent.'''
    def __init__(self, *args, **kwargs):
        parent_conn = child_conn = (Queue(), Queue())
        self.conn = parent_conn
        self.process = Thread(target=net_async, args=(child_conn,
                                                        args, kwargs),
                                                        daemon=True)
        self.process.start()

    def predict_on_batch(self, batch):
        '''Send save message and have the agent save.'''
        self.conn[0].put(Message(FFNetFunctions.predict_on_batch, batch))
        #return self.conn[1].get()
        
    def collect(self):
        return self.conn[1].get()

    def train_on_batch(self, batch, labels):
        '''Send train message and have the agent train asynchronously.'''
        self.conn[0].put(Message(FFNetFunctions.train_on_batch, (batch, labels)))
        #return self.conn[1].get()