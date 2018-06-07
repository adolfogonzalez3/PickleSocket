
from PickleSocket.Networking import networkShell
import socket

class Server(networkShell):

    def __init__(self, host='localhost', port=50007, integer_length=8,
                 buffer_size=2**10):
        super().__init__(host, port, integer_length, buffer_size)

    def open(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(1)
        self.mailbox, _ = sock.accept()
        self.mailbox_socket = sock

    def close(self, type, value, traceback):
        self.mailbox.close()
        self.mailbox_socket.close()

    def read(self):
        '''Read Data received in Mailbox.'''
        amount = int.from_bytes(self.mailbox.recv(self.integer_length), byteorder='big')
        data = []
        while amount != 0:
            if amount >= self.buffer_size:
                d = self.mailbox.recv(self.buffer_size)
            else:
                d = self.mailbox.recv(amount)
            amount -= len(d)
            data.append(d)
        return b''.join(data)

    def read_stream(self):
        '''Read from connection pairs of length-payload pairs.

        Each message sent will be assumed to have its length sent
        as a 8 byte number preceding the payload. The length is used
        to recieve the full payload.
        The connection closes when a 0 length message is sent.
        '''
        amount = int.from_bytes(self.mailbox.recv(self.integer_length), byteorder='big')
        while amount != 0:
            data = []
            while amount != 0:
                if amount >= self.buffer_size:
                    d = self.mailbox.recv(self.buffer_size)
                else:
                    d = self.mailbox.recv(amount)
                amount -= len(d)
                data.append(d)
            yield b''.join(data)
            amount = int.from_bytes(self.mailbox.recv(self.integer_length), byteorder='big')