from abc import ABC, abstractmethod

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from consts import *


class ClientModel:
    def __init__(self, id=0, fullname='', telephone='', address='', email='', is_company=False):
        self.id = id
        self.fullname = fullname
        self.telephone = telephone
        self.address = address
        self.email = email
        self.is_company = is_company


class ClientRepository(ABC):
    @abstractmethod
    def create(self, data: ClientModel):
        pass

    @abstractmethod
    def get(self, id: int) -> ClientModel:
        pass

    @abstractmethod
    def update(self, data: ClientModel) -> bool:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> list[ClientModel]:
        pass

    @abstractmethod
    def find_by_name(self, fullname: str) -> list[ClientModel]:
        pass


class ClientRepositoryImpl(ClientRepository):
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
            print('Unable to connect to the database')
            exit(-1)

    def create(self, data):
        query_text = ('INSERT INTO clients (fullname, telephone, address, email, is_company) '
                      'VALUES (?, ?, ?, ?, ?)')
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.fullname)
        query.addBindValue(data.telephone)
        query.addBindValue(data.address)
        query.addBindValue(data.email)
        query.addBindValue(data.is_company)

        return query.exec()

    def get(self, id):
        query_text = 'SELECT * FROM clients WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        if not query.exec():
            exit("Couldn't execute the query!")

        query.next()
        return ClientModel(query.value(0),
                           query.value(1),
                           query.value(2),
                           query.value(3),
                           query.value(4),
                           query.value(5))

    def update(self, data):
        query_text = "UPDATE clients SET fullname=?, telephone=?, address=?, email=?, is_company=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.fullname)
        query.addBindValue(data.telephone)
        query.addBindValue(data.address)
        query.addBindValue(data.email)
        query.addBindValue(data.is_company)
        query.addBindValue(data.id)

        return query.exec()

    def delete(self, user_id):
        query_text = 'DELETE FROM clients WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(user_id)

        return query.exec()

    def get_all(self):
        query_text = 'SELECT * FROM clients ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!")

        res = []
        while query.next():
            res.append(ClientModel(query.value(0),
                                   query.value(1),
                                   query.value(2),
                                   query.value(3),
                                   query.value(4),
                                   query.value(5)))

        return res

    def get_names_and_ids(self):
        query_text = 'SELECT fullname, id FROM clients ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!")

        res = []
        while query.next():
            res.append(ClientModel(fullname=query.value(0),
                                   id=query.value(1)))

        return res

    def find_by_name(self, fullname: str) -> list[ClientModel]:
        query_text = 'SELECT * FROM clients WHERE fullname LIKE ?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(fullname + '%')

        if not query.exec():
            print("Couldn't execute the query!")
            return []

        res = []
        while query.next():
            res.append(ClientModel(query.value(0),
                                   query.value(1),
                                   query.value(2),
                                   query.value(3),
                                   query.value(4),
                                   query.value(5)))

        return res


client_repository_impl = ClientRepositoryImpl()
