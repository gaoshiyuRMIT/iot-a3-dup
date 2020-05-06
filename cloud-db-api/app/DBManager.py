from abc import ABC, ABCMeta, abstractmethod
from .db import getConn
from .errors.api_exceptions import InvalidArgument

class DBManager(ABC):
    FIELDS = []
    TABLE_NAME = ""

    @property
    def conn(self):
        return getConn()

    @classmethod
    def keepValidFieldsOnly(cls, d: dict, throw=False) -> dict:
        if throw:
            invalidKeys = set(d.keys()) - set(cls.FIELDS)
            if len(invalidKeys) > 0:
                message = "invalid key(s): {}".format(", ".join(invalidKeys))
                raise InvalidArgument(message)
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

