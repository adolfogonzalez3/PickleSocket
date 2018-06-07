
import pickle

from PickleSocket.Networking import TwoWaySocket

class PickleSocket(TwoWaySocket):

    def __init__(self, host='localhost', port=50007,
                integer_length=8, buffer_size=2**10, as_server=True):
        super().__init__(host, port, integer_length, buffer_size, as_server)

    def read(self):
        data = self.server.read()
        return pickle.loads(data)

    def read_stream(self):
        for data in self.server.read_stream():
            yield pickle.loads(data)

    def send(self, payload):
        payload = pickle.dumps(payload)
        self.client.send(payload)