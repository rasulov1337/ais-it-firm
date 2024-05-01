from abc import ABC, abstractmethod
from PyQt6.QtSql import QSqlDatabase
from consts import *


class BaseRepository(ABC):

    def __init__(self):
        # Init DB connection
        self.db = QSqlDatabase.addDatabase('QPSQL')
        self.db.setHostName(DB_HOST_NAME)
        self.db.setPort(DB_PORT)
        self.db.setDatabaseName(DB_NAME)
        self.db.setUserName(DB_USERNAME)
        self.db.setPassword(DB_PASSWORD)

        self.db.open()
        if not self.db.open():
            print('Unable to connect to the database: ', self.db.lastError().databaseText())
            exit(-1)

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def create(self, data) -> bool:
        pass

    @abstractmethod
    def update(self, data) -> bool:
        pass
