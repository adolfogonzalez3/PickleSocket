import unittest
import socket

from threading import Thread
from PickleSocket import PickleSocket

def task():
    HOST = 'localhost'
    PORT = 50007
    INTEGER_LENGTH = 8
    with PickleSocket(HOST, PORT, INTEGER_LENGTH, as_server=False) as sock:
        sock.send({'string': 'Hello World!'})
        
class TestPickleSocket(unittest.TestCase):

    def test_read_send(self):
        HOST = 'localhost'
        PORT = 50007
        INTEGER_LENGTH = 8
        
        self.process = Thread(target=task, daemon=True)
        self.process.start()
        
        with PickleSocket(host=HOST, port=PORT, integer_length=INTEGER_LENGTH) as sock:
            dict = sock.read()
            self.assertEqual('Hello World!', dict['string'])
        
        

if __name__ == '__main__':
    unittest.main()