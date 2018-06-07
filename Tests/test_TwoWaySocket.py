import unittest
import socket

from threading import Thread
from PickleSocket.Networking import TwoWaySocket

def task():
    HOST = 'localhost'
    PORT = 50007
    INTEGER_LENGTH = 8
    with TwoWaySocket(HOST, PORT, INTEGER_LENGTH, as_server=False) as sock:
        sock.send(b'Hello World!')
        
class TestTwoWaySocket(unittest.TestCase):

    def test_read_send(self):
        HOST = 'localhost'
        PORT = 50007
        INTEGER_LENGTH = 8
        
        self.process = Thread(target=task, daemon=True)
        self.process.start()
        
        with TwoWaySocket(host=HOST, port=PORT, integer_length=INTEGER_LENGTH) as sock:
            string = sock.read()
            self.assertEqual(b'Hello World!', string)
        
        

if __name__ == '__main__':
    unittest.main()