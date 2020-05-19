#!/usr/bin/python3
import pymysql as p
from abc import ABC, abstractmethod
from db_exception import DBException


class DBManager(ABC):
    USER = "root"
    PASSWORD = "toor"
    HOST =  "35.201.0.12"
    DATABASE = "pi-database"

    """ Initialise DBManager. Defines connection as a class attribute
    (which is a representation of a socket with a mysql server) and creates
    connection to gcloud database.
    DBManager uses the class constants: HOST, DATABASE, USER and PASSWORD
    to initialise this object, and store the connection object."""
    def __init__(self, connection=None):
        if(connection is None):
            try:
                # create a connection to the database
                connection = p.connect(
                    DBManager.HOST, DBManager.USER, DBManager.PASSWORD,
                    DBManager.DATABASE, connect_timeout=10)
            except p.Error as e:    # all errors related to db functioning
                raise DBException('DB Error connecting to pi-database',
                                  e.args[1], e.args[0])
            except Exception as e:   # catch any other types of errors
                raise DBException('NON-DB Error connecting to pi-database',
                                  str(e.args))
        self.connection = connection

    """Connect method connects to the database, in case of initialisation
    not working, or self.connection being closed for another reason."""
    def connect(self):
        # check the connection does not exist before attempting
        # to connect again.
        if(self.connection is None):
            try:
                self.connection = p.connect(
                    DBManager.HOST, DBManager.USER, DBManager.PASSWORD,
                    DBManager.DATABASE, connect_timeout=10)
            except p.Error as e:
                raise DBException('DB-Error connecting to pi-database',
                                  e.args[1], e.args[0])
            except Exception as e:   # catch any other types of errors
                raise DBException('NON-DB Error connecting to pi-database',
                                  str(e.args))

    """ __enter__ and __exit__ are required functions for the 
    'with .. as ..:' statment to be functional in user defined classes."""
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close

    """close() sends a quit message to the database and closes the
    socket/conenction to the database. Any uncommitted changes
    will be lost."""
    def close(self):
        try:
            self.connection.close()
        except p.Error as e:    # Catch all errors related to db functioning
            raise DBException('DB Error closing connection to pi-database',
                              e.args[1], e.args[0])

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
