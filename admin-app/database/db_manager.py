#!/usr/bin/python3
import pymysql as p
from abc import ABC, abstractmethod

class DBManager(ABC):
    USER = "root"
    PASSWORD = "toor"
    HOST =  "35.201.0.12"
    DATABASE = "pi-database"

    """ Initialise DBManager. Defines connection as a class attribute 
    which is a connection to a google cloud database, and a connection
    object (which is a representation of a socket with a mysql server). 
    DBManager uses the class constants: HOST, DATABASE, USER and PASSWORD 
    to initialise this object, and stores the object in the connection attribute."""
    def __init__(self, connection=None):
        if(connection == None):
            try:
                #create a connection to the database 
                connection = p.connect(DBManager.HOST, DBManager.USER,
                                        DBManager.PASSWORD, DBManager.DATABASE, 
                                        connect_timeout=10)

            except p.OperationalError(): #connection issues 
                pass
            except p.NotSupportedError: #database API not supported by database 
                pass
            except p.InternalError: # error internal to db
                pass
            except p.DatabaseError(): # catchall in case of unanticipated errors
                pass
        self.connection = connection
    
    def connect(self):
        if(self.connection == None):
            try:
                #create a connection to the database 
                self.connection = p.connect(DBManager.HOST, DBManager.USER,
                                        DBManager.PASSWORD, DBManager.DATABASE, 
                                        connect_timeout=10)
                
            except p.OperationalError(): #connection issues 
                pass
            except p.NotSupportedError: #database API not supported by database 
                pass
            except p.InternalError: # error internal to db
                pass
            except p.DatabaseError(): # catchall in case of unanticipated errors
                pass
    
    """ __enter__ and __exit__ are required functions for the with .. as ..:
    statment to be functional in user defined classes. """
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close

    """close() sends a quit message ot the db and closes the 
    socket/conenction to the database. Any uncommitted changes
    will be lost."""
    def close(self):
        try: 
            self.connection.close()
        except (p.OperationalError, p.InternalError, p.NotSupportedError):
            # db errors while closing
            pass
        except p.DatabaseError: # catchall in case of unanticipated errors
            pass
    
    @abstractmethod
    def createTable(self):
        pass

    @abstractmethod
    def getAll(self, table):
        pass

    @abstractmethod
    def getItem(self):
        pass

    @abstractmethod
    def insertItem(self):
        pass

    @abstractmethod
    def updateItem(self):
        pass

