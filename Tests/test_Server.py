import unittest
import socket

from threading import Thread
from PickleSocket.Networking import Server

def task():
    HOST = 'localhost'
    PORT = 50007
    INTEGER_LENGTH = 8
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        while True:
            try:
                sock.connect((HOST, PORT))
                break
            except ConnectionRefusedError:
                sleep(1)
        string = b'Hello World!'
        length = len(string).to_bytes(INTEGER_LENGTH, byteorder='big')
        sock.sendall(length)
        sock.sendall(string)
        
class TestServer(unittest.TestCase):

    def test_read(self):
        HOST = 'localhost'
        PORT = 50007
        INTEGER_LENGTH = 8
        
        self.process = Thread(target=task, daemon=True)
        self.process.start()
        
        with Server(host=HOST, port=PORT, integer_length=INTEGER_LENGTH) as serv:
            string = serv.read()
            self.assertEqual(b'Hello World!', string)
        
        

if __name__ == '__main__':
    unittest.main()