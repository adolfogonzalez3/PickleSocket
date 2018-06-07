import unittest
import socket

from threading import Thread
from PickleSocket.Networking import Client

def task():
    HOST = 'localhost'
    PORT = 50007
    INTEGER_LENGTH = 8
    
    with Client(host=HOST, port=PORT, integer_length=INTEGER_LENGTH) as client:
            client.send(b'Hello World!')
        
class TestClient(unittest.TestCase):

    def test_send(self):
        HOST = 'localhost'
        PORT = 50007
        INTEGER_LENGTH = 8
        
        self.process = Thread(target=task, daemon=True)
        self.process.start()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(1)
            mailbox, _ = sock.accept()
            
            # Should receive integer N as eight bytes followed by N bytes.
            integer_bytes = mailbox.recv(8)
            integer = int.from_bytes(integer_bytes, byteorder='big')
            self.assertEqual(integer, 12)
            string = mailbox.recv(integer)
            self.assertEqual(string, b'Hello World!')
            
            mailbox.close()
        
        

if __name__ == '__main__':
    unittest.main()