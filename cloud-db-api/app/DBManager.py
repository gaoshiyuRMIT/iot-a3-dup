from abc import ABC, ABCMeta, abstractmethod
from . import app

class DBManager(ABC):
    FIELDS = []
    TABLE_NAME = ""

    def __init__(self):
        # TODO: use third-party library to create a connection
        self.conn = None

    @abstractmethod
    def getMany(self, filt: dict) -> list:
        return []

    @abstractmethod
    def getOne(self, id) -> dict:
        return {}

    @abstractmethod
    def updateOne(self, id, newVal: dict) -> bool:
        return True
    
    @abstractmethod
    def addOne(self, newVal: dict) -> bool:
        return True

