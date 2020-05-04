from abc import ABC, ABCMeta, abstractmethod
from .db import getConn

class DBManager(ABC):
    FIELDS = []
    TABLE_NAME = ""

    @property
    def conn(self):
        return getConn()

    @classmethod
    def keepValidFieldsOnly(cls, d: dict) -> dict:
        return {k: d.get(k) for k in cls.FIELDS}

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

