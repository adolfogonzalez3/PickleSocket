
import socket
import pickle

from PickleSocket.Networking import Server, Client

class TwoWaySocket(object):
    def __init__(self, host='localhost', port=50007,
                integer_length=8, buffer_size=2**10, as_server=True):
        self.integer_length = integer_length
        self.buffer_size = buffer_size
        self.host = host
        self.port = port
        self.as_server = as_server
        
    def open_as_server(self):
        self.server = Server(host=self.host, port=self.port,
                            integer_length=self.integer_length,
                            buffer_size=self.buffer_size)
        self.server.open()
        host = pickle.loads(self.read())
        port = int(pickle.loads(self.read()))
        self.client = Client(host=host, port=port,
                            integer_length=self.integer_length,
                            buffer_size=self.buffer_size)
        self.client.open()
        
    def open_as_client(self):
        self.client = Client(host=self.host, port=self.port,
                            integer_length=self.integer_length,
                            buffer_size=self.buffer_size)
        self.client.open()
        self.send(pickle.dumps('localhost'))
        self.send(pickle.dumps(self.port+1))
        self.server = Server(host='localhost', port=self.port+1,
                            integer_length=self.integer_length,
                            buffer_size=self.buffer_size)
        self.server.open()
        
    def open(self):
        if self.as_server is True:
            self.open_as_server()
        else:
            self.open_as_client()

    def read(self):
        return self.server.read()

    def read_stream(self):
        for data in self.server.read_stream():
            yield data

    def send(self, payload):
        self.client.send(payload)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close(type, value, traceback)

    def close(self, type, value, traceback):
        self.client.close(type, value, traceback)
        self.server.close(type, value, traceback)