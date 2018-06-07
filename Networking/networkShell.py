
from abc import ABC, abstractmethod


class networkShell(ABC):
    '''An abstract class used as the base for the client and server classes.
    
    Should not be used as is.'''
    
    def __init__(self, host='localhost', port=50007,
                integer_length=8, buffer_size=2**10):
        self.integer_length = integer_length
        self.buffer_size = buffer_size
        self.host = host
        self.port = port

    @abstractmethod
    def open(self):
        pass
        
    @abstractmethod
    def close(self, type, value, traceback):
        pass
        
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close(type, value, traceback)
        
    def get_port(self):
        return self.port