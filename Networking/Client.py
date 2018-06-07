
from PickleSocket.Networking import networkShell
import socket
from time import sleep

class Client(networkShell):

    def __init__(self, host='localhost', port=50007, integer_length=8,
                 buffer_size=2**10):
        super().__init__(host, port, integer_length, buffer_size)
        self.sock = None

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect((self.host, self.port))
                break
            except ConnectionRefusedError:
                sleep(1)

    def close(self, type, value, traceback):
        self.sock.close()

    def send(self, payload):
        '''Send payload over connection.'''
        if self.sock is None:
            self.open()
        length = len(payload).to_bytes(self.integer_length, byteorder='big')
        self.sock.sendall(length)
        self.sock.sendall(payload)