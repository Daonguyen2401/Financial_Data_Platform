from abc import ABC, abstractmethod

class StorageBase:
    def __init__(self):
        pass

    @abstractmethod
    def append(self, df, target):
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def write(self, df, target):
        raise NotImplementedError("Method not implemented")